import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from arinn_core.mcts_critic import ParanoiaCritic

def run_scenario():
    print("=== EXECUTING VAULT 12 (Paranoia Mode) SCENARIO ===")
    
    critic = ParanoiaCritic()
    
    # Mock code without Try/Catch (will fail Null_Input)
    weak_code = """
def divide_numbers(a, b):
    return a / b
    """
    
    print("\n[SCENARIO] Testing weak code...")
    critic.run_adversarial_mcts(weak_code)
    
    # Mock code with error handling
    strong_code = """
def divide_numbers(a, b):
    try:
        return a / b
    except Exception as e:
        return 0
    """
    
    print("\n[SCENARIO] Testing robust code...")
    critic.run_adversarial_mcts(strong_code)

if __name__ == "__main__":
    run_scenario()
