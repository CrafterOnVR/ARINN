"""
Phase 29 & 54 Verification Script.
Tests the Imagination Engine (Dream) and the Calculator Protocol.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_calculator():
    print("=" * 60)
    print("  PHASE 54 VERIFICATION: The Calculator Protocol")
    print("=" * 60 + "\n")
    
    from arinn_core.calculator import Calculator  # type: ignore
    calc = Calculator()
    
    # Test 1: Detection
    print("[TEST 1] Pattern Detection...")
    assert calc.detect("Calculate 123 * 456") == "123 * 456"
    assert calc.detect("what is 2 + 2") == "2 + 2"
    assert calc.detect("compute 10 / 3") == "10 / 3"
    assert calc.detect("Hello world") is None
    print("  [PASS] Correctly detects math requests and ignores non-math.\n")
    
    # Test 2: Safe Evaluation
    print("[TEST 2] Safe Evaluation...")
    result, err = calc.evaluate("123 * 456")
    assert result == 56088, f"Expected 56088, got {result}"
    assert err is None
    print(f"  123 * 456 = {result} [CORRECT]")
    
    result, err = calc.evaluate("2 ** 10")
    assert result == 1024
    print(f"  2 ** 10 = {result} [CORRECT]")
    
    result, err = calc.evaluate("100 / 4 + 3")
    assert result == 28.0
    print(f"  100 / 4 + 3 = {result} [CORRECT]")
    print("  [PASS] All arithmetic evaluations correct.\n")
    
    # Test 3: Safety - Block dangerous code
    print("[TEST 3] Safety (Block Dangerous Expressions)...")
    result, err = calc.evaluate("__import__('os').system('dir')")
    assert result is None
    assert err is not None
    print(f"  __import__ blocked: {err}")
    
    result, err = calc.evaluate("open('file.txt')")
    assert result is None
    print(f"  open() blocked: {err}")
    print("  [PASS] Dangerous expressions correctly blocked.\n")
    
    # Test 4: End-to-end
    print("[TEST 4] End-to-End Process...")
    answer = calc.process("Calculate 123 * 456")
    assert "56088" in answer
    print(f"  Input: 'Calculate 123 * 456' -> {answer}")
    
    answer = calc.process("Hello there")
    assert answer is None
    print(f"  Input: 'Hello there' -> None (correctly ignored)")
    print("  [PASS] End-to-end pipeline works.\n")

def test_dream_engine():
    print("=" * 60)
    print("  PHASE 29 VERIFICATION: The Imagination Engine")
    print("=" * 60 + "\n")
    
    from arinn_core.dream import DreamWeaver  # type: ignore
    
    # Test without hive (standalone mode)
    print("[TEST 1] Dream Generation (Standalone, no Hive)...")
    dreamer = DreamWeaver(hive=None)
    
    dream = dreamer.generate_dream()
    assert len(dream) > 5, f"Dream too short: '{dream}'"
    print(f"  Generated dream: {dream[:100]}...")
    print("  [PASS] LLM dream generation works.\n")
    
    # Test REM cycle (short, 3 seconds)
    print("[TEST 2] REM Sleep Cycle (3s, no broadcast)...")
    count = dreamer.enter_rem_cycle(duration=3.0, broadcast=False)
    assert count >= 1, "No dreams generated during REM!"
    print(f"  Dreams generated: {count}")
    
    journal = dreamer.get_journal()
    assert len(journal) == count
    print(f"  Journal entries: {len(journal)}")
    print("  [PASS] REM cycle generates and logs dreams.\n")

if __name__ == "__main__":
    test_calculator()
    test_dream_engine()
    
    print("=" * 60)
    print("  ALL TESTS PASSED. Phase 29 & 54 Verified.")
    print("=" * 60)
