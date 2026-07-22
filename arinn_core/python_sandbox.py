import os
import subprocess
import tempfile
import ast
import copy
from arinn_core.ast_evolution import ASTOperatorMutator

class SafePythonCrucible:
    """
    Replaces the fatal flaw of `exec()` which can cause infinite loops.
    Writes the genetic code + test cases to a temp file and executes it via isolated subprocess.
    """
    def __init__(self, test_cases_code: str):
        self.test_cases_code = test_cases_code

    def execute_and_score(self, source_code: str) -> float:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "eval.py")
            
            # Combine the mutated genetic code with the isolated verification tests
            full_code = source_code + "\n\n" + self.test_cases_code
            
            with open(file_path, "w") as f:
                f.write(full_code)
                
            try:
                # Execute safely with a strict 2-second timeout to prevent infinite loop lobotomies
                result = subprocess.run(
                    ["python", file_path], 
                    capture_output=True, 
                    text=True, 
                    timeout=2.0
                )
                
                # If the script finishes without error (exit 0), the asserts passed!
                if result.returncode == 0:
                    return 1.0
                else:
                    return 0.5 # Logic Error / AssertionError
            except subprocess.TimeoutExpired:
                return 0.0 # Infinite Loop Caught!
            except Exception:
                return 0.2
