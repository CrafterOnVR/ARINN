
import os
import torch
from arinn_core.brain import ArinnBrain

def test_unified_brain():
    print("\n--- Testing Unified Brain Architecture ---")
    
    # 1. Clean old files
    model_path = "test_unified_brain.pth"
    referee_path = "test_unified_brain_referee.pth"
    config_path = "test_unified_brain_configs.json"
    
    if os.path.exists(model_path): os.remove(model_path)
    if os.path.exists(referee_path): os.remove(referee_path)
    if os.path.exists(config_path): os.remove(config_path)
    
    # 2. Initialize Brain (Should create Hivemind + Referee)
    print("Initializing Brain...")
    brain = ArinnBrain(model_path=model_path)
    
    assert hasattr(brain, 'model'), "Brain missing Hivemind"
    assert hasattr(brain, 'arena'), "Brain missing DebateArena (Referee)"
    assert brain.model.num_experts == 20
    print("[PASS] Brain initialized with all organs.")
    
    # 3. Modify Referee State (Train it slightly to change weights)
    print("Modifying Referee State...")
    original_weight = brain.arena.referee.fc1.weight.data.clone()
    
    # Fake training signal
    inputs = torch.randn(1, 2)
    brain.arena.train_referee(inputs, target_success=1.0)
    
    new_weight = brain.arena.referee.fc1.weight.data
    assert not torch.equal(original_weight, new_weight), "Referee weights didn't change"
    print("[PASS] Referee state modified.")
    
    # 4. Save
    print("Saving Unified State...")
    brain.save()
    
    assert os.path.exists(model_path)
    assert os.path.exists(referee_path)
    assert os.path.exists(config_path)
    print("[PASS] All component files created.")
    
    # 5. Load New Instance
    print("Loading Unified State into New Brain...")
    brain2 = ArinnBrain(model_path=model_path)
    
    # Check if weights match
    loaded_weight = brain2.arena.referee.fc1.weight.data
    assert torch.equal(new_weight, loaded_weight), "Referee state lost on reload!"
    print("[PASS] Referee state persisted and loaded.")
    
    # Cleanup
    if os.path.exists(model_path): os.remove(model_path)
    if os.path.exists(referee_path): os.remove(referee_path)
    if os.path.exists(config_path): os.remove(config_path)

if __name__ == "__main__":
    try:
        test_unified_brain()
        print("\n(SUCCESS) UNIFIED ARCHITECTURE VERIFIED.")
    except Exception as e:
        print(f"\n(FAIL) VERIFICATION FAILED: {e}")
        exit(1)
