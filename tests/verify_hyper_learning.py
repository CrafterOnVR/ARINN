
import os
import time
from arinn_core.hyper_learning import KnowledgeTracker, RecursiveOptimizer, SafetyLock

def test_hyper_learning():
    print("\n--- Testing Phase 17 Hyper-Efficiency ---")
    
    # 1. Velocity Tracking
    tracker = KnowledgeTracker()
    tracker = KnowledgeTracker()
    # Mock history manually to control time
    now = time.time()
    tracker.history = [
        (now - 2.0, 10.0),
        (now - 1.0, 10.0),
        (now, 10.0)
    ]
    tracker.total_gain = 30.0
    
    vel = tracker.get_velocity()
    # 30 units / 2.0s -> 15.0 KUPS
    print(f"[PASS] Velocity Calculated: {vel:.2f} KUPS")
    assert vel > 0
    
    # 2. Recursive Optimization
    optimizer = RecursiveOptimizer()
    action = optimizer.optimize(current_velocity=2.0)
    print(f"[PASS] Optimization Action: {action}")
    assert action == "SCALING_UP"
    assert optimizer.params["recursion_depth"] > 1
    
    action = optimizer.optimize(current_velocity=0.01)
    print(f"[PASS] Optimization Action: {action}")
    assert action == "STABILIZING"
    
    # 3. Manual Override
    safety = SafetyLock("test_override.lock")
    assert not safety.is_locked()
    
    safety.engage_lock()
    print(f"[PASS] Lock Engaged.")
    assert safety.is_locked()
    
    safety.release_lock()
    print(f"[PASS] Lock Released.")
    assert not safety.is_locked()
    
    if os.path.exists("test_override.lock"):
        os.remove("test_override.lock")

if __name__ == "__main__":
    try:
        test_hyper_learning()
        print("\n(SUCCESS) ALL PHASE 17 VERIFICATIONS PASSED.")
    except Exception as e:
        print(f"\n(FAIL) VERIFICATION FAILED: {e}")
        exit(1)
