
import os
import hashlib
import shutil
import logging
from typing import List, Dict

class FailsafeGuard:
    """
    Independent system integrity verifier.
    Ensures critical files exist and are not corrupted.
    Triggered before and after sensitive operations.
    """
    
    CRITICAL_FILES = [
        "agent.py",
        "super_enhanced_agent.py",
        "arinn_core/brain.py",
        "arinn_core/identity.py",
        "safety_controller.py"
    ]
    
    BACKUP_DIR = "backup_stable"
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = root_dir
        self.hashes: Dict[str, str] = {}
        
    def create_stable_snapshot(self):
        """Creates a verified snapshot of the current state."""
        if not os.path.exists(self.BACKUP_DIR):
            os.makedirs(self.BACKUP_DIR)
            
        for filename in self.CRITICAL_FILES:
            src = os.path.join(self.root_dir, filename)
            if os.path.exists(src):
                # Calculate hash
                file_hash = self._get_hash(src)
                self.hashes[filename] = file_hash
                
                # Copy to backup
                dst = os.path.join(self.BACKUP_DIR, os.path.basename(filename)) # Flatten structure for simple backup
                shutil.copy2(src, dst)
                
        # Save hashes
        with open(os.path.join(self.BACKUP_DIR, "manifest.chk"), "w") as f:
            for k, v in self.hashes.items():
                f.write(f"{k}={v}\n")
                
        logging.info("[FAILSAFE] Stable snapshot created.")

    def verify_integrity(self) -> bool:
        """
        Checks if current critical files match the stable snapshot manifest.
        Returns False if any file is missing or modified unexpectedly (if we expected stability).
        """
        manifest_path = os.path.join(self.BACKUP_DIR, "manifest.chk")
        if not os.path.exists(manifest_path):
            logging.warning("[FAILSAFE] No manifest found. Cannot verify.")
            return True # Assume safe if no baseline, or force fail? Safe for now to allow init.
            
        # Re-read manifest
        stored_hashes = {}
        with open(manifest_path, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=")
                    stored_hashes[k] = v
                    
        # Check files
        for filename, expected_hash in stored_hashes.items():
            filepath = os.path.join(self.root_dir, filename)
            if not os.path.exists(filepath):
                logging.error(f"[FAILSAFE] Critical file missing: {filename}")
                return False
                
            current_hash = self._get_hash(filepath)
            if current_hash != expected_hash:
                # In Phase 7, code modifications are FORBIDDEN unless manual. 
                # So any change here implies unauthorized modification or corruption.
                logging.error(f"[FAILSAFE] Integrity mismatch: {filename}")
                return False
                
        return True

    def rollback(self):
        """Restores files from backup."""
        logging.warning("[FAILSAFE] INITIATING ROLLBACK...")
        for filename in self.CRITICAL_FILES:
            backup_path = os.path.join(self.BACKUP_DIR, os.path.basename(filename))
            target_path = os.path.join(self.root_dir, filename)
            
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, target_path)
                logging.info(f"[FAILSAFE] Restored {filename}")
            else:
                logging.error(f"[FAILSAFE] Backup missing for {filename}!")
                
    def _get_hash(self, path: str) -> str:
        sha = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                sha.update(chunk)
        return sha.hexdigest()
