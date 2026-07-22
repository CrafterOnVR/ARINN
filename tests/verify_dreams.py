
import unittest
from arinn_core.hivemind import HiveSwarm
from arinn_core.dream import DreamWeaver

class TestDreams(unittest.TestCase):
    def test_01_rem_cycle(self):
        print("\n[TEST] Verifying Imagination Engine...")
        hive = HiveSwarm()
        weaver = DreamWeaver(hive)
        
        # Run short REM cycle
        print("  > Entering REM Sleep (1s)...")
        count = weaver.enter_rem_cycle(duration=1.0)
        
        print(f"  > Generated {count} synthetic scenarios.")
        print(f"  > Sample Dream: {weaver.dream_journal[0] if count > 0 else 'None'}")
        
        self.assertGreater(count, 0, "No dreams generated in 1s")
        self.assertGreater(len(weaver.dream_journal), 0)

if __name__ == '__main__':
    unittest.main()
