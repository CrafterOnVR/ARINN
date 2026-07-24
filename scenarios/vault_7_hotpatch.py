import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from arinn_core.live_patching import ImmortalCodebase

def broken_function():
    return "I am a broken string and I have a bug."

def synthesized_fix():
    return "I am the fixed string. The bug has been eradicated."

def run_scenario():
    print("=== EXECUTING VAULT 7 (Semantic Self-Healing) SCENARIO ===")
    
    codebase = ImmortalCodebase()
    
    print(f"Pre-Patch Output: {broken_function()}")
    
    # Hot swap the __code__ pointer of the broken function
    success = codebase.hot_swap_function(broken_function, synthesized_fix)
    
    if success:
        print(f"Post-Patch Output: {broken_function()}")

if __name__ == "__main__":
    run_scenario()
