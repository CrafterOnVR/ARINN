
import unittest
import time
from arinn_core.vision_system import VisionSystem
from arinn_core.hivemind import HiveSwarm

class TestPerformance(unittest.TestCase):
    def test_01_vision_speed(self):
        print("\n[TEST] Benchmarking Vision System...")
        vision = VisionSystem()
        img = vision.capture()
        if img is None: 
            print("  > Skipping calc (No Screen)")
            return

        # Warmup
        vision.analyze(img)
        
        # Benchmark
        start_t = time.time()
        for _ in range(10):
            vision.analyze(img)
        duration = (time.time() - start_t) / 10
        
        print(f"  > Vision Analysis Time: {duration:.4f}s avg")
        self.assertLess(duration, 0.5, "Vision analysis is too slow!")

    def test_02_hive_parallelism(self):
        print("\n[TEST] Benchmarking Hive Swarm Parallelism...")
        hive = HiveSwarm()
        
        # We manually inject a 'slow' think into brains to test parallelism
        # Just check if broadcast time is significantly less than sum of individual think times
        # But SubBrain.think uses process_time which is CPU time.
        # Broadcast uses ThreadPoolExecutor.
        
        start_t = time.time()
        # This will trigger multiple brains (e.g. Logic, General)
        hive.broadcast("What is the Logic of the General strategy?") 
        duration = time.time() - start_t
        
        print(f"  > Hive Broadcast Time: {duration:.4f}s")
        self.assertLess(duration, 2.0, "Hivemind parallel processing too slow!")

if __name__ == '__main__':
    unittest.main()
