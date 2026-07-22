
import importlib
import sys
import logging

class HotReloader:
    """
    Phase 33: Hot Swap.
    Allows ARINN to update its brain while running.
    """
    @staticmethod
    def reload_module(module_name):
        try:
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
                print(f"[HOTSWAP] Module '{module_name}' reloaded successfully.")
                return True
            else:
                print(f"[HOTSWAP] Module '{module_name}' not loaded.")
                return False
        except Exception as e:
            logging.error(f"[HOTSWAP] Failed to reload {module_name}: {e}")
            return False
