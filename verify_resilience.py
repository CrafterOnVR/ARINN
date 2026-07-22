
import unittest
import os
import shutil
from arinn_core.resilience import AutoHealer, StressTester
from arinn_core.hivemind import HiveSwarm

class TestResilience(unittest.TestCase):
    def setUp(self):
        # Setup a dummy module to break
        self.test_dir = "arinn_core"
        self.dummy_path = os.path.join(self.test_dir, "dummy_fragile.py")
        with open(self.dummy_path, 'w') as f:
            f.write("def safe_function():\n    return 'Safe'\n")
            
    def tearDown(self):
        if os.path.exists(self.dummy_path):
            os.remove(self.dummy_path)
            
    def test_01_immortality(self):
        print("\n[TEST] Verifying Auto-Healer (Immortality)...")
        healer = AutoHealer(self.test_dir)
        
        # 1. Break the file
        print("  > SABOTAGE: Corrupting dummy_fragile.py...")
        with open(self.dummy_path, 'w') as f:
            f.write("def broken_function()\n    return 'Syntax Error'\n") # Missing colon
            
        # 2. Check Integrity
        damaged = healer.check_integrity()
        self.assertIn("dummy_fragile.py", damaged)
        print("  > Healer detected damage.")
        
        # 3. Heal
        success, msg = healer.heal()
        print(f"  > Heal Result: {msg}")
        self.assertTrue(success)
        
        # 4. Verify Fix
        damaged_after = healer.check_integrity()
        self.assertEqual(len(damaged_after), 0)
        
    def test_02_stress_test(self):
        print("\n[TEST] Verifying Hivemind Stress Stability...")
        hive = HiveSwarm()
        tester = StressTester(hive)
        
        # Run small batch for speed
        success = tester.run_torture_test(count=10)
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()
