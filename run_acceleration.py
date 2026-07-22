
"""
ARINN ACCELERATION LAUNCHER
Bypasses the CLI menu to immediately trigger the High-Leverage Acceleration Curriculum.
This allows the agent to start studying the 10 Core Axioms without manual intervention.
"""
import sys
import time

# Ensure we can import arinn_core
sys.path.append(".")

from arinn_core.identity import ArinnIdentity
from arinn_core.continuous_learning import ContinuousLearner

def start_acceleration():
    print("Initializing ARINN Identity...")
    identity = ArinnIdentity()
    learner = ContinuousLearner(identity)
    
    print("Launching Phase 12: Acceleration Curriculum...")
    try:
        # This loop will run until the user presses `
        learner.loop_acceleration_study()
    except KeyboardInterrupt:
        print("\nLearning interrupted by user.")
    except Exception as e:
        print(f"\nCritical Error during learning: {e}")

if __name__ == "__main__":
    start_acceleration()
