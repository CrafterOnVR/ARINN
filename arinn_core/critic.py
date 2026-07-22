
import os
import subprocess
import time
from arinn_core.cortex import SiliconCortex
from arinn_core.hydra import HydraProtocol

class CodeRepairEngine:
    """
    Phase 57: The Critic Protocol (System 2).
    Generates, Tests, and Fixes code in a loop.
    """
    def __init__(self, max_retries=3):
        self.cortex = SiliconCortex()
        self.hydra = HydraProtocol()
        self.max_retries = max_retries

    def generate_and_refine(self, project_name, description):
        print(f"\n[CRITIC] Task: Create '{project_name}' - {description}")
        
        # Initial Attempt (System 1 - Fast)
        print("[CRITIC] Attempt 1 (Intuition)...")
        self.hydra.spawn_project(project_name, description)
        
        project_path = os.path.join(self.hydra.gen_root, project_name)
        main_py = os.path.join(project_path, "main.py")
        
        if not os.path.exists(main_py):
            print("[CRITIC] Critical Error: File not created.")
            return False

        # Refinement Loop (System 2 - Slow)
        for i in range(self.max_retries):
            print(f"[CRITIC] Testing Attempt {i+1}...")
            success, error = self.run_test(main_py)
            
            if success:
                print(f"[CRITIC] Success! Code works on Attempt {i+1}.")
                return True
            else:
                print(f"[CRITIC] Failure. Error: {error.strip()[:100]}...") # Truncate log
                
                # The Fix (Feedback Loop)
                print(f"[CRITIC] Thinking (Refining)...")
                
                # Since Cortex.generate_thought is limited by distilgpt2 context, 
                # we use a very targeted prompt.
                # In a real LLM, we'd feed the whole code + error.
                # Here, we just ask for the specific correction.
                
                # Heuristic Fix: Make it a completion task
                fix_prompt = f"The previous code failed with: {error}\nWrite the corrected full Python script for {description}. Return only code."
                raw_output = self.cortex.generate_thought(fix_prompt, max_length=300)
                
                # Clean up the generation (Chat Model Heuristic)
                lines = raw_output.split('\n')
                clean_lines = []
                capture = False
                
                for line in lines:
                    if "```" in line and "python" in line:
                        capture = True
                        continue
                    if "```" in line and capture:
                        capture = False
                        continue
                    if line.strip().startswith("import ") or line.strip().startswith("from ") or line.strip().startswith("def ") or line.strip().startswith("class ") or line.strip().startswith("if __name__"):
                        capture = True
                    
                    if capture or line.startswith("    ") or line.strip().startswith("#"):
                        clean_lines.append(line)
                        
                if not clean_lines:
                    # Fallback
                    clean_lines = [l for l in lines if not ("Here" in l or "Sure" in l)]

                full_code = "# Attempt {i+2} (Refined)\n" + "\n".join(clean_lines)
                
                with open(main_py, "w") as f:
                    f.write(full_code)
                    
        print("[CRITIC] Exhausted all retries. The problem is too hard.")
        return False

    def run_test(self, script_path):
        try:
            # Sandbox: Run with timeout
            # We assume a successful script exits with 0 and prints something?
            # Or just doesn't crash.
            result = subprocess.run(
                ["python", script_path], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except subprocess.TimeoutExpired:
            return False, "Timeout: Infinite Loop Detected."
        except Exception as e:
            return False, str(e)

if __name__ == "__main__":
    clinic = CodeRepairEngine()
    # Hard Test: "Write a script that prints the first 5 primes" 
    # (distilgpt2 often messes up the 'for' loop syntax)
    clinic.generate_and_refine("Clinic_Test", "print first 5 prime numbers")
