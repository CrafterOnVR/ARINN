
import time
import random

class CostAccountant:
    """
    Tracks the 'True Cost' of learning.
    Metrics: Compute Time, Parameter Updates, Failed Attempts.
    Calculates ROI (Knowledge Gain / Cost).
    """
    def __init__(self):
        self.session_costs = {} # session_id -> {compute, updates, failures}
        
    def start_session(self, session_id):
        self.session_costs[session_id] = {
            "start_time": time.time(),
            "updates": 0,
            "failures": 0,
            "cost_score": 0.0
        }
        
    def log_update(self, session_id):
        if session_id in self.session_costs:
            self.session_costs[session_id]["updates"] += 1
            
    def log_failure(self, session_id):
        if session_id in self.session_costs:
            self.session_costs[session_id]["failures"] += 1
            
    def end_session(self, session_id, knowledge_gain):
        """Returns ROI score."""
        if session_id not in self.session_costs: return 0.0
        
        data = self.session_costs[session_id]
        duration = time.time() - data["start_time"]
        
        # Calculate Cost: Time + (Updates * 0.01) + (Failures * 0.5)
        cost = duration + (data["updates"] * 0.01) + (data["failures"] * 0.5)
        data["cost_score"] = cost
        
        roi = knowledge_gain / (cost + 1e-9) # Avoid div/0
        return roi

class CompressionEngine:
    """
    Compresses learned concepts into minimal representations.
    Merges redundant concepts and replaces facts with rules.
    """
    def compress_concept(self, original_data):
        """
        Compresses concept using ZLIB (Real Algorithmic Compression).
        Returns compressed_data (bytes), compression_ratio, retained_info (1.0 for lossless).
        """
        import zlib
        import pickle
        
        # Serialize first
        try:
            if isinstance(original_data, bytes):
                data_bytes = original_data
            else:
                data_bytes = pickle.dumps(original_data)
                
            original_size = len(data_bytes)
            compressed_bytes = zlib.compress(data_bytes, level=9)
            compressed_size = len(compressed_bytes)
            
            ratio = original_size / (compressed_size + 1e-9)
            
            return {
                "compressed": compressed_bytes,
                "ratio": ratio,
                "retained_power": 1.0 # Zlib is lossless
            }
        except Exception as e:
            print(f"Compression failed: {e}")
            return {
                "compressed": original_data,
                "ratio": 1.0,
                "retained_power": 1.0
            }

class StrategyOptimizer:
    """
    Strategy Darwinism.
    Maintains a population of learning strategies.
    Evolves them based on ROI feedback.
    """
    def __init__(self):
        self.strategies = {
            "brute_force": {"fitness": 0.2, "usage": 0},
            "heuristic_search": {"fitness": 0.5, "usage": 0},
            "causal_inference": {"fitness": 0.8, "usage": 0},
            "meta_learning": {"fitness": 0.7, "usage": 0}
        }
        
    def select_strategy(self):
        # Weighted random choice based on fitness
        candidates = list(self.strategies.keys())
        weights = [self.strategies[k]["fitness"] for k in candidates]
        return random.choices(candidates, weights=weights, k=1)[0]
        
    def update_fitness(self, strategy_name, roi_score):
        if strategy_name in self.strategies:
            strat = self.strategies[strategy_name]
            # Moving average
            strat["fitness"] = (strat["fitness"] * 0.8) + (roi_score * 0.2)
            strat["usage"] += 1
            
            # Deprecate if too low (Strategy Death)
            if strat["usage"] > 10 and strat["fitness"] < 0.1:
                print(f"[DARWIN] Strategy EXTINCT: {strategy_name}")
                del self.strategies[strategy_name]
