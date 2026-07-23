import os
import torch
import gc

class ARINNFineTuner:
    """
    Phase 10: The LoRA Fine-Tuning Engine.
    Uses Parameter-Efficient Fine-Tuning (PEFT) to train local models on ARINN's 
    synthetic Swarm datasets, allowing it to mathematically "grow" a brain overnight.
    """
    def __init__(self, model_id="Qwen/Qwen2.5-1.5B-Instruct", output_dir=None):
        self.model_id = model_id
        
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.output_dir = output_dir or os.path.join(project_root, "models", "arinn_lora_weights")
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def trigger_night_cycle(self, dataset_path: str):
        """
        Loads the dataset and triggers a LoRA fine-tuning run.
        """
        print("\n" + "="*50)
        print("🌙 [NIGHT CYCLE] INITIATING ARINN CORTEX UPGRADE")
        print("="*50)
        print(f"[LoRA] Target Dataset: {dataset_path}")
        print(f"[LoRA] Base Model: {self.model_id}")
        try:
            if torch.cuda.is_available():
                device_name = torch.cuda.get_device_name(0)
                vram_gb = round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 1)
                hw_string = f"{device_name} ({vram_gb}GB VRAM) detected."
            else:
                hw_string = "CPU / Alternative Accelerator detected."
        except Exception:
            hw_string = "Alternative Hardware detected."
            
        print(f"[LoRA] Hardware Check: {hw_string}")
        print("[LoRA] Loading Transformers and PEFT frameworks...")
        
        # Vault 1: Liquid Multiverse Snapshot
        try:
            from arinn_core.liquid_multiverse import LiquidMerger
            merger = LiquidMerger()
            merger.snapshot_golden_seed()
        except ImportError:
            print("[LIQUID] LiquidMerger not available. Skipping snapshot.")
        
        try:
            # We wrap the actual import to avoid crashing the whole Orchestrator 
            # if dependencies aren't installed yet.
            import transformers
            from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
            from datasets import load_dataset
        except ImportError as e:
            print(f"\n[WARNING] Missing Machine Learning frameworks! Error: {e}")
            print("To run the physical Night Cycle, you must install dependencies:")
            print("pip install torch transformers peft bitsandbytes datasets trl accelerate")
            print("Skipping actual weight mutation for this cycle. Resuming Swarm...\n")
            return False

        try:
            print("[LoRA] Loading Dataset...")
            dataset = load_dataset("json", data_files={"train": dataset_path}, split="train")
            
            # Formatting function for Instruction Tuning
            def format_prompts(examples):
                texts = []
                for msgs in examples["messages"]:
                    text = ""
                    for msg in msgs:
                        text += f"<|im_start|>{msg['role']}\n{msg['content']}<|im_end|>\n"
                    texts.append(text)
                return {"text": texts}
                
            formatted_dataset = dataset.map(format_prompts, batched=True)
            
            print("[LoRA] Loading Base Model...")
            
            # Fallback for AMD/Windows users without native CUDA
            has_cuda = torch.cuda.is_available()
            dml_device = None
            if not has_cuda:
                try:
                    import torch_directml
                    if torch_directml.is_available():
                        dml_device = torch_directml.device()
                        print(f"[LoRA] DirectML detected. Binding to {torch_directml.device_name(0)}")
                except ImportError:
                    pass
            
            if has_cuda:
                bnb_config = transformers.BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.float16
                )
                model = transformers.AutoModelForCausalLM.from_pretrained(
                    self.model_id,
                    quantization_config=bnb_config,
                    device_map="auto"
                )
            elif dml_device is not None:
                model = transformers.AutoModelForCausalLM.from_pretrained(
                    self.model_id,
                    torch_dtype=torch.float16
                )
                model.to(dml_device)
            else:
                print("[WARNING] CUDA not detected. Falling back to CPU for LoRA. This will be very slow!")
                model = transformers.AutoModelForCausalLM.from_pretrained(
                    self.model_id,
                    device_map="cpu",
                    torch_dtype=torch.float32
                )
                
            tokenizer = transformers.AutoTokenizer.from_pretrained(self.model_id)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
                
            model = prepare_model_for_kbit_training(model) if has_cuda else model
            
            lora_config = LoraConfig(
                r=8,
                lora_alpha=16,
                target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
                lora_dropout=0.05,
                bias="none",
                task_type="CAUSAL_LM"
            )
            
            model = get_peft_model(model, lora_config)
            
            print(f"[LoRA] Model architecture ready.")
            try:
                model.print_trainable_parameters()
            except AttributeError:
                pass
            print("[LoRA] Commencing Gradient Descent...")
            
            import math
            
            # Tokenize the dataset
            def tokenize_function(examples):
                return tokenizer(examples["text"], truncation=True, max_length=1024)
            
            tokenized_dataset = formatted_dataset.map(tokenize_function, batched=True)
            
            from transformers import DataCollatorForLanguageModeling
            data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)
            
            if dml_device is not None:
                print("[LoRA] Executing custom PyTorch gradient loop for AMD (DirectML)...")
                from torch.utils.data import DataLoader
                from tqdm import tqdm
                
                # Remove non-tensor columns so dataloader doesn't crash
                tokenized_dataset = tokenized_dataset.remove_columns(["text", "messages"])
                tokenized_dataset.set_format("torch")
                
                dataloader = DataLoader(tokenized_dataset, batch_size=2, collate_fn=data_collator)
                optimizer = torch.optim.AdamW(model.parameters(), lr=2e-4)
                
                model.train()
                max_steps = 1000
                progress_bar = tqdm(total=max_steps)
                step = 0
                
                for batch in dataloader:
                    batch = {k: v.to(dml_device) for k, v in batch.items()}
                    outputs = model(**batch)
                    loss = outputs.loss
                    loss.backward()
                    
                    optimizer.step()
                    optimizer.zero_grad()
                    progress_bar.update(1)
                    
                    step += 1
                    if step >= max_steps:
                        break
                        
                progress_bar.close()
            else:
                from transformers import Trainer
                training_args = transformers.TrainingArguments(
                    output_dir=self.output_dir,
                    per_device_train_batch_size=2,
                    gradient_accumulation_steps=4,
                    warmup_steps=5,
                    max_steps=1000, 
                    learning_rate=2e-4,
                    fp16=has_cuda,
                    logging_steps=10,
                    optim="paged_adamw_8bit" if has_cuda else "adamw_torch",
                    save_strategy="no" 
                )
                
                trainer = Trainer(
                    model=model,
                    train_dataset=tokenized_dataset,
                    args=training_args,
                    data_collator=data_collator
                )
                trainer.train()
            
            print("\n[LoRA] Training Complete! Synthesizing new Neural Weights...")
            final_path = os.path.join(self.output_dir, "arinn_latest_adapter")
            
            # DirectML tensors are opaque to the OS serializer, so we must pull the weights back to system RAM first
            if dml_device is not None:
                print("[LoRA] Offloading mutated weights from AMD VRAM to System RAM for serialization...")
                model = model.to("cpu")
                
            model.save_pretrained(final_path)
            
            print(f"[NIGHT CYCLE] SUCCESS. Brain upgraded. New weights saved to {final_path}")
            
            # Clean up VRAM
            # Clean up VRAM
            del model
            if 'trainer' in locals():
                del trainer
            gc.collect()
            torch.cuda.empty_cache()
            
            return True
            
        except Exception as e:
            print(f"\n[FATAL ERROR] Night Cycle Failed: {str(e)}")
            return False

if __name__ == "__main__":
    # Test the class
    tuner = ARINNFineTuner()
    # tuner.trigger_night_cycle("dummy_path.jsonl")
