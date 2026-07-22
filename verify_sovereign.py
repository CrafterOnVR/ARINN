
import threading
import time
import sys
from sovereign import sovereign_loop  # type: ignore

def verify_sovereign():
    print("[TEST] Launching Sovereign Loop in background...")
    
    # Run loop in thread so we can kill it
    t = threading.Thread(target=sovereign_loop, daemon=True)
    t.start()
    
    print("[TEST] Thread started. Watching for 10 seconds...")
    time.sleep(15)
    
    if t.is_alive():
        print("[TEST] Sovereign is active (looping). Test Passed.")
        print("[TEST] Terminating simulation.")
    else:
        print("[TEST] Sovereign died prematurely. Test Failed.")

if __name__ == "__main__":
    verify_sovereign()
