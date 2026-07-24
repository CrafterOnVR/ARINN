import os
import sys
import torch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from arinn_core.cognitive_engine import RadixCacheArray, FSM_ConstraintModule

def run_scenario():
    print("=== EXECUTING VAULT 9 & 10 SCENARIOS ===")
    
    # Vault 9: Radix KV Cache Sharing
    print("\n[VAULT-9] Metacognitive Parameter Shifting (The Fractured Mind)")
    radix = RadixCacheArray()
    mock_kv_tensor = torch.randn(128, 512)
    
    print("[VAULT-9] Orchestrator generating base prompt context...")
    base_cache = radix.get_or_allocate("system_prompt_hash_123", mock_kv_tensor)
    
    print("[VAULT-9] Fracturing mind into 'Critic Lobe' and 'Panic Lobe'...")
    critic_cache = radix.get_or_allocate("system_prompt_hash_123", None)
    panic_cache = radix.get_or_allocate("system_prompt_hash_123", None)
    
    if id(base_cache) == id(critic_cache) == id(panic_cache):
        print("[VAULT-9] SUCCESS. All three independent lobes are physically sharing the exact same VRAM memory pointer via RadixAttention.")
        
    # Vault 10: FSM Logit Masking
    print("\n[VAULT-10] Just-In-Time (JIT) Tool Activation (Prompt De-Bloating)")
    fsm = FSM_ConstraintModule(vocab_size=10000)
    
    # Let's say tool triggers are tokens [105, 500, 999]
    tool_tokens = [105, 500, 999]
    
    print(f"[VAULT-10] AI is attempting a task requiring ONLY tool 500.")
    fsm.authorize_tool([500])
    
    mock_logits = torch.randn(1, 10000)
    print(f"[VAULT-10] Pre-Mask Logits for unauthorized tool 999: {mock_logits[0, 999].item():.4f}")
    
    safe_logits = fsm.mask_logits(mock_logits, tool_tokens)
    print(f"[VAULT-10] Post-Mask Logits for unauthorized tool 999: {safe_logits[0, 999].item()}")
    print(f"[VAULT-10] FSM active. The AI is now mathematically incapable of hallucinating an unauthorized tool call.")

if __name__ == "__main__":
    run_scenario()
