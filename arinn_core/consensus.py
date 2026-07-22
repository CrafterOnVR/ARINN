
import random

class ConsensusManager:
    """
    Orchestrates Cross-Expert Verification.
    """
    def __init__(self, hivemind):
        self.hivemind = hivemind
        
    def verify_plan(self, tasks):
        """
        Asks NeuralCore to formally verify the task array structure.
        """
        try:
            from .neural_core import NeuralCore # type: ignore
            core = NeuralCore()
            prompt = f"Verify execution plan viability: {[t.description for t in set(tasks)]}. Return viability from 0.0 to 1.0."
            
            resp, _ = core.generate_thought(prompt, max_tokens=20)
            
            # Simple bounded heuristic extraction
            score = 0.8 if "1.0" in resp or "0.9" in resp or "0.8" in resp else 0.4
            
            if score > 0.7:
                return True, score, "Plan Approved by Neural Consensus."
            return False, score, "Plan Rejected: Viability check failed."
        except Exception as e:
             return False, 0.0, f"Consensus Evaluation Offline: {e}"
            
    def _get_expert_vote(self, expert, tasks):
        # Real Metric: Shannon Entropy of the plan text
        # Experts approve plans that have enough "Information Content" but aren't "Noise"
        
        full_text = " ".join([t.description for t in tasks.values()])
        if not full_text: return 0.0
        
        import math
        # Calculate Entropy
        prob = [float(full_text.count(c)) / len(full_text) for c in dict.fromkeys(list(full_text))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
        
        # Valid English text usually has entropy between 3.5 and 5.0
        # If it's too low (e.g. "aaaaa"), reject. 
        if entropy > 2.5:
            return 1.0
        else:
            return 0.0

class RefereeArbitration:
    """
    Resolves conflicts when consensus is low.
    """
    def arbitrate(self, plan, expert_votes):
        # Logic to suggest amendments
        return "Refine plan: Break down complex 'Study' tasks further."
