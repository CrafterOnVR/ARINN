from arinn_core.memory_logger import MemoryLogger  # type: ignore

_instance = None

def log_golden_memory(prompt, code):
    """
    Wrapper for MemoryLogger.log_golden_memory.
    """
    global _instance
    if _instance is None:
        _instance = MemoryLogger()
    
    return _instance.log_golden_memory(prompt, code)

def retrieve_relevant_memory(query):
    """
    Wrapper for MemoryLogger.retrieve_relevant_memory.
    """
    global _instance
    if _instance is None:
        _instance = MemoryLogger()
    
    return _instance.retrieve_relevant_memory(query)
