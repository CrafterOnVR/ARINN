
import logging
import sys
from .sandbox import SandboxExecutor  # type: ignore

class Crucible:
    """
    Phase 70: The Crucible.
    Local Verification Engine & Gatekeeper.
    Enforces that NO code leaves the system unless it passes execution.
    """
    def __init__(self):
        self.sandbox = SandboxExecutor(timeout_seconds=5.0)

    def check_syntax(self, code_snippet):
        """
        Runs static analysis via flake8.
        Returns: (passed: bool, feedback: str)
        """
        import tempfile
        import subprocess
        import os

        # Write code to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py', encoding='utf-8') as tmp:
            tmp.write(code_snippet)
            tmp_path = tmp.name

        try:
            # Run flake8 (F821 undefined name, E999 syntax error)
            # focusing on fatal errors first.
            cmd = [
                'flake8', 
                tmp_path, 
                '--select=E9,F63,F7,F82', 
                '--isolated', 
                '--format=%(row)d:%(col)d: %(code)s %(text)s'
            ]
            # If flake8 is not found in PATH but we installed it, try module invocation
            # But earlier logs showed scripts warn about PATH. 
            # Safe bet: python -m flake8
            cmd = [sys.executable, '-m', 'flake8', tmp_path, '--select=E9,F63,F7,F82', '--isolated']
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, "Syntax Check Passed."
            else:
                # Return the stderr/stdout from flake8
                issues = result.stdout.strip() + result.stderr.strip()
                # Clean up filename from output to avoid confusion
                issues = issues.replace(tmp_path, "generated_code.py")
                return False, f"Static Analysis Failed:\n{issues}"

        except Exception as e:
            return False, f"Linter Error: {e}"
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def verify_code(self, code_snippet):
        """
        Runs the code in the Sandbox.
        Returns (Success: bool, Feedback: str)
        """
        # 1. Static Check (Syntax/Linter)
        if "import" not in code_snippet and "print" not in code_snippet:
             return False, "Code seems empty or invalid (no imports/prints)."
             
        syntax_ok, syntax_msg = self.check_syntax(code_snippet)
        if not syntax_ok:
            return False, syntax_msg

        # 2. Runtime Check (Sandbox)
        result = self.sandbox.run_snippet(code_snippet)
        
        if result['success']:
            return True, result['stdout']
        else:
            error_msg = result['stderr']
            if result['timed_out']:
                error_msg = "Execution Timed Out (Limit 5s)."
            return False, error_msg

    def filter_loop(self, generator_func, prompt, max_retries=3):
        """
        The Gatekeeper Loop.
        Args:
            generator_func: Function(context) -> code_str
            prompt: Initial task prompt
        Returns:
            (is_golden: bool, final_code: str, execution_log: str)
        """
        current_context = prompt
        
        for attempt in range(max_retries + 1):
            print(f"[CRUCIBLE] Attempt {attempt+1}/{max_retries+1}...")
            
            # 1. Generate
            code = generator_func(current_context)
            
            # 2. Verify
            passed, feedback = self.verify_code(code)
            
            if passed:
                print(f"[CRUCIBLE] Verification Passed! (Golden)")
                return True, code, feedback
            else:
                print(f"[CRUCIBLE] Verification Failed: {feedback.strip()[:100]}...")
                # 3. Retry Feedback
                current_context = f"{prompt}\n\nPREVIOUS ATTEMPT FAILED.\nCODE:\n{code}\n\nERROR:\n{feedback}\n\nFIXED CODE:"
                
        print("[CRUCIBLE] All attempts failed. Rejecting output.")
        return False, None, feedback
