
import unittest
import sys
import logging
# Suppress heavy logs
logging.getLogger().setLevel(logging.CRITICAL)

from arinn_core.forge import InfinityForge
from arinn_core.quantum_swarm import QuantumSwarm
from arinn_core.apex_memory import ApexMemory

class TestApex(unittest.TestCase):
    def test_01_infinity_forge(self):
        print("\n[TEST] Verifying Infinity Forge (Real World Install)...")
        # We test installing 'requests' (safe, likely already there)
        # to prove logic runs without breaking system.
        success = InfinityForge.ensure_import("requests")
        self.assertTrue(success)
        print("  > Forge successfully verified 'requests' capability.")

    def test_02_quantum_swarm(self):
        print("\n[TEST] Verifying Quantum Swarm (Async Speed)...")
        swarm = QuantumSwarm()
        urls = ["http://example.com" for _ in range(5)]
        # We run it synchronously for test
        # We expect it might fail if aiohttp is missing, but logic should handle it.
        results = swarm.run_swarm(urls)
        print(f"  > Swarm fetched {len(results)} items.")
        self.assertEqual(len(results), 5)
        
    def test_03_apex_memory(self):
        print("\n[TEST] Verifying Apex Memory (Neuro-Symbolic)...")
        apex = ApexMemory()
        
        # Store
        apex.memorize("Singularity", "The technological point of no return.", related_to=None)
        apex.memorize("AI", "Artificial Intelligence", related_to="Singularity")
        
        # Structure Check
        related = apex.titan.associative_recall("Singularity")
        print(f"  > Graph Recall: {related}")
        
        # Vector Recall (Mock)
        # assert structure is correct
        self.assertTrue(apex.titan.graph.has_node("Singularity"))

if __name__ == '__main__':
    unittest.main()
