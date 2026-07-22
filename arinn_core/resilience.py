
import os
import shutil
import ast
import hashlib
import time
import logging

class AutoHealer:
    """
    18. Resilience & Self-Healing.
    Monitors core cognitive files for corruption and restores them.
    "Immortal Codebase"
    """
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.backups = {}
        self.snapshot()
        
    def snapshot(self):
        """Creates in-memory backup of valid files."""
        print("[HEALER] Taking tissue sample (Snapshotting code)...")
        for f in os.listdir(self.target_dir):
            if f.endswith(".py"):
                path = os.path.join(self.target_dir, f)
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        # Only backup if valid
                        ast.parse(content)
                        self.backups[f] = content
                except Exception as e:
                    logging.warning(f"Could not snapshot {f}: {e}")
                    
    def check_integrity(self):
        """Scans for brain damage (SyntaxErrors)."""
        damaged = []
        for f in self.backups.keys():
            path = os.path.join(self.target_dir, f)
            try:
                if not os.path.exists(path):
                    damaged.append(f)
                    continue
                    
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    ast.parse(content) # Check syntax
            except SyntaxError:
                damaged.append(f)
            except Exception:
                damaged.append(f) # Missing or unreadable
                
        return damaged
        
    def heal(self):
        """Restores damaged files."""
        start_t = time.time()
        damaged = self.check_integrity()
        if not damaged:
            return False, "System Healthy."
            
        print(f"[HEALER] DETECTED DAMAGE in: {damaged}. Initiating Rapid Reconstruction...")
        for f in damaged:
            path = os.path.join(self.target_dir, f)
            with open(path, 'w', encoding='utf-8') as file:
                file.write(self.backups[f])
                
        dt = time.time() - start_t
        return True, f"Repaired {len(damaged)} modules in {dt:.4f}s."

class StressTester:
    """
    Floods the Hivemind to ensure stability.
    """
    def __init__(self, hive):
        self.hive = hive
        
    def run_torture_test(self, count=100):
        print(f"[STRESS] Bombarding Hive with {count} thoughts...")
        errors = 0
        start = time.time()
        for i in range(count):
            try:
                self.hive.broadcast(f"Stress Test Stimulus {i}")
            except Exception as e:
                errors += 1
                
        dt = time.time() - start
        print(f"[STRESS] Complete. {count} cycles in {dt:.2f}s. Errors: {errors}")
        return errors == 0
