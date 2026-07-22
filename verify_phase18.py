
from arinn_core.strategic_autonomy import DomainManager, MetaPlanner, IdeaSynthesizer

def test_strategic_autonomy():
    print("\n--- Testing Phase 18 Strategic Autonomy ---")
    
    # 1. Skill Tree / Domain Manager
    dm = DomainManager()
    assert dm.domains['Coding']['level'] == 0
    
    # Add XP (Level up threshold is 100 for lvl 0)
    leveled = dm.add_xp('Coding', 101)
    
    assert leveled is True
    assert dm.domains['Coding']['level'] == 1
    assert dm.domains['Coding']['xp'] == 1
    print(f"[PASS] Domain Level Up works. Code Lv: {dm.domains['Coding']['level']}")
    
    # 2. Meta-Planner
    planner = MetaPlanner()
    target_lvl = 2
    strat = planner.create_strategy("Coding", target_lvl)
    
    assert strat['goal'] == "Reach Coding Lvl 2"
    assert len(strat['dag'].tasks) > 0
    print(f"[PASS] Strategy Created: {strat['goal']} with {len(strat['dag'].tasks)} tasks.")
    
    # 3. Idea Synthesizer
    # Need at least two active domains > lvl 0
    dm.add_xp('Physics', 101) # Level up Physics
    
    synth = IdeaSynthesizer(dm)
    idea = synth.synthesize()
    
    assert idea is not None
    assert idea['hypothesis'] is not None
    print(f"[PASS] Idea Synthesized: {idea['hypothesis']}")
    
    # Test failure case (only 1 domain)
    dm2 = DomainManager()
    dm2.domains['General']['level'] = 0 # Force disable General
    dm2.add_xp('Coding', 101) # Level 1
    
    synth2 = IdeaSynthesizer(dm2)
    idea2 = synth2.synthesize() # active = [Coding]. len < 2.
    assert idea2 is None
    print("[PASS] Synthesizer correctly handles insufficient domains.")

if __name__ == "__main__":
    try:
        test_strategic_autonomy()
        print("\n(SUCCESS) ALL PHASE 18 VERIFICATIONS PASSED.")
    except Exception as e:
        print(f"\n(FAIL) VERIFICATION FAILED: {e}")
        exit(1)
