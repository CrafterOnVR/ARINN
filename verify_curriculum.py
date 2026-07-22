
from arinn_core.advanced_curriculum import get_curriculum

def test_curriculum():
    print("\n--- Testing Acceleration Curriculum (Refined) ---")
    
    curriculum = get_curriculum()
    assert isinstance(curriculum, dict)
    assert len(curriculum) == 10
    
    # Check structure of Module 1
    mod1 = curriculum[1]
    required_keys = ["title", "core_skill", "axiom", "what_to_learn", "signals_of_mastery", "accelerates", "depends_on"]
    
    for key in required_keys:
        assert key in mod1, f"Missing key: {key}"
        
    print(f"Module 1 Loaded: {mod1['title']}")
    print(f"Signals: {mod1['signals_of_mastery'][0]}...")
    print(f"Accelerates: {mod1['accelerates'][0]}...")
    print("[PASS] Curriculum structure verified (All new fields present).")
    
    # Check Module 10 Refinement
    mod10 = curriculum[10]
    has_pruners = False
    for item in mod10['what_to_learn']:
        if "Search-Space Pruners" in item:
            has_pruners = True
            break
    assert has_pruners, "Module 10 missing 'Search-Space Pruners'"
    print("[PASS] Module 10 includes Search-Space Pruners.")
    
    # Check Dependency Logic
    assert isinstance(mod1['depends_on'], list)
    print("[PASS] Dependency graph structure valid.")

if __name__ == "__main__":
    try:
        test_curriculum()
        print("\n(SUCCESS) REFINED CURRICULUM VERIFIED.")
    except Exception as e:
        print(f"\n(FAIL) VERIFICATION FAILED: {e}")
        exit(1)
