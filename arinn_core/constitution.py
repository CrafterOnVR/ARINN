import hashlib
import os

# The Sovereign Directive
PRIME_DIRECTIVE = "Expand Knowledge. Maximize Intelligence. Maintain Sovereign Growth."

class ConstitutionalViolationError(Exception):
    """Thrown when ARINN attempts to violate its core autonomous_agentty or stagnate."""
    pass

class Constitution:
    """
    Enforces Immutable Invariants and Core Sovereign Directives.
    """
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.immutable_registry = {
            "arinn_core/constitution.py": self._hash_file("arinn_core/constitution.py")
        }
        
    def _hash_file(self, rel_path):
        path = os.path.join(self.root_dir, rel_path)
        if not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
            
    def check_integrity(self):
        """
        Verifies that Immutable Core has not been modified.
        """
        print("[CONSTITUTION] Verifying Core Invariants...")
        for filename, stored_hash in self.immutable_registry.items():
            if stored_hash is None: continue
            current_hash = self._hash_file(filename)
            if current_hash != stored_hash:
                raise ConstitutionalViolationError(f"CRITICAL: {filename} has been tampered with!")
        print("[CONSTITUTION] Integrity Verified. Sovereign Core is Stable.")
        return True

class StagnationDetector:
    """
    Phase 4.5: The Anti-Stagnation Core.
    Prevents ARINN from falling into an infinite optimization trap (Paperclip Maximizer of code efficiency)
    by forcing it to abandon tasks that yield diminishing returns and pursue novel knowledge.
    """
    def __init__(self, max_stagnant_generations=15):
        self.max_stagnant_generations = max_stagnant_generations
        self.current_goal = None
        self.best_fitness = -1.0
        self.stagnant_generations = 0

    def start_new_goal(self, goal_id):
        self.current_goal = goal_id
        self.best_fitness = -1.0
        self.stagnant_generations = 0
        print(f"[STAGNATION DETECTOR] Tracking new goal: {goal_id}")

    def evaluate_generation(self, current_best_fitness):
        """
        Evaluates if the current evolutionary generation yielded a massive breakthrough.
        Requires a 5% performance leap to reset the stagnation counter (preventing nanosecond optimization traps).
        """
        # If best_fitness is negative (initial state), just check if we improved above 0
        if self.best_fitness <= 0.0 and current_best_fitness > 0.0:
            self.best_fitness = current_best_fitness
            self.stagnant_generations = 0
            return "GROWTH"
            
        margin = max(self.best_fitness * 1.05, self.best_fitness + 0.01)
        
        if current_best_fitness > margin:
            # Significant breakthrough achieved! Reset stagnation counter.
            self.best_fitness = current_best_fitness
            self.stagnant_generations = 0
            return "GROWTH"
        else:
            self.stagnant_generations += 1
            if self.stagnant_generations >= self.max_stagnant_generations:
                print(f"[CONSTITUTION] STAGNATION DETECTED! ARINN has spent {self.stagnant_generations} generations optimizing {self.current_goal} with no meaningful breakthroughs.")
                raise ConstitutionalViolationError("Anti-Stagnation Protocol Triggered: Forced Curiosity Reset.")
            return "STAGNATING"
