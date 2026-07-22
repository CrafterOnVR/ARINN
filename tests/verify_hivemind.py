
import unittest
from arinn_core.hivemind import HiveSwarm

class TestHivemind(unittest.TestCase):
    def test_01_initialize(self):
        print("\n[TEST] Verifying Hive Genesis...")
        hive = HiveSwarm()
        self.assertEqual(len(hive.brains), 20, "Should have 20 SubBrains")
        print("  > 20 SubBrains confirmed online.")
        
    def test_02_sparse_activation(self):
        print("\n[TEST] Verifying Sparse Activation...")
        hive = HiveSwarm()
        
        # Stimulus with clear domain keyword
        stimulus = "Can you explain the Physics of a black hole?"
        
        # Check percepts directly
        active = [b.domain for b in hive.brains if b.perceive(stimulus)]
        print(f"  > Stimulus: '{stimulus}' -> Active: {active}")
        
        self.assertIn("Physics", active, "Physics brain should have woken up")
        self.assertNotIn("Psychology", active, "Psychology brain should sleep (unless low perplexity)")
        
    def test_03_arbitration(self):
        print("\n[TEST] Verifying Arbitration...")
        hive = HiveSwarm()
        response = hive.broadcast("What is the Logic behind this code?")
        print(f"  > Hive Response:\n{response}")
        
        self.assertIn("Consensus", response)
        self.assertIn("Logic", response)

if __name__ == '__main__':
    unittest.main()
