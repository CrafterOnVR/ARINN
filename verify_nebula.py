
import unittest
import time
import requests
from arinn_core.nebula_core import NebulaCore

class TestNebula(unittest.TestCase):
    def test_01_distributed_mesh(self):
        print("\n[TEST] Verifying Nebula Protocol (Distributed Mesh)...")
        
        # 1. Start Core
        core = NebulaCore()
        core.start_server()
        time.sleep(1) # Let server bind
        
        # 2. Expand Mesh (Launch 2 Real Terminals)
        core.expand_mesh(count=2)
        
        # Give nodes time to boot and register
        print("  > Waiting for Satellites to align...")
        time.sleep(3)
        
        # 3. Distribute Work
        print("  > Broadcasting Directives to Mesh...")
        core.queue_task("RESEARCH", "Quantum Computing")
        core.queue_task("RESEARCH", "Neural Networks")
        
        # 4. Wait for Intel (Polling core results)
        print("  > Awaiting Distributed Intel...")
        start = time.time()
        while len(core.results) < 2:
            time.sleep(1)
            if time.time() - start > 10:
                print("  > Timeout waiting for nodes.")
                break
                
        # 5. Verify
        print(f"  > Intel Received: {len(core.results)} packets.")
        print(f"  > Data: {core.results}")
        
        # Cleanup
        core.stop()
        
        self.assertGreaterEqual(len(core.results), 2)

if __name__ == '__main__':
    unittest.main()
