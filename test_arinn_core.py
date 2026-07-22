
import sys
import os
import shutil
import time

# Ensure we can import modules
sys.path.append(os.getcwd())

try:
    from arinn_core.identity import ArinnIdentity, Phase
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def test_arinn_growth():
    print("Initializing ARINN Identity...")
    
    # Clean up state for fresh test
    if os.path.exists("bootloader_state.json"):
        os.remove("bootloader_state.json")
    if os.path.exists("arinn_brain.pth"):
        os.remove("arinn_brain.pth")
    if os.path.exists("arinn_secure_memory.enc"):
        os.remove("arinn_secure_memory.enc")
    
    arinn = ArinnIdentity()
    
    print(f"Initial Phase: {arinn.bootloader.current_phase.name}")
    
    # Run loop until operational
    max_steps = 20
    steps = 0
    while steps < max_steps:
        print(f"--- Step {steps + 1} ---")
        operational = arinn.wake_up()
        
        if operational:
            print("ARINN is FULLY OPERATIONAL!")
            break
            
        steps += 1
        time.sleep(0.5)

    if not operational:
        print("FAILED to reach operational state within max steps.")
    else:
        print("SUCCESS: ARINN grew up.")

    # Test autonomous choice
    choice = arinn.autonomous_choice(0.85)
    print(f"Choice at 85% mastery: {choice}")
    choice_master = arinn.autonomous_choice(0.95)
    print(f"Choice at 95% mastery: {choice_master}")
    choice_novice = arinn.autonomous_choice(0.50)
    print(f"Choice at 50% mastery: {choice_novice}")

if __name__ == "__main__":
    test_arinn_growth()
