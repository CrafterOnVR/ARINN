
import time
import requests # type: ignore
import sys
import os
import random

# Configuration
CORE_URL = "http://localhost:9999"
NODE_ID = f"SAT-{os.getpid()}"

def run_satellite():
    """
    Phase 39: Nebula Node.
    The worker unit of the mesh.
    """
    print(f"[{NODE_ID}] Satellite Online. Establishing Uplink to {CORE_URL}...")
    
    # 1. Register
    try:
        requests.post(f"{CORE_URL}/register", json={"id": NODE_ID})
        print(f"[{NODE_ID}] Uplink Established. Standing by for Hive directives.")
    except Exception:
        print(f"[{NODE_ID}] Uplink Failed. Core not found. Aborting.")
        return

    # 2. Loop
    while True:
        try:
            # Poll for task
            resp = requests.get(f"{CORE_URL}/task")
            if resp.status_code == 200:
                data = resp.json()
                task = data.get("task")
                
                if task:
                    print(f"[{NODE_ID}] Processing Directive: {task['type']}")
                    import hashlib
                    # Genuine CPU computational proof-of-work
                    proof = str(task.get('payload', 'null')).encode()
                    for _ in range(300000): # Hard CPU-bound loop to prove cycles
                        proof = hashlib.sha256(proof).digest()
                    
                    # Result
                    result = f"Computed cryptographic task hash: {bytes(proof).hex()[:12]}" # type: ignore
                    requests.post(f"{CORE_URL}/result", json={"id": NODE_ID, "result": result})
                    print(f"[{NODE_ID}] Task Complete. Intel Uploaded.")
                else:
                    # Idle heartbeat
                    print(f"[{NODE_ID}] ...listening...", end="\r")
                    time.sleep(2)
            else:
                time.sleep(2)
                
        except Exception as e:
            print(f"[{NODE_ID}] Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_satellite()
