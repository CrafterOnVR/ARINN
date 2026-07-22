
import os
import time
import random
from arinn_core.efficiency_engine import CostAccountant, CompressionEngine, StrategyOptimizer
from arinn_core.representation_manager import RepresentationController
from arinn_core.memory import SecureMemory

def test_efficiency_engine():
    print("\n--- Testing Efficiency Engine ---")
    
    
    # 1. Cost Accounting
    accountant = CostAccountant()
    session_id = "test_sess"
    accountant.start_session(session_id)
    time.sleep(0.01)
    accountant.log_update(session_id)
    # Gain scales with data size now, so 1.0 is fine for test
    roi = accountant.end_session(session_id, knowledge_gain=100.0) 
    assert roi > 0
    print(f"[PASS] ROI Calculated: {roi:.2f}")
    
    # 2. Compression
    compressor = CompressionEngine()
    long_string = "A" * 100
    res = compressor.compress_concept(long_string)
    assert res['ratio'] > 1.0 # Should be compressed
    assert res['retained_power'] == 1.0 # Zlib is Lossless!
    print(f"[PASS] Compression Ratio: {res['ratio']:.2f}")
    
    # 3. Strategy Darwinism
    optimizer = StrategyOptimizer()
    strategy = optimizer.select_strategy()
    print(f"[PASS] Strategy Selected: {strategy}")
    optimizer.update_fitness(strategy, roi_score=2.0)
    assert optimizer.strategies[strategy]['fitness'] > 0.2
    print(f"[PASS] Strategy Fitness Updated.")

def test_representation_switching():
    print("\n--- Testing Representation Manager ---")
    controller = RepresentationController()
    fmt = controller.choose_representation("Logic Problem")
    assert fmt == "Symbolic"
    print(f"[PASS] Chose {fmt} for Logic.")
    
    new_fmt = controller.switch_representation(fmt, recent_error=1.0) # EMA -> 0.3
    new_fmt = controller.switch_representation(fmt, recent_error=1.0) # EMA -> 0.3 + 0.7*0.3 = 0.51 > 0.4
    
    if new_fmt == fmt:
         print(f"[FAIL] Did not switch. EMA Error: {controller.error_history[fmt]}")
    
    assert new_fmt != fmt
    print(f"[PASS] Switched to {new_fmt} due to high error.")

def test_memory_heatmap():
    print("\n--- Testing Memory Heat Map ---")
    mem = SecureMemory(storage_file="test_phase14_mem.enc")
    
    # Store Hot and Cold items
    mem.store("hot_item", "important", initial_utility=0.9)
    mem.store("cold_item", "trivial", initial_utility=0.0)
    
    # Access hot item to boost temp
    mem.retrieve("hot_item")
    
    # Get Map
    heat_map = mem.get_heat_map()
    assert heat_map["hot_item"] > heat_map["cold_item"]
    print(f"[PASS] Heat Map Valid (Hot > Cold).")
    
    # Archive Cold
    count = mem.archive_cold_memories(temp_threshold=0.2)
    assert count >= 1
    assert mem.memory_cache["cold_item"]["priority"] == "ARCHIVE"
    print(f"[PASS] Archived {count} Cold memories.")
    
    # Cleanup
    if os.path.exists("test_phase14_mem.enc"):
        os.remove("test_phase14_mem.enc")

if __name__ == "__main__":
    try:
        test_efficiency_engine()
        test_representation_switching()
        test_memory_heatmap()
        print("\n(SUCCESS) ALL PHASE 14 VERIFICATIONS PASSED.")
    except Exception as e:
        print(f"\n(FAIL) VERIFICATION FAILED: {e}")
        exit(1)
