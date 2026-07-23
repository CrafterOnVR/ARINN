import os
import sys
import psutil
import threading
import time

class SecurityJailViolation(Exception):
    pass

class CyberGauntlet:
    """
    Phase 11: The Paranoia Mode (Zero-Trust Protocol) and Immune System.
    Provides OS-level intercepts and physical hardware monitoring to ensure 
    subagents cannot crash the machine or edit unauthorized files.
    """
    
    def __init__(self, safe_zone: str, cpu_threshold: float = 90.0, network_allowed: bool = False):
        self.safe_zone = os.path.abspath(safe_zone)
        self.cpu_threshold = cpu_threshold
        self.network_allowed = network_allowed
        self.immune_active = False

    def activate_zero_trust(self):
        """
        Injects a low-level audit hook into the Python interpreter.
        This intercepts every OS-level call made by this process.
        """
        def audit_hook(event, args):
            # 1. Block unauthorized File Access
            if event == "builtins.open" or event == "os.open":
                path = os.path.abspath(args[0])
                # We allow reading of Python libraries, but block writing/accessing 
                # things outside the safe zone (unless it's in a known safe read-only dir)
                if not path.startswith(self.safe_zone):
                    # For a strict jail, we would block everything. For ARINN to function, 
                    # we must block WRITE access outside the safe zone.
                    mode = args[1] if len(args) > 1 else "r"
                    if "w" in mode or "a" in mode or "+" in mode:
                        raise SecurityJailViolation(f"[GAUNTLET] BLOCKED WRITE ATTEMPT outside Safe Zone: {path}")

            # 2. Block Subprocesses / Shell Execution
            if event == "subprocess.Popen" or event == "os.system":
                cmd = args[1] if len(args) > 1 else ""
                if isinstance(cmd, (list, tuple)):
                    cmd_str = " ".join(str(c) for c in cmd)
                else:
                    cmd_str = str(cmd)
                    
                    # Whitelist hardware probes used by AI libraries (ChromaDB, Torch)
                    # We also whitelist 'python' so the ToolSandbox can verify generated code
                    safe_commands = ["lscpu", "wmic", "sysctl", "systeminfo", "nvidia-smi", "chcp", "ver", "python"]
                    if not any(safe in cmd_str.lower() for safe in safe_commands):
                        raise SecurityJailViolation(f"[GAUNTLET] BLOCKED UNAUTHORIZED SHELL EXECUTION: {args}")

            # 3. Block Network Access (if disallowed)
            if not self.network_allowed and (event == "socket.connect" or event == "urllib.Request"):
                # Exception: Allow HuggingFace and common CDN ports for model downloading 
                # (NeuralCore needs to fetch weights securely via HTTPS)
                if event == "socket.connect" and len(args) > 1 and isinstance(args[1], tuple) and len(args[1]) >= 2:
                    ip, port = args[1][0], args[1][1]
                    if port == 443:
                        return # Allow secure model downloads
                
                raise SecurityJailViolation(f"[GAUNTLET] BLOCKED UNAUTHORIZED NETWORK REQUEST: {args}")

        sys.addaudithook(audit_hook)
        print(f"[GAUNTLET] Zero-Trust Audit Hook Active. Safe Zone: {self.safe_zone}")

    def _immune_system_loop(self):
        """Watchdog thread that monitors CPU usage"""
        p = psutil.Process(os.getpid())
        high_cpu_seconds = 0
        
        while self.immune_active:
            try:
                # Get CPU percentage over a 1 second interval
                cpu_usage = p.cpu_percent(interval=1.0)
                if cpu_usage > self.cpu_threshold:
                    high_cpu_seconds += 1
                else:
                    high_cpu_seconds = 0
                    
                if high_cpu_seconds >= 3: # 3 consecutive seconds over threshold
                    print(f"\n[IMMUNE SYSTEM] COLLAPSE SCORE EXCEEDED! CPU spiked to {cpu_usage}%.")
                    print("[IMMUNE SYSTEM] Assuming infinite loop mutation. Terminating process...")
                    p.kill() # Hard kill the process
            except psutil.NoSuchProcess:
                break
            time.sleep(0.1)

    def activate_immune_system(self):
        """Starts the CPU/RAM watchdog thread"""
        # DISABLED PER USER REQUEST - Immune System was killing active evolution loops
        print("[GAUNTLET] Immune System Watchdog DISABLED. Agent free to consume 100% CPU.")
        pass

    def lock_agent(self):
        """Engages all security protocols for the current process."""
        self.activate_zero_trust()
        self.activate_immune_system()
