from arinn_core.testing_environment import Crucible  # type: ignore

_instance = None

def verify_code(code_snippet):
    """
    Wrapper for Crucible.verify_code.
    """
    global _instance
    if _instance is None:
        _instance = Crucible()
    
    success, feedback = _instance.verify_code(code_snippet)
    if not success:
        print(f"[CRUCIBLE] Rejected: {feedback[:100]}...")
    else:
        print(f"[CRUCIBLE] Verified Golden.")
    return success
