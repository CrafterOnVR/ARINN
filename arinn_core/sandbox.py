
import subprocess
import logging
import os
import sys
import threading
import time
from typing import Dict, Any, Optional

class SandboxExecutor:
    """
    Executes code in a controlled separate process (Sandbox).
    Prevents experimental code from crashing the main agent.
    """
    
    def __init__(self, timeout_seconds=5.0):
        self.timeout = timeout_seconds

    def run_snippet(self, code_snippet: str, env_vars: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Runs a python snippet in a separate process.
        """
        # Create a temporary file for the snippet
        import tempfile
        
        result = {
            "success": False,
            "stdout": "",
            "stderr": "",
            "exit_code": None,
            "timed_out": False
        }

        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code_snippet)
                temp_path = f.name
            
            # Prepare environment
            proc_env = os.environ.copy()
            if env_vars:
                proc_env.update(env_vars)
            
            # Run subprocess
            # We use sys.executable to ensure we run with the same python interpreter
            start_time = time.time()
            try:
                proc = subprocess.run(
                    [sys.executable, temp_path],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    env=proc_env
                )
                
                result["stdout"] = proc.stdout
                result["stderr"] = proc.stderr
                result["exit_code"] = proc.returncode
                result["success"] = (proc.returncode == 0)
                
            except subprocess.TimeoutExpired as e:
                result["timed_out"] = True
                result["stdout"] = e.stdout.decode() if e.stdout else ""
                result["stderr"] = e.stderr.decode() if e.stderr else "Timed Out"
                
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
        except Exception as e:
            result["stderr"] = f"Sandbox Infrastructure Error: {e}"
            
        return result
