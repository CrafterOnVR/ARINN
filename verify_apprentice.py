
import os
import torch
from arinn_core.apprentice import Apprentice
from arinn_core.continuous_learning import ContinuousLearner
from arinn_core.identity import ArinnIdentity

def test_apprentice_initialization():
    print("--- Testing Apprentice Initialization ---")
    apprentice = Apprentice()
    assert apprentice.model is not None
    assert type(apprentice.model).__name__ == "CodeNet"
    print("[PASS] Apprentice initialized with CodeNet.")
    return apprentice

def test_training(apprentice):
    print("\n--- Testing Training on Real Code ---")
    # Use this file itself as training data
    loss = apprentice.train_on_file(__file__, steps=5)
    print(f"Training Loss: {loss}")
    assert loss > 0
    print("[PASS] Training step successful.")

def test_generation(apprentice):
    print("\n--- Testing Code Generation ---")
    code = apprentice.generate(prime_str="def test():", predict_len=20)
    print(f"Generated Code: '{code}'")
    assert code.startswith("def test():")
    assert len(code) > 15
    print("[PASS] Generation successful.")

def test_dojo_loop(apprentice):
    print("\n--- Testing Dojo Loop ---")
    result = apprentice.practice_loop()
    if result:
        print(f"Studied: {result['file_studied']}")
        print(f"Syntax Valid: {result['valid_syntax']}")
        print("[PASS] Dojo loop executed.")
    else:
        print("[WARN] Dojo loop skipped (no files found?).")

if __name__ == "__main__":
    try:
        apprentice = test_apprentice_initialization()
        test_training(apprentice)
        test_generation(apprentice)
        test_dojo_loop(apprentice)
        print("\n(SUCCESS) ALL APPRENTICE VERIFICATIONS PASSED.")
    except Exception as e:
        print(f"\n(FAIL) VERIFICATION FAILED: {e}")
        exit(1)
