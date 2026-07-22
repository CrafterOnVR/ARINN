
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
print(f"[DOWNLOADER] Starting download for {model_id}...")

try:
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    print("[DOWNLOADER] Tokenizer collected.")
    
    model = AutoModelForCausalLM.from_pretrained(model_id)
    print("[DOWNLOADER] Model weights collected.")
    
    print("[DOWNLOADER] Success. Brain is ready.")
except Exception as e:
    print(f"[DOWNLOADER] Error: {e}")
