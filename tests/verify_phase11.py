
import os
import torch
import time
from arinn_core.hivemind import ArinnHivemind, ExpertType
from arinn_core.referee import DebateArena
from arinn_core.memory import SecureMemory

def test_asymmetry():
    print("\n--- Testing Expert Asymmetry ---")
    mind = ArinnHivemind(num_experts=5)
    
    # Check if experts have different types
    types_found = set()
    for exp in mind.experts:
        types_found.add(exp.expert_type)
        print(f"Expert {exp.expert_type}: {exp.activation}")

    assert len(types_found) > 1
    assert ExpertType.CREATIVE in types_found
    print("[PASS] Experts are asymmetric.")
    return mind

def test_referee(mind):
    print("\n--- Testing Referee System ---")
    arena = DebateArena(mind)
    
    # Fake input
    x = torch.randn(1, 2)
    result = arena.conduct_debate(x)
    
    print(f"Referee Confidence: {result['referee_confidence']:.4f}")
    assert 0.0 <= result['referee_confidence'] <= 1.0
    print("[PASS] Referee conducted debate.")

def test_memory_darwinism():
    print("\n--- Testing Memory Darwinism ---")
    # Use a temp file
    temp_mem = "test_darwin.enc"
    temp_key = "test_darwin.key"
    if os.path.exists(temp_mem): os.remove(temp_mem)
    if os.path.exists(temp_key): os.remove(temp_key)
    
    mem = SecureMemory(key_file=temp_key, storage_file=temp_mem)
    
    # Clean output from previous run if any
    mem.memory_cache = {}
    
    # Store 5 items
    for i in range(5):
        mem.store(f"item{i}", f"data{i}", initial_utility=0.5)
        
    # Access item 0 and 1 repeatedly (boost utility)
    mem.retrieve("item0")
    mem.retrieve("item0")
    mem.retrieve("item1")
    
    # Prune keeping 60% (3 items)
    removed = mem.prune_memories(retention_ratio=0.6)
    
    keys = mem.list_keys()
    print(f"Remaining Keys: {keys}")
    print(f"Removed: {removed}")
    
    assert "item0" in keys # High utility
    assert len(keys) == 3
    assert removed == 2
    
    print("[PASS] Darwinian pruning successful.")
    
    # Cleanup
    if os.path.exists(temp_mem): os.remove(temp_mem)
    if os.path.exists(temp_key): os.remove(temp_key)

if __name__ == "__main__":
    try:
        mind = test_asymmetry()
        test_referee(mind)
        test_memory_darwinism()
        print("\n(SUCCESS) ALL PHASE 11 VERIFICATIONS PASSED.")
    except Exception as e:
        print(f"\n(FAIL) VERIFICATION FAILED: {e}")
        # import traceback
        # traceback.print_exc()
        exit(1)
