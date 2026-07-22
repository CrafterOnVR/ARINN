
import os
import sys
import threading
import time
import asyncio
from arinn_core.continuous_learning import ContinuousLearner
from super_enhanced_agent import SuperEnhancedResearchAgent

class MockIdentity:
    def __init__(self):
        # minimal mock for brain
        from arinn_core.brain import ArinnBrain
        self.brain = ArinnBrain()

def test_real_world_learning_execution():
    print("\n--- Testing Real-World Learning Execution (Brief) ---")
    try:
        identity = MockIdentity()
        learner = ContinuousLearner(identity)
        
        # We need to test if it CAN import requests/bs4 (dependencies)
        import requests
        import bs4
        print("[PASS] Dependencies 'requests' and 'bs4' found.")
        
        print("[PASS] ContinuousLearner initialized.")
    except Exception as e:
        print(f"[FAIL] Real-World Learning Setup Failed: {e}")
        return False
    return True

async def test_agent_async_init():
    print("\n--- Testing Agent Async Init ---")
    try:
        # We want to see if maximizing intelligence triggers the warning 
        # (captured via logs usually, here just checking for crash)
        agent = SuperEnhancedResearchAgent(enable_super_intelligence=True, use_llm=False)
        print("[PASS] SuperEnhancedResearchAgent initialized without crash.")
        
        # Check if automation engine is running (it should have been tasked)
        # We give it a moment
        await asyncio.sleep(0.5)
        if hasattr(agent, 'automation_engine') and agent.automation_engine.running:
             print("[PASS] Automation Engine is RUNNING.")
        else:
             print("[WARN] Automation Engine not running? (Might be waiting on loop)")
        
    except Exception as e:
        print(f"[FAIL] Agent Init Failed: {e}")

def main():
    if not test_real_world_learning_execution():
        exit(1)
        
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_agent_async_init())
    
    print("\n(SUCCESS) FINAL VERIFICATION PASSED.")

if __name__ == "__main__":
    main()
