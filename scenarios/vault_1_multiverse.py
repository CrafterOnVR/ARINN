import os
import torch
from safetensors.torch import save_file
import sys

# Add core to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from arinn_core.liquid_multiverse import LiquidMerger

def create_dummy_lora(path, name):
    os.makedirs(path, exist_ok=True)
    # Create a random weight matrix
    weights = {
        "base_model.model.model.layers.0.self_attn.q_proj.lora_A.weight": torch.randn(16, 128, dtype=torch.float16),
        "base_model.model.model.layers.0.self_attn.q_proj.lora_B.weight": torch.randn(128, 16, dtype=torch.float16)
    }
    save_file(weights, os.path.join(path, "adapter_model.safetensors"))
    with open(os.path.join(path, "adapter_config.json"), "w") as f:
        f.write('{"r": 16, "lora_alpha": 32, "target_modules": ["q_proj"]}')
    print(f"[SCENARIO] Created dummy divergent timeline adapter: {name}")

def run_scenario():
    print("=== EXECUTING VAULT 1 SCENARIO ===")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "arinn_lora_weights"))
    
    alpha_path = os.path.join(base_dir, "timeline_alpha")
    beta_path = os.path.join(base_dir, "timeline_beta")
    merged_path = os.path.join(base_dir, "collapsed_timeline")
    
    create_dummy_lora(alpha_path, "Timeline Alpha")
    create_dummy_lora(beta_path, "Timeline Beta")
    
    merger = LiquidMerger()
    merger.wasserstein_barycenter_merge(alpha_path, beta_path, merged_path)

if __name__ == "__main__":
    run_scenario()
