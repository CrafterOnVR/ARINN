
import time
import os
import json

class KnowledgeTracker:
    """
    Tracks the velocity of knowledge acquisition.
    Metric: Knowledge Units per Second (KUPS).
    """
    def __init__(self):
        self.history = []
        self.start_time = time.time()
        self.total_gain = 0.0
        
    def log_gain(self, gain_amount):
        timestamp = time.time()
        self.history.append((timestamp, gain_amount))
        self.total_gain += gain_amount
        
        # Keep history short (last 100 events) for rolling average
        if len(self.history) > 100:
            self.history.pop(0)
            
    def get_velocity(self):
        """Returns KUPS (Knowledge Units Per Second) over last window."""
        if not self.history: return 0.0
        
        start = self.history[0][0]
        end = self.history[-1][0]
        duration = end - start
        
        if duration < 1.0: return 0.0
        
        window_gain = sum(x[1] for x in self.history)
        return window_gain / duration

class RecursiveOptimizer:
    """
    Dynamically adjusts system parameters to maximize velocity.
    """
    def __init__(self):
        self.params = {
            "learning_rate": 0.001,
            "batch_size": 32,
            "recursion_depth": 1
        }
        
    def optimize(self, current_velocity):
        """
        Adjusts parameters based on velocity feedback.
        """
        # Heuristic: If velocity is high, increase depth and batch size (Scale up)
        # If velocity is low, decrease to stabilize.
        
        if current_velocity > 1.0: # High speed threshold
            self.params["learning_rate"] *= 1.05
            self.params["batch_size"] = min(256, int(self.params["batch_size"] * 1.1))
            self.params["recursion_depth"] = min(10, self.params["recursion_depth"] + 1)
            return "SCALING_UP"
            
        elif current_velocity < 0.1: # Stalled
            self.params["learning_rate"] *= 0.9
            self.params["batch_size"] = max(1, int(self.params["batch_size"] * 0.9))
            self.params["recursion_depth"] = max(1, self.params["recursion_depth"] - 1)
            return "STABILIZING"
            
        return "MAINTAINING"

class SafetyLock:
    """
    Manual Override System.
    """
    def __init__(self, lock_file="manual_override.lock"):
        self.lock_file = lock_file
        
    def is_locked(self):
        return os.path.exists(self.lock_file)
        
    def engage_lock(self):
        with open(self.lock_file, "w") as f:
            f.write("OVERRIDE ENGAGED")
            
    def release_lock(self):
        if os.path.exists(self.lock_file):
            os.remove(self.lock_file)
