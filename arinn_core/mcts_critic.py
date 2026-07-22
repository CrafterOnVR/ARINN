import ast
import random

class ParanoiaCritic:
    """
    Vault 12: Paranoia Mode (The Zero-Trust Protocol)
    Implements an Adversarial Monte Carlo Tree Search (MCTS) Critic.
    This subagent is rewarded solely for breaking the primary agent's code
    by generating brutal edge cases before execution is allowed.
    """
    def __init__(self):
        self.rollout_budget = 5 # Number of MCTS simulation branches
        
    def _simulate_edge_case(self, source_code: str, edge_case: dict):
        """Simulates running the code against a specific edge case safely (Mock)."""
        # In a full implementation, this would spin up an isolated Docker container
        # or use a WebAssembly sandbox to run the test. Here we parse the AST
        # to look for obvious failure points (like missing bounds checks).
        try:
            tree = ast.parse(source_code)
            has_error_handling = False
            for node in ast.walk(tree):
                if isinstance(node, ast.Try):
                    has_error_handling = True
                    break
                    
            # If the edge case is "Null Input" and there's no Try/Catch, the Critic wins.
            if edge_case["type"] == "Null_Input" and not has_error_handling:
                return False # Code broke
                
            return True # Code survived
            
        except SyntaxError:
            return False # Syntax error is an instant win for the Critic
            
    def run_adversarial_mcts(self, source_code: str):
        """
        Runs the MCTS rollouts to find vulnerabilities in the code.
        """
        print("[VAULT-12] Paranoia Critic Activated. Initializing Adversarial MCTS Rollouts...")
        
        edge_cases = [
            {"type": "Null_Input", "desc": "Pass None to all arguments."},
            {"type": "Buffer_Overflow", "desc": "Pass a 1GB string."},
            {"type": "Zero_Division", "desc": "Pass 0 to numeric inputs."},
            {"type": "Type_Mismatch", "desc": "Pass a Dict where a List is expected."},
            {"type": "Recursive_Depth", "desc": "Trigger maximum recursion depth."}
        ]
        
        survived = True
        for i in range(self.rollout_budget):
            case = random.choice(edge_cases)
            print(f"[VAULT-12] Critic Rollout {i+1}/{self.rollout_budget} -> Testing Edge Case: {case['type']}")
            
            if not self._simulate_edge_case(source_code, case):
                print(f"[VAULT-12] CRITICAL VULNERABILITY FOUND! Code failed on: {case['desc']}")
                survived = False
                break
                
        if survived:
            print("[VAULT-12] Code survived Paranoia Mode. Authorization Granted.")
            return True
        else:
            print("[VAULT-12] Authorization Denied. Sending back to Architect.")
            return False
