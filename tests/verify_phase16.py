
import time
from arinn_core.instruction_mastery import InstructionDecomposer, ExecutionDAG, FeedbackLoop
from arinn_core.consensus import ConsensusManager, RefereeArbitration

# Mock Hivemind for testing
class MockHivemind:
    def __init__(self):
        self.experts = ["E1", "E2", "E3"]

def test_instruction_stack():
    print("\n--- Testing Phase 16 Instruction Mastery ---")
    
    # 1. Decomposition
    decomposer = InstructionDecomposer()
    # Complex instruction
    instruction = "Study the aerodynamics of bumblebees"
    tasks = decomposer.decompose(instruction)
    
    assert len(tasks) == 3 # SEARCH, READ, COMPUTE
    print(f"[PASS] Decomposed '{instruction}' into {len(tasks)} tasks.")
    print(f"       Types: {[t.type for t in tasks]}")
    
    # 2. DAG Dependencies
    # Task 1 (Search) must be done before Task 2 (Read)
    dag = ExecutionDAG(tasks)
    runnable = dag.get_runnable_tasks()
    
    assert len(runnable) == 1
    assert runnable[0].type == "SEARCH"
    print("[PASS] DAG Dependency Check 1: Only SEARCH is runnable.")
    
    # Complete Search
    dag.update_task(runnable[0].id, "COMPLETED")
    runnable_next = dag.get_runnable_tasks()
    
    assert len(runnable_next) == 1
    assert runnable_next[0].type == "READ"
    print("[PASS] DAG Dependency Check 2: READ unlocked after SEARCH.")
    
    # 3. Consensus
    hivemind = MockHivemind()
    consensus = ConsensusManager(hivemind)
    approved, score, msg = consensus.verify_plan(tasks)
    
    # Random vote, so we just check it runs
    print(f"[PASS] Consensus check ran. Result: {approved} (Score: {score:.2f})")
    
    # 4. Feedback / Correction
    feedback = FeedbackLoop()
    # Mock a failed task
    failed_task = tasks[0]
    failed_task.type = "COMPUTE"
    failed_task.error = "ZeroDivisionError: division by zero"
    
    correction = feedback.analyze_failure(failed_task)
    assert "CONCEPTUAL_ERROR" in correction
    print(f"[PASS] Feedback Loop caught ZeroDivision: {correction}")

if __name__ == "__main__":
    try:
        test_instruction_stack()
        print("\n(SUCCESS) ALL PHASE 16 VERIFICATIONS PASSED.")
    except Exception as e:
        print(f"\n(FAIL) VERIFICATION FAILED: {e}")
        exit(1)
