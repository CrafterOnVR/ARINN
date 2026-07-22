
import os
import json
from arinn_core.crucible import Crucible  # type: ignore
from arinn_core.memory_logger import MemoryLogger  # type: ignore

def verify_hybrid():
    print("=== Epoch VIII Verification (Hybrid Stack) ===\n")
    
    crucible = Crucible()
    logger = MemoryLogger()
    
    # 1. Test Crucible Gatekeeper
    print("[TEST] The Crucible...")
    
    # Bad Code
    bad_code = "print('Hello World' " # Syntax Error
    passed, _, msg = crucible.filter_loop(lambda x: bad_code, "Write bad code", max_retries=1)
    if not passed:
        print(f"  > Blocked Bad Code: {msg} (Correct)")
    else:
        print("  > FAILED: Allowed Bad Code!")
        
    # Good Code
    good_code = "print('Verification Successful')"
    passed, code, output = crucible.filter_loop(lambda x: good_code, "Write good code", max_retries=1)
    
    if passed and "Verification Successful" in output:
        print("  > Verified Good Code (Correct)")
    else:
        print(f"  > FAILED: Blocked Good Code! ({output})")
        
    # 2. Test Memory Logger
    print("\n[TEST] Cloud Dreaming Logger...")
    if passed:
        success = logger.log_golden_memory("Write good code", code)
        
        # Verify File
        log_path = "training_data/golden_memories.jsonl"
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                last_line = f.readlines()[-1]
                data = json.loads(last_line)
                if data['output'] == good_code:
                    print(f"  > Logged to JSONL: {log_path} (Correct)")
                else:
                    print("  > FAILED: JSONL content mismatch.")
        else:
             print("  > FAILED: JSONL file not created.")

if __name__ == "__main__":
    verify_hybrid()
