import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, LogitsProcessor, LogitsProcessorList, TextIteratorStreamer
from peft import PeftModel
from safetensors.torch import load_file
import time
import threading
import sys

class NaNGuardLogitsProcessor(LogitsProcessor):
    def __call__(self, input_ids, scores):
        # Prevent DirectML from crashing during multinomial sampling by purging NaNs and Infs.
        # Avoid torch.nan_to_num to prevent CPU fallback performance bottlenecks on DML.
        scores[scores != scores] = -1e4
        scores[scores == float('inf')] = 1e4
        scores[scores == float('-inf')] = -1e4
        return scores

class NeuralCore:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NeuralCore, cls).__new__(cls)
            cls._instance._init_model()
        return cls._instance
        
    def _init_model(self):
        print("[NEURAL] Initializing True Neural Architecture...")
        
        try:
            import torch_directml
            self.device = torch_directml.device()
            print(f"[NEURAL] DirectML detected. Targeting: {self.device}")
        except ImportError:
            self.device = torch.device("cpu")
            print(f"[NEURAL] DirectML not found. Falling back to CPU: {self.device}")
        
        model_id = "Qwen/Qwen2.5-1.5B-Instruct"
        print(f"[NEURAL] Loading Base Model: {model_id}...")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16)
            
            adapter_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "arinn_lora_weights", "arinn_latest_adapter"))
            stable_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "arinn_lora_weights", "arinn_previous_stable"))
            
            if os.path.exists(adapter_path):
                # NaN Quarantine Protocol
                try:
                    state_dict = load_file(os.path.join(adapter_path, "adapter_model.safetensors"))
                    if any(torch.isnan(v).any() for v in state_dict.values()):
                        print(f"[NEURAL] QUARANTINE WARNING: {adapter_path} contains NaN corruption! Aggressively rejecting adapter.")
                        raise ValueError("Mathematical NaN Corruption Detected in LoRA Weights")
                        
                    print(f"[NEURAL] Found pristine Swarm-trained LoRA adapter! Injecting weights from: {adapter_path}")
                    self.model = PeftModel.from_pretrained(self.model, adapter_path)
                    print("[NEURAL] Fusing LoRA weights into base tensors for high-speed inference...")
                    self.model = self.model.merge_and_unload()
                except Exception as lora_e:
                    print(f"[NEURAL] WARNING: latest_adapter corrupted ({lora_e}). Attempting fallback to previous_stable...")
                    if os.path.exists(stable_path):
                        try:
                            state_dict = load_file(os.path.join(stable_path, "adapter_model.safetensors"))
                            if any(torch.isnan(v).any() for v in state_dict.values()):
                                raise ValueError("Mathematical NaN Corruption Detected in Stable Weights")
                            self.model = PeftModel.from_pretrained(self.model, stable_path)
                            print("[NEURAL] Fusing stable LoRA weights...")
                            self.model = self.model.merge_and_unload()
                            print("[NEURAL] Successfully loaded previous_stable adapter.")
                        except Exception as e2:
                            print(f"[NEURAL] Stable adapter also corrupted ({e2}). Running on pure baseline weights.")
                    else:
                        print("[NEURAL] No stable fallback found. Running on baseline weights.")
            elif os.path.exists(stable_path):
                try:
                    state_dict = load_file(os.path.join(stable_path, "adapter_model.safetensors"))
                    if any(torch.isnan(v).any() for v in state_dict.values()):
                        raise ValueError("Mathematical NaN Corruption")
                    print(f"[NEURAL] latest_adapter missing. Found pristine previous_stable. Injecting weights from: {stable_path}")
                    self.model = PeftModel.from_pretrained(self.model, stable_path)
                    print("[NEURAL] Fusing stable LoRA weights...")
                    self.model = self.model.merge_and_unload()
                except Exception as e:
                    print(f"[NEURAL] Stable adapter corrupted ({e}). Running on baseline weights.")
            else:
                print("[NEURAL] No LoRA adapter found. Running on baseline weights.")
                
            self.model.to(self.device)
            self.model.eval()
            print("[NEURAL] Neural Core Online and Ready for Inference.")
            self.mode = "TRUE_NEURAL"
        except Exception as e:
            print(f"[NEURAL] Architecture initialization failed: {e}")
            self.mode = "SYMBOLIC"
            self.model = None

    def generate_thought(self, prompt, max_tokens=1024):
        if self.mode != "TRUE_NEURAL" or self.model is None:
            raise RuntimeError("True Neural Core is offline.")
            
        print("[NEURAL] Executing forward pass...")
        messages = [
            {"role": "system", "content": "You are ARINN, a master Python developer. Output only raw code. Do not use markdown blocks."},
            {"role": "user", "content": prompt}
        ]
        
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
        
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        
        generation_kwargs = dict(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            logits_processor=LogitsProcessorList([NaNGuardLogitsProcessor()]),
            pad_token_id=self.tokenizer.eos_token_id,
            streamer=streamer
        )
        
        thread = threading.Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()
        
        start_time = time.time()
        tokens_generated = 0
        response = ""
        
        for new_text in streamer:
            response += new_text
            tokens_generated += 1
            elapsed = time.time() - start_time
            if elapsed > 0 and tokens_generated % 2 == 0:
                tps = tokens_generated / elapsed
                remaining = max_tokens - tokens_generated
                eta = remaining / tps if tps > 0 else 0
                sys.stdout.write(f"\r\033[94m[NEURAL] Executing forward pass... (TPS: {tps:.1f} | ETA: {eta:.1f}s)\033[0m          ")
                sys.stdout.flush()
                
        sys.stdout.write(f"\r\033[94m[NEURAL] Forward pass complete! (Final TPS: {tokens_generated/(time.time()-start_time):.1f})\033[0m{' ' * 20}\n")
        sys.stdout.flush()
        
        return response, {}
