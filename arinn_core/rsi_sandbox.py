import os
import shutil
import tempfile
import subprocess
import re
import random
from arinn_core.ast_evolution import GeneticCodeEngine

class RSICrucible:
    """
    Phase 6: The Recursive Self-Improvement Crucible.
    Takes a mutated brain module, isolates the entire project in a temporary sandbox,
    and grades its intelligence by making it solve the Daydreamer benchmark.
    """
    def __init__(self, project_root: str, target_file: str):
        self.project_root = project_root
        self.target_file = target_file # e.g. "arinn_core/ast_evolution.py"

    def execute_and_score(self, source_code: str) -> float:
        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. Clone the entire project into the isolated sandbox
            for item in os.listdir(self.project_root):
                if item in ['.git', '.venv', '__pycache__']:
                    continue
                s = os.path.join(self.project_root, item)
                d = os.path.join(temp_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
                    
            # 2. Inject the mutated brain module
            target_path = os.path.join(temp_dir, self.target_file)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(source_code)
                
            # 3. Force the mutated brain to run the Daydreamer Benchmark
            try:
                # 60 second absolute timeout for the entire evolutionary run
                result = subprocess.run(
                    ["python", "background_worker.py"], 
                    cwd=temp_dir,
                    capture_output=True, 
                    text=True, 
                    timeout=5.0 
                )
                
                if result.returncode != 0:
                    print(f"[RSI SANDBOX] Benchmark Crashed! stderr: {result.stderr}")
                    return 0.1 # The mutated brain crashed or threw an exception
                    
                # 4. Parse the intelligence score from the output
                match = re.search(r"Final Peak Fitness \(Speed Score\): (\d+\.\d+)", result.stdout)
                if match:
                    return float(match.group(1))
                else:
                    return 0.2 # Failed to complete the benchmark properly
                    
            except subprocess.TimeoutExpired:
                return 0.0 # The mutated brain got stuck in an infinite loop!
            except Exception:
                return 0.0
