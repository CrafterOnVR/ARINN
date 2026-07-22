
import logging
from typing import Dict, List, Any
import time

class MetaOptimizer:
    """
    Optimizes learning strategies and hyperparameters based on performance metrics.
    Corresponds to Phase 7: Autonomous Meta-Efficiency.
    """
    
    def __init__(self):
        self.learning_rate = 0.01
        self.search_depth = "moderate" # options: shallow, moderate, deep
        self.decision_threshold = 0.85 # The dynamic 80/90 rule point
        
        # Metrics History
        self.knowledge_gain_history = []
        self.last_adjustment_time = time.time()
        
    def record_learning_session(self, initial_mastery: float, final_mastery: float, duration: float):
        """Records the outcome of a learning session to calculate velocity."""
        if duration <= 0: return
        
        gain = final_mastery - initial_mastery
        velocity = gain / duration # Mastery points per second
        
        self.knowledge_gain_history.append({
            "velocity": velocity,
            "params": {
                "lr": self.learning_rate,
                "depth": self.search_depth
            }
        })
        
        # Keep history manageable
        if len(self.knowledge_gain_history) > 50:
            self.knowledge_gain_history.pop(0)
            
        logging.info(f"[META] Recorded session. Velocity: {velocity:.4f}/s")
        
        self._optimize()

    def _optimize(self):
        """Analyze history and adjust parameters."""
        if len(self.knowledge_gain_history) < 5:
            return # Need more data
            
        recent_avg = sum(x['velocity'] for x in self.knowledge_gain_history[-5:]) / 5
        overall_avg = sum(x['velocity'] for x in self.knowledge_gain_history) / len(self.knowledge_gain_history)
        
        logging.info(f"[META] Analysis: Recent Vel={recent_avg:.4f} vs Overall={overall_avg:.4f}")
        
        # Simple Hill Climbing / Heuristic Logic
        if recent_avg < overall_avg * 0.9:
            logging.info("[META] Performance dropping. Attempting strategy shift.")
            self._shift_strategy()
        elif recent_avg > overall_avg * 1.1:
            logging.info("[META] Performance improving. Maintaining course.")

    def check_for_expansion_needs(self) -> bool:
        """
        Determines if the Hivemind needs physical expansion (more neurons).
        Triggers:
        1. Plateau: Recent velocity is consistently low/zero despite strategy shifts.
        2. Random Evolution: Small change during exploration.
        """
        if len(self.knowledge_gain_history) < 10: return False
        
        recent_vels = [x['velocity'] for x in self.knowledge_gain_history[-10:]]
        avg_vel = sum(recent_vels) / 10
        
        # 1. Plateau Detection (Stuck)
        # If velocity is very low (< 0.05) for 10 steps, we are stuck.
        if avg_vel < 0.05:
            logging.warning(f"[META] Learning Plateau detected (Avg Vel {avg_vel:.4f}). Requesting Neural Expansion.")
            return True
            
        # 2. Random Evolution (1% chance)
        import random
        if random.random() < 0.01:
            logging.info("[META] Triggering Random Evolutionary Expansion.")
            return True
            
        return False
            
    def _shift_strategy(self):
        """Randomly or heuristically adjust parameters to find better optima."""
        import random
        
        # Adjust Learning Rate
        if random.random() > 0.5:
            old_lr = self.learning_rate
            self.learning_rate *= random.choice([0.8, 1.2])
            self.learning_rate = max(0.001, min(0.1, self.learning_rate))
            logging.info(f"[META] Adjusted Learning Rate: {old_lr:.4f} -> {self.learning_rate:.4f}")
            
        # Adjust Search Depth
        if random.random() > 0.7:
             modes = ["shallow", "moderate", "deep"]
             old_depth = self.search_depth
             self.search_depth = random.choice(modes)
             logging.info(f"[META] Adjusted Search Depth: {old_depth} -> {self.search_depth}")

    def get_current_params(self) -> Dict[str, Any]:
        return {
            "learning_rate": self.learning_rate,
            "search_depth": self.search_depth,
            "decision_threshold": self.decision_threshold
        }
