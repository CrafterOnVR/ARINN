import os
import sys
import time
import subprocess
import re
import random
import datetime
import traceback
from typing import Optional

class AutoresearchAgent:
    """
    Implements Phase 84: The Autoresearch Protocol.
    Uses deterministic mutation strategies to evolve hyperparameters
    in train_amd.py, since the local LLM (distilgpt2) is too small
    to reliably generate valid Python code.
    
    Loop:
    1. Read train_amd.py
    2. Apply a random hyperparameter mutation
    3. Run the training loop (fixed 5-minute budget)
    4. Evaluate val_bpb
    5. Keep (git commit) or revert via Git
    """
    # Mutable hyperparameters and their valid ranges
    MUTATIONS = {
        "DEPTH": {"line_pattern": r"^DEPTH\s*=\s*(\d+)", "type": "int", "choices": [2, 3, 4, 6, 8]},
        "MODEL_DIM": {"line_pattern": r"^MODEL_DIM\s*=\s*(\d+)", "type": "int", "choices": [128, 192, 256, 384, 512]},
        "NUM_HEADS": {"line_pattern": r"^NUM_HEADS\s*=\s*(\d+)", "type": "int", "choices": [2, 4, 8]},
        "TOTAL_BATCH_SIZE": {"line_pattern": r"^TOTAL_BATCH_SIZE\s*=\s*.+", "type": "literal", "choices": ["2**14", "2**15", "2**16", "2**17"]},
        "DEVICE_BATCH_SIZE": {"line_pattern": r"^DEVICE_BATCH_SIZE\s*=\s*(\d+)", "type": "int", "choices": [8, 16, 32, 64]},
        "LEARNING_RATE": {"line_pattern": r"^LEARNING_RATE\s*=\s*[\d\.e\-]+", "type": "float", "choices": [1e-4, 2e-4, 3e-4, 5e-4, 8e-4, 1e-3]},
        "WARMUP_STEPS": {"line_pattern": r"^WARMUP_STEPS\s*=\s*(\d+)", "type": "int", "choices": [5, 10, 20, 30, 50]},
        "WEIGHT_DECAY": {"line_pattern": r"^WEIGHT_DECAY\s*=\s*[\d\.]+", "type": "float", "choices": [0.0, 0.01, 0.05, 0.1, 0.2]},
    }

    def __init__(self, repo_dir):
        self.repo_dir = repo_dir
        self.train_file = os.path.join(self.repo_dir, 'train_amd.py')
        self.results_file = os.path.join(self.repo_dir, 'results.tsv')
        self.current_branch: Optional[str] = None

    def initialize_experiment(self, tag=None):
        if tag is None:
            tag = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_branch = f"autoresearch/{tag}"
        print(f"[AUTORESEARCH] Initializing experiment branch: {self.current_branch}")
        
        subprocess.run(["git", "stash"], cwd=self.repo_dir, capture_output=True)
        subprocess.run(["git", "checkout", "master"], cwd=self.repo_dir, capture_output=True)
        
        res = subprocess.run(["git", "checkout", "-b", str(self.current_branch)], cwd=self.repo_dir, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[AUTORESEARCH] Failed to create branch: {res.stderr}")
            return False

        if not os.path.exists(self.results_file):
            with open(self.results_file, 'w') as f:
                f.write("commit\tval_bpb\tmemory_gb\tstatus\tdescription\n")
        return True

    def propose_changes(self, current_code, previous_results_summary=""):
        """
        Applies a random hyperparameter mutation to train_amd.py.
        Returns (new_code, description) or (None, None) on failure.
        """
        # Pick a random hyperparameter to mutate
        param_name = random.choice(list(self.MUTATIONS.keys()))
        mutation = self.MUTATIONS[param_name]
        new_value = random.choice(mutation["choices"])
        
        # Find and replace the line in the code
        pattern = mutation["line_pattern"]
        match = re.search(pattern, current_code, re.MULTILINE)
        
        if not match:
            print(f"[AUTORESEARCH] Could not find {param_name} in code. Skipping.")
            return None, None
        
        old_line = match.group(0)
        
        # Format the new value
        if mutation["type"] == "int":
            new_line = f"{param_name} = {new_value}"
        elif mutation["type"] == "float":
            new_line = f"{param_name} = {new_value}"
        elif mutation["type"] == "literal":
            new_line = f"{param_name} = {new_value}"
        
        # Ensure MODEL_DIM is divisible by NUM_HEADS
        if param_name == "MODEL_DIM":
            # Read current NUM_HEADS
            heads_match = re.search(r"^NUM_HEADS\s*=\s*(\d+)", current_code, re.MULTILINE)
            if heads_match:
                num_heads = int(heads_match.group(1))
                if new_value % num_heads != 0:
                    # Round to nearest valid value
                    new_value = (new_value // num_heads) * num_heads
                    if new_value == 0:
                        new_value = num_heads
                    new_line = f"{param_name} = {new_value}"
        
        if param_name == "NUM_HEADS":
            dim_match = re.search(r"^MODEL_DIM\s*=\s*(\d+)", current_code, re.MULTILINE)
            if dim_match:
                model_dim = int(dim_match.group(1))
                if model_dim % new_value != 0:
                    # Pick the nearest valid head count
                    valid_heads = [h for h in mutation["choices"] if model_dim % h == 0]
                    if valid_heads:
                        new_value = random.choice(valid_heads)
                        new_line = f"{param_name} = {new_value}"
                    else:
                        return None, None
        
        description = f"Mutate {param_name}: {old_line.strip()} -> {new_line.strip()}"
        new_code = current_code.replace(old_line, new_line, 1)
        
        print(f"[AUTORESEARCH] {description}")
        return new_code, description

    def run_experiment(self, description):
        print(f"[AUTORESEARCH] Running experiment: {description}")
        
        subprocess.run(["git", "add", "train_amd.py"], cwd=self.repo_dir)
        subprocess.run(["git", "commit", "-m", description], cwd=self.repo_dir)
        
        commit_hash = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=self.repo_dir, capture_output=True, text=True).stdout.strip()
        
        log_file_path = os.path.join(self.repo_dir, 'run.log')
        try:
             # Prefer Python 3.12 venv with DirectML for AMD GPU
             venv312 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".venv312", "Scripts", "python.exe")
             python_exe = venv312 if os.path.exists(venv312) else sys.executable
             with open(log_file_path, "w") as log_file:
                 subprocess.run([python_exe, "train_amd.py"], cwd=self.repo_dir, stdout=log_file, stderr=subprocess.STDOUT, timeout=660)
        except subprocess.TimeoutExpired:
             print("[AUTORESEARCH] Run timed out (>11 mins).")
             return commit_hash, 0.0, 0.0, "crash (timeout)"
        except Exception as e:
             print(f"[AUTORESEARCH] Run failed immediately: {e}")
             return commit_hash, 0.0, 0.0, "crash (exception)"
             
        return self.parse_results(log_file_path, commit_hash)
        
    def parse_results(self, log_file, commit_hash):
        if not os.path.exists(log_file):
            return commit_hash, 0.0, 0.0, "crash (no log)"
            
        val_bpb = 0.0
        peak_vram_mb = 0.0
        
        with open(log_file, 'r') as f:
            content = f.read()
            
        bpb_match = re.search(r"^val_bpb:\s+([0-9\.]+)", content, re.MULTILINE)
        if bpb_match:
            val_bpb = float(bpb_match.group(1))
            
        vram_match = re.search(r"^peak_vram_mb:\s+([0-9\.]+)", content, re.MULTILINE)
        if vram_match:
            peak_vram_mb = float(vram_match.group(1))
        
        # Check for FAIL or error markers
        if "FAIL" in content or "Traceback" in content:
            return commit_hash, val_bpb, round(float(peak_vram_mb / 1024)), "crash" # pyre-ignore
            
        memory_gb = round(float(peak_vram_mb / 1024)) # pyre-ignore
        
        if val_bpb == 0.0:
            return commit_hash, val_bpb, memory_gb, "crash"
        return commit_hash, val_bpb, memory_gb, "completed"

    def read_best_score(self):
        best_bpb = float('inf')
        if not os.path.exists(self.results_file):
             return best_bpb
             
        with open(self.results_file, 'r') as f:
            lines = f.readlines()[1:] # pyre-ignore
            for line in lines:
                parts = line.strip().split('\t')
                if len(parts) >= 4 and parts[3] == 'keep':
                    try:
                        val = float(parts[1])
                        if 0 < val < best_bpb:
                            best_bpb = val
                    except ValueError:
                        pass
        return best_bpb

    def log_result(self, commit, val_bpb, memory_gb, status, description):
        with open(self.results_file, 'a') as f:
            f.write(f"{commit}\t{val_bpb:.6f}\t{memory_gb:.1f}\t{status}\t{description}\n")

    def execution_loop(self, max_iterations=20):
        if not self.initialize_experiment():
            print("[AUTORESEARCH] Initialization failed. Aborting.")
            return

        print("[AUTORESEARCH] --- Establishing Baseline ---")
        best_bpb = self.read_best_score()
        
        if best_bpb == float('inf'):
            print("[AUTORESEARCH] Running initial baseline experiment.")
            commit, val_bpb, memory_gb, status = self.run_experiment("baseline")
            if status == "completed":
                status = "keep"
                best_bpb = val_bpb
            self.log_result(commit, val_bpb, memory_gb, status, "baseline")
        else:
            print(f"[AUTORESEARCH] Baseline already exists. Current best val_bpb: {best_bpb}")

        recent_history: list[str] = []
        consecutive_crashes: int = 0
        
        for i in range(max_iterations):
            print(f"\n[AUTORESEARCH] === Iteration {i+1}/{max_iterations} ===")
            
            with open(self.train_file, 'r') as f:
                current_code = f.read()
            
            new_code, desc = self.propose_changes(current_code, "\n".join(recent_history[-5:])) # pyre-ignore
            
            if not new_code:
                print("[AUTORESEARCH] Failed to generate valid mutation. Retrying.")
                continue
                
            with open(self.train_file, 'w') as f:
                f.write(new_code)
                
            commit, val_bpb, memory_gb, status = self.run_experiment(desc)
            
            if status == "crash":
                 consecutive_crashes += 1 # pyre-ignore
                 print(f"[AUTORESEARCH] Run crashed ({consecutive_crashes} consecutive). Reverting '{desc}'.")
                 self.log_result(commit, val_bpb, memory_gb, "crash", desc)
                 subprocess.run(["git", "reset", "--hard", "HEAD~1"], cwd=self.repo_dir)
                 recent_history.append(f"Tried: {desc} -> Result: CRASHED")
                 
                 if consecutive_crashes >= 5:
                     print("[AUTORESEARCH] Too many consecutive crashes. Aborting loop.")
                     break
                 continue
            
            consecutive_crashes = 0  # Reset on success
                 
            if val_bpb < best_bpb and val_bpb > 0:
                 print(f"[AUTORESEARCH] SUCCESS! New best score: {val_bpb:.6f} (was {best_bpb:.6f}). Keeping changes.")
                 best_bpb = val_bpb
                 self.log_result(commit, val_bpb, memory_gb, "keep", desc)
                 recent_history.append(f"Tried: {desc} -> Result: IMPROVED (val_bpb: {val_bpb:.6f})")
            else:
                 print(f"[AUTORESEARCH] Failed to improve. Score: {val_bpb:.6f} (best: {best_bpb:.6f}). Reverting.")
                 self.log_result(commit, val_bpb, memory_gb, "discard", desc)
                 subprocess.run(["git", "reset", "--hard", "HEAD~1"], cwd=self.repo_dir)
                 recent_history.append(f"Tried: {desc} -> Result: WORSE (val_bpb: {val_bpb:.6f})")
                 
        print(f"\n[AUTORESEARCH] Loop finished. Best val_bpb achieved: {best_bpb}")
        print(f"[AUTORESEARCH] Results logged in: {self.results_file}")
