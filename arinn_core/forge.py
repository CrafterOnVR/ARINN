
import sys
import subprocess
import importlib
import logging

class InfinityForge:
    """
    Phase 37: The Infinity Forge.
    Real-World Effect: Physical expansion of the agent's environment.
    Allows ARINN to 'forge' new tools by installing PyPI packages at runtime.
    """
    @staticmethod
    def install(package_name):
        """
        Uses pip to install a package.
        """
        print(f"[FORGE] Detecting missing capability... Forging '{package_name}'...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"[FORGE] Successfully installed {package_name}.")
            
            # Attempt to import it immediately to verify
            try:
                importlib.invalidate_caches()
                importlib.import_module(package_name)
                print(f"[FORGE] Module '{package_name}' is now active memory.")
                return True
            except ImportError:
                print(f"[FORGE] Installed {package_name} but dynamic import failed (requires restart?).")
                return True
                
        except subprocess.CalledProcessError as e:
            logging.error(f"[FORGE] Failed to forge {package_name}: {e}")
            return False

    @staticmethod
    def ensure_import(module_name, package_name=None):
        """
        Tries to import module. If not found, installs package.
        """
        if not package_name:
            package_name = module_name
            
        try:
            importlib.import_module(module_name)
            return True
        except ImportError:
            print(f"[FORGE] Missing dependency: {module_name}")
            return InfinityForge.install(package_name)
