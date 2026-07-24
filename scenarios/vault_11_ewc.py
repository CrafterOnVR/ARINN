import os
import sys
import torch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from arinn_core.ewc_immunity import ImmuneSystemEWC

def run_scenario():
    print("=== EXECUTING VAULT 11 (The Immune System) SCENARIO ===")
    
    immune = ImmuneSystemEWC(lambda_ewc=50.0)
    
    # Mock golden seed
    golden_weights = {
        "layer_1.weight": torch.ones(10, 10, dtype=torch.float16)
    }
    
    immune.register_golden_seed(golden_weights)
    
    print("\n[SCENARIO] Applying catastrophic mutation (changing all weights to 0)...")
    bad_mutation = {
        "layer_1.weight": torch.zeros(10, 10, dtype=torch.float16)
    }
    
    immune.evaluate_mutation(bad_mutation, collapse_threshold=100.0)
    
    print("\n[SCENARIO] Applying safe mutation (changing a few weights slightly)...")
    good_mutation = {
        "layer_1.weight": torch.ones(10, 10, dtype=torch.float16) * 0.99
    }
    
    immune.evaluate_mutation(good_mutation, collapse_threshold=100.0)

if __name__ == "__main__":
    run_scenario()
