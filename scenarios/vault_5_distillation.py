import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from arinn_core.distillation import DatasetDistiller

def run_scenario():
    print("=== EXECUTING VAULT 5 (Dataset Distillation) SCENARIO ===")
    
    distiller = DatasetDistiller()
    
    mock_jsonl_path = "data/synthetic_datasets/arinn_training_data_2026-07-23.jsonl"
    
    distilled_tensor = distiller.distill_jsonl_dataset(mock_jsonl_path)
    
    print(f"[VAULT-5] Final Tensor Shape: {distilled_tensor.shape}")
    print("[VAULT-5] Dataset Distillation Complete.")

if __name__ == "__main__":
    run_scenario()
