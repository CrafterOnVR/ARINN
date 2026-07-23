import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

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
            self.model = AutoModelForCausalLM.from_pretrained(model_id)
            
            adapter_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "arinn_lora_weights", "arinn_latest_adapter"))
            stable_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "arinn_lora_weights", "arinn_previous_stable"))
            
            if os.path.exists(adapter_path):
                print(f"[NEURAL] Found Swarm-trained LoRA adapter! Injecting weights from: {adapter_path}")
                try:
                    self.model = PeftModel.from_pretrained(self.model, adapter_path)
                except Exception as lora_e:
                    print(f"[NEURAL] WARNING: latest_adapter corrupted ({lora_e}). Attempting fallback to previous_stable...")
                    if os.path.exists(stable_path):
                        self.model = PeftModel.from_pretrained(self.model, stable_path)
                        print("[NEURAL] Successfully loaded previous_stable adapter.")
                    else:
                        print("[NEURAL] No stable fallback found. Running on baseline weights.")
            elif os.path.exists(stable_path):
                print(f"[NEURAL] latest_adapter missing. Found previous_stable. Injecting weights from: {stable_path}")
                self.model = PeftModel.from_pretrained(self.model, stable_path)
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
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=False,
                temperature=None,
                top_p=None,
                top_k=None,
                repetition_penalty=1.15,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, outputs)]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return response, {}
