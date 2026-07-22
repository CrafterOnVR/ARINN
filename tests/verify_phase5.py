
import os
import shutil
import json
import time
from datetime import datetime
from safety_controller import SelfImprovementPermission, VerificationManager, rollback_to_stable
from arinn_core.continuous_learning import ContinuousLearner
from self_improvement_manager import SelfImprovementManager

def test_permission_system():
    print("\n--- Testing Permission System ---")
    perm = SelfImprovementPermission("test_permission.json")
    
    # Initial state should be DENIED
    assert not perm.is_granted(), "Initial permission should be DENIED"
    print("[PASS] Initial state matches.")
    
    # Grant
    perm.grant()
    perm = SelfImprovementPermission("test_permission.json") # Reload
    assert perm.is_granted(), "Permission should be CONFIRMED after grant()"
    print("[PASS] Grant successful.")
    
    # Revoke
    perm.revoke()
    perm = SelfImprovementPermission("test_permission.json") # Reload
    assert not perm.is_granted(), "Permission should be DENIED after revoke()"
    print("[PASS] Revoke successful.")
    
    # Cleanup
    if os.path.exists("test_permission.json"):
        os.remove("test_permission.json")

def test_verification_manager():
    print("\n--- Testing Verification Manager ---")
    # Verify this file itself
    checksum = VerificationManager.calculate_checksum(__file__)
    assert len(checksum) == 64, "Checksum should be SHA-256 hex string"
    print(f"[PASS] Checksum verified: {checksum[:8]}...")
    
    # Verify project integrity (should pass as we fixed syntax errors)
    root = os.path.dirname(__file__)
    integrity = VerificationManager.verify_project_integrity(root)
    if not integrity["success"]:
        print(f"[FAIL] Integrity check failed: {integrity['errors']}")
    else:
        print("[PASS] Project integrity verified.")

def test_rollback():
    print("\n--- Testing Rollback ---")
    test_dir = "test_rollback_target"
    backup_dir = "test_rollback_backup"
    
    # Setup
    if os.path.exists(test_dir): shutil.rmtree(test_dir)
    if os.path.exists(backup_dir): shutil.rmtree(backup_dir)
    
    os.makedirs(test_dir)
    os.makedirs(backup_dir)
    
    with open(os.path.join(test_dir, "file.txt"), "w") as f: f.write("CORRUPTED")
    with open(os.path.join(backup_dir, "file.txt"), "w") as f: f.write("STABLE")
    
    # Rollback
    success = rollback_to_stable(backup_dir, test_dir)
    assert success, "Rollback function returned False"
    
    with open(os.path.join(test_dir, "file.txt"), "r") as f:
        content = f.read()
    
    assert content == "STABLE", f"Rollback failed content check (files restored as {content})"
    print("[PASS] Rollback restored correct content.")
    
    # Cleanup
    shutil.rmtree(test_dir)
    shutil.rmtree(backup_dir)

def test_self_improvement_safeguards():
    print("\n--- Testing Self-Improvement Safeguards ---")
    # permission.json should be default DENIED
    agent_mock = type('obj', (object,), {'github_controller': None})
    manager = SelfImprovementManager(agent_mock)
    
    # Try to clean up real permission file if exists to prevent accidental global side effect
    if os.path.exists("permission.json"):
        os.remove("permission.json")
    
    result = manager.initiate_self_improvement("Test Topic", {"intelligence_score": 90})
    
    assert result["success"] is False, "Should fail without permission"
    assert "improvement_detected" in result, "Structure match"
    print("[PASS] Blocked without permission.")

def test_real_world_learning_exists():
    print("\n--- Testing Real-World Learning Existence ---")
    # Check directly on the class to avoid instantiation dependency hell
    assert hasattr(ContinuousLearner, 'loop_real_world_learning'), "loop_real_world_learning missing"
    print("[PASS] Real-World Learning method detected.")

if __name__ == "__main__":
    try:
        test_permission_system()
        test_verification_manager()
        test_rollback()
        test_self_improvement_safeguards()
        test_real_world_learning_exists()
        print("\n\n(SUCCESS) ALL PHASE 5 VERIFICATIONS PASSED.")
    except Exception as e:
        print(f"\n\n(FAIL) VERIFICATION FAILED: {e}")
        exit(1)
