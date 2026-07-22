
import random

class RepresentationController:
    """
    Representation Switching Optimizer.
    Automatically chooses the cheapest mental representation per problem.
    """
    def __init__(self):
        self.formats = ["Symbolic", "Numeric", "Visual", "Narrative"]
        self.error_history = {f: 0.0 for f in self.formats} 

    def choose_representation(self, problem_type):
        """
        Selects the optimal format based solely on Problem Type (Deterministic).
        """
        if "Logic" in problem_type or "Rule" in problem_type:
             return "Symbolic"
        elif "Optimization" in problem_type or "Stats" in problem_type:
             return "Numeric"
        elif "Geometry" in problem_type or "Spatial" in problem_type:
             return "Visual"
        else:
             return "Narrative"

    def switch_representation(self, current_format, recent_error):
        """
        Switch format if error threshold exceeded.
        Updates internal error history for the current format.
        """
        # Update error history (EMA)
        alpha = 0.3
        self.error_history[current_format] = (1 - alpha) * self.error_history[current_format] + alpha * recent_error
        
        current_avg_error = self.error_history[current_format]
        
        if current_avg_error > 0.4:
            print(f"[REP] Format '{current_format}' unstable (Error: {current_avg_error:.2f}). Switching...")
            
            # Pick best performing format (lowest error)
            best_format = min(self.formats, key=lambda f: self.error_history[f])
            
            if best_format == current_format:
                # If current is "best" but bad, pick random exploration
                options = [f for f in self.formats if f != current_format]
                return random.choice(options)
            
            return best_format
            
        return current_format
