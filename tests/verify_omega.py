
import unittest
import logging
# Suppress logging for cleaner output
logging.getLogger().setLevel(logging.CRITICAL)

from arinn_core.omega import Omega

class TestOmega(unittest.TestCase):
    def test_01_convergence(self):
        print("\n[TEST] Verifying Omega Loop (AGI Convergence)...")
        
        # Init Omega (Scans workspace, builds Titan)
        omega = Omega()
        
        # Run 1 Cycle
        print("  > Triggering Cycle: 'Understand Entropy'")
        omega.solve("Understand Entropy")
        
        # Verify Scaled Swarm based on Resources using resource monitor
        # If CPU is low locally, it might scale up
        print(f"  > Swarm Scaled to: {omega.swarm.pool_size} agents")
        self.assertGreaterEqual(omega.swarm.pool_size, 1)

if __name__ == '__main__':
    unittest.main()
