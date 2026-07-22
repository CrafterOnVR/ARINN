
import time
from arinn_core.planetary_brain import PlanetaryMind

def test_planetary_brain():
    print("\n--- Testing Phase 19 Planetary Cognition ---")
    
    # 1. Initialize Mind
    mind = PlanetaryMind()
    assert len(mind.agents) == 0
    
    # 2. Spawn Agents
    id1 = mind.spawn_agent("TestAgent1")
    id2 = mind.spawn_agent("TestAgent2")
    
    assert len(mind.agents) == 2
    assert mind.agents[0].is_alive()
    print(f"[PASS] Spawned 2 agents: {id1}, {id2}")
    
    # 3. Wait for Insights (Parallel Execution)
    # Agents sleep 0.1s + 0.5s = 0.6s per cycle.
    # Wait 2 seconds, should have insights.
    print("Waiting for agents to generate insights...")
    time.sleep(2.5)
    
    logs = mind.state.logs
    count = len(logs)
    print(f"[PASS] Agents generated {count} logs.")
    if count == 0:
        print("[FAIL] No logs generated. Threads stuck?")
    assert count > 0
    
    # 4. Check Global State Integrity
    # Insights should be stored by topic
    insights1 = mind.state.get_insights("TestAgent1")
    insights2 = mind.state.get_insights("TestAgent2")
    
    total_stored = len(insights1) + len(insights2)
    print(f"[PASS] Global Knowledge Base has {total_stored} items.")
    assert total_stored > 0
    
    # 5. Shutdown
    print("Stopping swarm...")
    mind.stop_all()
    
    assert not mind.agents[0].running
    print("[PASS] Swarm shutdown successfully.")

if __name__ == "__main__":
    try:
        test_planetary_brain()
        print("\n(SUCCESS) ALL PHASE 19 VERIFICATIONS PASSED.")
    except Exception as e:
        print(f"\n(FAIL) VERIFICATION FAILED: {e}")
        exit(1)
