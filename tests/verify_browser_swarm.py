
import unittest
import os
import shutil
from arinn_core.browser_swarm import BrowserSwarm

class TestSwarm(unittest.TestCase):
    def setUp(self):
        # Create 3 dummy pages
        self.files = []
        for i in range(3):
            path = os.path.abspath(f"swarm_test_{i}.html")
            with open(path, "w") as f:
                f.write(f"<html><title>Page {i}</title><body>Target {i}</body></html>")
            self.files.append(path)
            
    def tearDown(self):
        for f in self.files:
            if os.path.exists(f):
                os.remove(f)
                
    def test_01_parallel_browsing(self):
        print("\n[TEST] Verifying Shadow Swarm...")
        swarm = BrowserSwarm(pool_size=3)
        
        urls = [f"file:///{f.replace(os.sep, '/')}" for f in self.files]
        results = swarm.swarm_urls(urls)
        
        print(f"  > Swarm Results: {results}")
        
        # Verify
        self.assertEqual(len(results), 3)
        self.assertTrue(any("Visited: Page 0" in r for r in results))
        self.assertTrue(any("Visited: Page 1" in r for r in results))
        self.assertTrue(any("Visited: Page 2" in r for r in results))

if __name__ == '__main__':
    unittest.main()
