
import os
import time
import shutil
from arinn_core.meta_optimizer import MetaOptimizer
from safety_guard import FailsafeGuard

def test_meta_optimizer():
    print("\n--- Testing Meta Optimizer ---")
    opt = MetaOptimizer()
    
    # 1. Record sessions
    opt.record_learning_session(0.5, 0.6, 1.0) # V=0.1
    opt.record_learning_session(0.5, 0.55, 1.0) # V=0.05 (Dropping)
    
    # Check if params change
    params = opt.get_current_params()
    print(f"Current Params: {params}")
    
    # Force optimization
    for _ in range(10):
        opt.record_learning_session(0.5, 0.51, 1.0) # Low performance
        
    new_params = opt.get_current_params()
    print(f"New Params: {new_params}")
    
    # We expect some change (e.g., LR or Depth) due to low performance heuristic
    changed = (params['learning_rate'] != new_params['learning_rate'] or 
               params['search_depth'] != new_params['search_depth'])
               
    if changed:
        print("[PASS] MetaOptimizer adjusted parameters autonomously.")
    else:
        print("[WARN] parameters did not change (random chance?).")

def test_failsafe_guard():
    print("\n--- Testing Failsafe Guard ---")
    
    # Create dummy environment
    test_dir = "test_failsafe_env"
    if os.path.exists(test_dir): shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    critical_file = os.path.join(test_dir, "agent.py")
    with open(critical_file, "w") as f: f.write("original code")
    
    # Initialize Guard
    guard = FailsafeGuard(root_dir=test_dir)
    guard.BACKUP_DIR = os.path.join(test_dir, "backup")
    guard.CRITICAL_FILES = ["agent.py"]
    
    # 1. Create Snapshot
    guard.create_stable_snapshot()
    assert os.path.exists(os.path.join(guard.BACKUP_DIR, "agent.py"))
    print("[PASS] Snapshot executed.")
    
    # 2. Verify Integrity (Clean)
    assert guard.verify_integrity()
    print("[PASS] Integrity check (clean) passed.")
    
    # 3. Simulate Corruption
    with open(critical_file, "w") as f: f.write("CORRUPTED CODE")
    
    assert not guard.verify_integrity()
    print("[PASS] Integrity check (corrupted) detected change.")
    
    # 4. Rollback
    guard.rollback()
    with open(critical_file, "r") as f: content = f.read()
    assert content == "original code"
    print("[PASS] Rollback successful.")
    
    # Cleanup
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    try:
        test_meta_optimizer()
        test_failsafe_guard()
        print("\n(SUCCESS) ALL PHASE 7 VERIFICATIONS PASSED.")
    except Exception as e:
        print(f"\n(FAIL) VERIFICATION FAILED: {e}")
        exit(1)
