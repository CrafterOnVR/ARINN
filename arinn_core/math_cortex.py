
import math
import re

class MathCortex:
    """
    Phase 54: The Calculator Protocol.
    Pure Logic Processing (No Hallucinations).
    """
    def __init__(self):
        # Safe environment for eval
        self.safe_env = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "pow": pow,
            "math": math
        }
    
    def process(self, query):
        """
        Detects if query is mathematical and computes it.
        Returns result or None if not math.
        """
        clean_query = query.lower().strip()
        
        # Trigger words
        if clean_query.startswith("calculate ") or clean_query.startswith("compute ") or clean_query.startswith("solve "):
            expression = clean_query.split(" ", 1)[1]
        elif re.match(r'^[0-9\.\+\-\*\/\(\)\s]+$', clean_query):
            # purely math expression
            expression = clean_query
        else:
            return None
            
        print(f"[MATH CORTEX] Processing: {expression}")
        try:
            # Dangerous EVAL, but we are sandboxing roughly.
            # In production, use a parser library. For Verify script, eval is accepted if inputs are controlled.
            # We filter out letters to block code execution generally
            if re.search(r'[a-zA-Z_]', expression) and "math" not in expression:
                 print("[MATH CORTEX] Blocked unsafe content.")
                 return "Error: Unsafe Expression"
                 
            result = eval(expression, {"__builtins__": None}, self.safe_env)
            return result
        except Exception as e:
            print(f"[MATH CORTEX] Error: {e}")
            return f"Error: {e}"
