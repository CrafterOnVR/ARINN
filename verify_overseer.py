
import unittest
import os
from arinn_core.overseer import Overseer

class TestOverseer(unittest.TestCase):
    def test_01_panopticon(self):
        print("\n[TEST] Verifying Overseer Protocol (Omniscience)...")
        # Point to arinn_core
        target_dir = os.path.join(os.getcwd(), "arinn_core")
        overseer = Overseer(workspace_path=target_dir)
        
        # 1. Scan
        count = overseer.scan_workspace()
        print(f"  > Indexed {count} files in arinn_core.")
        self.assertGreater(count, 0)
        
        # 2. Verify Knowledge in Titan
        # Did it find 'Overseer' class?
        # Note: We just imported it, so the file exists.
        has_overseer = overseer.titan.graph.has_node("Overseer")
        print(f"  > Knowledge of 'Overseer' class present: {has_overseer}")
        self.assertTrue(has_overseer)
        
        # 3. Resource Vacuum
        scale = overseer.calculate_swarm_scale()
        print(f"  > Recommended Swarm Scale (based on CPU): {scale} Agents")
        self.assertGreaterEqual(scale, 1)

if __name__ == '__main__':
    unittest.main()
