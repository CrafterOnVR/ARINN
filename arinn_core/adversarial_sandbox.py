import os
import subprocess
import tempfile
import time

class AdversarialCrucible:
    """
    Phase 4: Adversarial Self-Play Sandbox.
    Grades mutated code strictly on execution speed (King of the Hill) using isolated subprocesses
    to guarantee ARINN cannot get trapped in infinite loop execution lockups.
    """
    def __init__(self, property_test_code: str):
        self.property_test_code = property_test_code

    def execute_and_score(self, source_code: str) -> float:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "eval.py")
            
            # The property_test_code must execute the physics test and print ONLY the microsecond score
            # or print "FAIL" if it did not sort correctly.
            full_code = source_code + "\n\n" + self.property_test_code
            
            with open(file_path, "w") as f:
                f.write(full_code)
                
            try:
                # 15 second absolute timeout limit
                result = subprocess.run(
                    ["python", file_path], 
                    capture_output=True, 
                    text=True, 
                    timeout=15.0 
                )
                
                output = result.stdout.strip()
                
                if result.returncode != 0 or "FAIL" in output:
                    return 0.1 # Failed the mathematical logic test
                    
                exec_time = float(output)
                if exec_time <= 0.0:
                    exec_time = 0.000001
                    
                fitness = 10.0 + (1.0 / exec_time)
                return fitness
                
            except subprocess.TimeoutExpired:
                return 0.0 # Caught an infinite loop!
            except ValueError:
                return 0.1 # Printed something weird
            except Exception:
                return 0.0 # Hard crash
