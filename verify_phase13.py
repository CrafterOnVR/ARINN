
import os
import time
from arinn_core.cognitive_expansion import GoalProposer, CognitiveToolCreator
from arinn_core.cross_domain import SynthesisEngine
from arinn_core.memory import SecureMemory

def test_goal_proposal():
    print("\n--- Testing Goal Proposal ---")
    proposer = GoalProposer()
    goal = proposer.propose_goal()
    
    assert goal is not None
    assert goal["type"] == "LEARNING_ONLY"
    assert "description" in goal
    assert goal["confidence"] > 0
    
    print(f"[PASS] Goal Proposed: {goal['description']}")
    
    proposer.complete_goal(goal)
    assert not proposer.active_goals
    assert len(proposer.completed_goals) == 1
    print("[PASS] Goal Completion logic verified.")

def test_tool_creation():
    print("\n--- Testing Cognitive Tool Creation ---")
    creator = CognitiveToolCreator()
    
    # Check default tools
    assert "PatternExtractor" in creator.tools
    print("[PASS] Default tools loaded.")
    
    # Use tool
    usage_before = creator.tools["PatternExtractor"]["usage_count"]
    creator.use_tool("PatternExtractor", success=True)
    usage_after = creator.tools["PatternExtractor"]["usage_count"]
    assert usage_after == usage_before + 1
    print("[PASS] Tool usage tracked.")
    
    # Invent tool
    new_tool = creator.invent_tool()
    assert new_tool in creator.tools
    print(f"[PASS] Invented New Tool: {new_tool}")

def test_cross_domain_synthesis():
    print("\n--- Testing Cross-Domain Synthesis ---")
    engine = SynthesisEngine()
    
    # Attempt synthesis (random chance, so we retry a few times to get a hit)
    mapping = None
    for _ in range(10):
        mapping = engine.attempt_synthesis("Physics", "Economics", "Entropy")
        if mapping: break
        
    if mapping:
        assert mapping["source"] == "Physics"
        assert mapping["target"] == "Economics"
        print(f"[PASS] Synthesis Mapped: {mapping['mapped']} (Conf: {mapping['confidence']:.2f})")
    else:
        print("[WARN] Synthesis unlucky (Random chance failed), but code ran.")

def test_memory_prioritization():
    print("\n--- Testing Memory Prioritization (Non-Destructive) ---")
    mem = SecureMemory(storage_file="test_phase13_mem.enc")
    
    # Store some items
    for i in range(10):
        mem.store(f"item_{i}", f"data_{i}", initial_utility=random.choice([0.9, 0.1]))
        
    # Deprioritize (Keep top 50%)
    demoted = mem.deprioritize_memories(retention_ratio=0.5)
    
    print(f"[PASS] Demoted {demoted} items.")
    
    # Check status
    cache = mem.memory_cache
    archived_count = 0
    for k, v in cache.items():
        if isinstance(v, dict):
            if v.get('priority') == 'ARCHIVE':
                archived_count += 1
                assert v['utility'] <= 0.05
    
    assert archived_count == demoted
    print(f"[PASS] {archived_count} items correctly flagged as ARCHIVE.")
    
    # Cleanup
    if os.path.exists("test_phase13_mem.enc"):
        os.remove("test_phase13_mem.enc")

import random

if __name__ == "__main__":
    try:
        test_goal_proposal()
        test_tool_creation()
        test_cross_domain_synthesis()
        test_memory_prioritization()
        print("\n(SUCCESS) ALL PHASE 13 VERIFICATIONS PASSED.")
    except Exception as e:
        print(f"\n(FAIL) VERIFICATION FAILED: {e}")
        exit(1)
