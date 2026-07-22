
import unittest
import os
import time
from arinn_core.architect import Architect
from arinn_core.hot_swap import HotReloader

class TestArchitect(unittest.TestCase):
    def setUp(self):
        self.target = "arinn_core/dummy_target.py"
        # Create dummy target
        with open(self.target, "w") as f:
            f.write("def slow_function():\n    time.sleep(0.1)\n    return True\n")
            
    def tearDown(self):
        if os.path.exists(self.target):
            os.remove(self.target)
        if os.path.exists(self.target + ".bak"):
            os.remove(self.target + ".bak")
            
    def test_01_self_rewrite(self):
        print("\n[TEST] Verifying Self-Rewriting Architect...")
        arch = Architect()
        
        # 1. Propose Change
        print("  > Requesting Refactor from NeuralCore...")
        # Since we likely don't have a local LLM, this triggers Symbolic Fallback
        # which appends a comment marker.
        new_code, msg = arch.propose_refactor("dummy_target.py")
        
        self.assertIsNotNone(new_code)
        self.assertIn("# OPTIMIZED BY ARCHITECT", new_code)
        
        # 2. Apply Change (Safety Protocol)
        print("  > Applying Change via Safety Sandbox...")
        success = arch.apply_change("dummy_target.py", new_code)
        self.assertTrue(success)
        
        # 3. Verify File Updated
        with open(self.target, "r") as f:
            content = f.read()
        self.assertIn("# OPTIMIZED BY ARCHITECT", content)
        
        # 4. Verify Backup Exists
        self.assertTrue(os.path.exists(self.target + ".bak"))
        print("  > Backup verified.")
        
        # 5. Hot Reload
        # We need to import it first to reload it
        import arinn_core.dummy_target
        HotReloader.reload_module("arinn_core.dummy_target")

if __name__ == '__main__':
    unittest.main()
