
import os
import shutil
import time

def load_upgrade():
    """
    Phase 73: The Brain Transplant Loader.
    Checks for new GGUF models from Cloud Dreaming.
    """
    model_dir = "arinn_model"
    active_model = "current_brain.gguf"
    
    if not os.path.exists(model_dir):
        os.makedirs(model_dir, exist_ok=True)
        
    # Look for new files
    candidates = [f for f in os.listdir(model_dir) if f.endswith(".gguf") and f != active_model]
    
    if not candidates:
        print("[LOADER] No new brain upgrades found.")
        return False
        
    print(f"[LOADER] Found {len(candidates)} candidate brains: {candidates}")
    
    # Pick latest
    candidates.sort(key=lambda x: os.path.getmtime(os.path.join(model_dir, x)), reverse=True)
    new_brain = candidates[0]
    
    print(f"[LOADER] Initiating Transplant: {new_brain} -> {active_model}")
    
    # Backup
    if os.path.exists(os.path.join(model_dir, active_model)):
        backup_name = f"backup_{int(time.time())}.gguf"
        shutil.move(os.path.join(model_dir, active_model), os.path.join(model_dir, backup_name))
        print(f"[LOADER] Old brain backed up to {backup_name}")
        
    # Install
    shutil.copy(os.path.join(model_dir, new_brain), os.path.join(model_dir, active_model))
    print("[LOADER] Transplant Complete. ARINN has evolved.")
    return True

if __name__ == "__main__":
    load_upgrade()
