
import subprocess
import sys
import time
import os
import signal

# ARINN WATCHER V1.0
# Purpose: Supervises the Genesis Engine. Handles crashes and "Magic 42" updates.

GENESIS_SCRIPT = "genesis.py"
EXIT_CODE_SHUTDOWN = 0
EXIT_CODE_CRASH = 1
EXIT_CODE_UPDATE = 42

def log(message):
    print(f"[WATCHER] {message}")

def run_genesis():
    """
    Runs the Genesis Engine as a subprocess.
    Returns the exit code.
    """
    log(" launching Genesis...")
    try:
        # We pass sys.argv to allow arguments to flow through if needed
        # mainly python executable + script + args
        cmd = [sys.executable, GENESIS_SCRIPT] + sys.argv[1:] # type: ignore
        
        # Start the process
        process = subprocess.Popen(cmd)
        
        # specific logic to handle KeyboardInterrupt in watcher and pass it to child?
        # For now, we just wait.
        try:
            exit_code = process.wait()
            return exit_code
        except KeyboardInterrupt:
            log("Interrupted. Stopping Genesis...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            return EXIT_CODE_SHUTDOWN
            
    except Exception as e:
        log(f"CRITICAL ERROR launching Genesis: {e}")
        return EXIT_CODE_CRASH

def main():
    log("Arinn Watcher Initiated.")
    log(f"Target: {GENESIS_SCRIPT}")
    
    while True:
        code = run_genesis()
        
        if code == EXIT_CODE_SHUTDOWN:
            log("Genesis requested Shutdown. Execution complete.")
            break
            
        elif code == EXIT_CODE_UPDATE:
            log("UPDATE SIGNAL RECEIVED (Code 42).")
            log("Genesis has updated itself. Restarting in 3 seconds...")
            time.sleep(3)
            # Loop continues, re-launching genesis
            
        else:
            log(f"Genesis exited unexpectedly with code {code}.")
            log("Crash detected. Rebooting in 5 seconds...")
            time.sleep(5)
            # Loop continues
            
if __name__ == "__main__":
    main()
