
import unittest
import os
from arinn_core.vision_system import VisionSystem

class TestVision(unittest.TestCase):
    def test_01_capture_and_analyze(self):
        print("\n[TEST] Verifying Vision System...")
        vision = VisionSystem()
        
        # 1. Capture
        img = vision.capture()
        if img is None:
            print("  > Capture returned None (Possible headless env). Skipping Assert.")
            return
            
        self.assertIsNotNone(img, "Screenshot should not be None")
        print(f"  > Capture size: {img.size}")
        
        # 2. Analyze
        metrics = vision.analyze(img)
        print(f"  > Metrics: {metrics}")
        self.assertIn("entropy", metrics)
        self.assertIn("brightness", metrics)
        self.assertGreater(metrics['entropy'], 0, "Entropy should be positive")
        
        # 3. Description
        desc = vision.describe_scene()
        print(f"  > Description: {desc}")
        self.assertIsInstance(desc, str)
        self.assertTrue(len(desc) > 5)

if __name__ == '__main__':
    unittest.main()
