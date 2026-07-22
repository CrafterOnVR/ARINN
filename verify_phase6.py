
import asyncio
from arinn_core.identity import ArinnIdentity
from arinn_core.cross_verifier import CrossVerifier
from arinn_core.sandbox import SandboxExecutor
from automation_engine import TaskForecaster

def test_explainable_reasoning():
    print("\n--- Testing Explainable Reasoning ---")
    identity = ArinnIdentity()
    
    # Force fake Phase 6 for testing
    identity.bootloader.current_phase = 5 # AUTONOMOUS_SCHOLAR = 5 in default
    
    # Test Explanation
    mastery_high = 0.95
    trace = identity.explain_decision("MOVE_TO_NEW_TOPIC", mastery_high)
    assert "[Reasoning Trace]" in trace
    assert "Mastery > 90%" in trace
    print("[PASS] High Mastery Trace consistent.")
    
    mastery_low = 0.50
    trace = identity.explain_decision("DEEP_DIVE", mastery_low)
    assert "Mastery < 80%" in trace
    print("[PASS] Low Mastery Trace consistent.")

def test_cross_verifier():
    print("\n--- Testing Cross Verifier ---")
    verifier = CrossVerifier()
    
    # Test Claim
    result = verifier.verify_fact("Python is a programming language")
    # Current implementation is simulated structure, so checking structure return
    assert "trusted" in result
    assert "score" in result
    assert "web search verification pending" in result.get("note", "").lower()
    print("[PASS] Verifier structure valid.")
    
    # Test Trust Check
    assert verifier.check_source_trust("https://wikipedia.org/wiki/AI")
    assert not verifier.check_source_trust("https://fake-news.com")
    print("[PASS] Trust whitelist working.")

def test_sandbox():
    print("\n--- Testing Sandbox Execution ---")
    sandbox = SandboxExecutor(timeout_seconds=2.0)
    
    # 1. Valid Code
    res = sandbox.run_snippet("print('Hello Sandbox')")
    assert res["success"]
    assert "Hello Sandbox" in res["stdout"]
    print("[PASS] Simple execution successful.")
    
    # 2. Timeout
    res = sandbox.run_snippet("import time; time.sleep(3)")
    assert res["timed_out"]
    assert not res["success"]
    print("[PASS] Timeout constraint enforced.")
    
    # 3. Error
    res = sandbox.run_snippet("1 / 0")
    assert not res["success"]
    assert "ZeroDivisionError" in res["stderr"]
    print("[PASS] Error containment successful.")

def test_forecasting():
    print("\n--- Testing Task Forecasting ---")
    forecaster = TaskForecaster()
    
    # Train Pattern: RESEARCH -> ANALYZE
    forecaster.record_transition("RESEARCH")
    forecaster.record_transition("ANALYZE")
    forecaster.record_transition("RESEARCH")
    forecaster.record_transition("ANALYZE")
    forecaster.record_transition("RESEARCH")
    
    # Predict next after RESEARCH
    preds = forecaster.predict_next("RESEARCH")
    # Should contain ANALYZE
    top_pred, prob = preds[0]
    
    assert top_pred == "ANALYZE"
    assert prob == 1.0
    print(f"[PASS] Correctly predicted 'ANALYZE' follows 'RESEARCH' (Prob: {prob:.1%})")

if __name__ == "__main__":
    try:
        test_explainable_reasoning()
        test_cross_verifier()
        test_sandbox()
        test_forecasting()
        print("\n(SUCCESS) ALL PHASE 6 VERIFICATIONS PASSED.")
    except Exception as e:
        print(f"\n(FAIL) VERIFICATION FAILED: {e}")
        exit(1)
