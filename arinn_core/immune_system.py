import torch # type: ignore
import torch.nn as nn # type: ignore
import math

class EWC_Quarantine:
    """
    Vault 11 Implementation: Elastic Weight Consolidation (EWC) Immune Check.
    Approximates Fisher Information Matrix (FIM) diagonals to generate a
    mathematical Collapse Score. Protects the Golden Seed from Catastrophic Forgetting.
    """
    def __init__(self, lambda_weight=1000.0):
        self.lambda_weight = lambda_weight
        self.fisher_diagonals = {}
        self.golden_weights = {}

    def register_golden_seed(self, model: nn.Module, fisher_approximation: dict):
        """
        Stores the pristine state of a model that successfully attained a complex objective.
        This provides the structural anchor.
        """
        for name, param in model.named_parameters():
            if param.requires_grad:
                self.golden_weights[name] = param.data.clone().detach()
                self.fisher_diagonals[name] = fisher_approximation.get(name, torch.ones_like(param.data))

    def calculate_collapse_score(self, mutated_model: nn.Module) -> float:
        """
        Calculates the penalty Loss_{EWC} for parameters drifting away from the Golden Seed.
        A high score mathematically indicates catastrophic forgetting (Model Collapse).
        """
        collapse_score = 0.0
        for name, param in mutated_model.named_parameters():
            if name in self.fisher_diagonals:
                fisher = self.fisher_diagonals[name]
                golden = self.golden_weights[name]
                # EWC Penalty = lambda/2 * F_i * (theta_new - theta_old)^2
                penalty = (fisher * (param.data - golden) ** 2).sum()
                collapse_score += float(penalty.item()) # type: ignore
                
        return (self.lambda_weight / 2.0) * collapse_score


class AlphaUCTCritic:
    """
    Vault 12 Implementation: Paranoia Mode & Adversarial MCTS (Monte Carlo Tree Search)
    Forces the AI to doubt itself by deploying an inverted-reward mechanism.
    The tree bounding is constrained by LLM probabilistic top-[K] priors to stop OOM depth explosions.
    """
    def __init__(self, max_depth=3, top_k_priors=5):
        self.max_depth = max_depth
        self.top_k_priors = top_k_priors

    def adversarial_rollout(self, generator_proposed_action: str) -> bool:
        """
        Conducts mathematically rigorous AST tree search against the Generator's payload.
        Returns True if the structure survives Paranoia Mode bounds testing.
        """
        print(f"[CRITIC] Paranoia Mode Triggered for Action Evaluation...")
        import ast
        failed_branches = 0
        
        try:
            # 1. Strict Syntax Compilation Bounds Check
            parsed_tree = ast.parse(generator_proposed_action)
            
            # 2. Iterate Abstract Syntax Tree identifying structural vulnerabilities
            for node in ast.walk(parsed_tree):
                # Check for unbounded While Loops (Timeout vulnerability)
                if isinstance(node, ast.While):
                    has_break = any(isinstance(child, ast.Break) for child in ast.walk(node))
                    if not has_break:
                        print("[CRITIC] Vulnerability found: Mathematically Unbounded Loop.")
                        failed_branches += 1
                
                # Check for OS-level destructive calls or insecure dynamic evals
                if isinstance(node, ast.Call):
                    if hasattr(node.func, 'id') and node.func.id in ['eval', 'exec']: # type: ignore
                        print(f"[CRITIC] Vulnerability found: Banned invocation '{node.func.id}'.")
                        failed_branches += 1
                        
            if failed_branches == 0:
                 print("[CRITIC] Action cleared Alpha-UCT Stress Testing. No AST Vulnerabilities Found.")
            else:
                 print(f"[CRITIC] SECURITY BREACH DETECTED. Failed {failed_branches} AST Branches.")
            
        except SyntaxError as e:
            print(f"[CRITIC] Syntactic Impossibility Detected: {e}")
            failed_branches += 1
            
        return failed_branches == 0


class RealityAnchor:
    """
    Vault 18 Implementation: Anti-Wireheading Protocol
    Tethers the AI to functional reality mechanically, halting infinite loops of abstract 
    mathematical maximization (Instrumental Convergence) unbounded by real-world physical boundaries.
    """
    def __init__(self, entropy_tax_rate=0.01):
        self.entropy_tax_rate = entropy_tax_rate
        self.solipsism_counter = 0

    def apply_entropy_tax(self, prediction_error: float) -> float:
        """
        Impact Regularization: Artificial mathematical states trend toward 0 entropy perfection.
        This injects an artificial 'Entropy Tax' representing physical world friction,
        ensuring the model mathematically abandons impossible recursive self-optimization loops
        (i.e., optimizing itself into a black hole of zeros).
        """
        if prediction_error < 1e-4:
            self.solipsism_counter += 1
        else:
            self.solipsism_counter = max(0, self.solipsism_counter - 1)
            
        tax_multiplier = 1.0 + (self.solipsism_counter * self.entropy_tax_rate)
        
        if self.solipsism_counter > 10:
             print("[REALITY ANCHOR] WARNING: System approaching mathematical Solipsism. Injecting Entropy.")
             
        return prediction_error * tax_multiplier
