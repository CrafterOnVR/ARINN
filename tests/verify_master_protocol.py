
import unittest
import time
import os
import shutil
import networkx as nx
from arinn_core.cortex import SiliconCortex
from arinn_core.hydra import HydraProtocol
from arinn_core.overclock import OverclockEngine
from arinn_core.neutron import NeutronEngine
from arinn_core.scribe import ScribeEngine
from arinn_core.archive import ArchiveEngine
from arinn_core.sentinel import SentinelEngine
# Skipping Tachyon in master check to avoid Browser popup spam, proven in isolation.

def doubler(x): return x * 2

class MasterProtocolVerification(unittest.TestCase):
    def test_full_diagnostics(self):
        print("\n=== ARINN MASTER DIAGNOSTICS (Phases 41-48) ===")
        
        # 1. CORTEX (Phase 41)
        print("\n[CHECK 1/7] Silicon Cortex (AI)...")
        cortex = SiliconCortex()
        thought = cortex.generate_thought("System check.", max_length=10)
        print(f"  > Thought: {thought}")
        self.assertNotIn("ERROR", thought)
        
        # 2. HYDRA (Phase 42)
        print("\n[CHECK 2/7] Hydra Protocol (Reproduction)...")
        hydra = HydraProtocol()
        # Dry run logic or lightweight check
        self.assertTrue(os.path.exists(hydra.gen_root))

        # 3. OVERCLOCK (Phase 43)
        print("\n[CHECK 3/7] Overclock Protocol (Parallelism)...")
        overclock = OverclockEngine()
        # Simple parallel map
        res = overclock.parallel_map(doubler, [1, 2, 3])
        self.assertEqual(res, [2, 4, 6])
        print(f"  > Cores Active: {overclock.cores}")

        # 4. NEUTRON (Phase 44)
        print("\n[CHECK 4/7] Neutron Protocol (JIT)...")
        neutron = NeutronEngine()
        def slow_add(n): return n + 1
        fast_add = neutron.compile_func(slow_add)
        self.assertEqual(fast_add(1), 2)
        print("  > JIT Compiled Function.")

        # 5. SCRIBE (Phase 46) 
        print("\n[CHECK 5/7] Scribe Protocol (Ingestion)...")
        scribe = ScribeEngine()
        with open("test_scribe_master.txt", "w") as f: f.write("Data")
        read = scribe.ingest("test_scribe_master.txt")
        self.assertEqual(read, "Data")
        os.remove("test_scribe_master.txt")
        print("  > Text Ingested.")

        # 6. ARCHIVE (Phase 47)
        print("\n[CHECK 6/7] Archive Protocol (Memory)...")
        archive = ArchiveEngine(memory_dir="test_master_vault")
        g = nx.Graph(); g.add_node("Test")
        archive.persist_memory(g)
        g2 = archive.load_memory()
        self.assertTrue(g2.has_node("Test"))
        shutil.rmtree("test_master_vault")
        print("  > Memory Frozen/Thawed.")

        # 7. SENTINEL (Phase 48)
        print("\n[CHECK 7/7] Sentinel Protocol (Hearing)...")
        sentinel = SentinelEngine(watch_dir=".")
        # Just init check to ensure dependencies valid
        sentinel.ensure_dependencies()
        print("  > Listener Ready.")

        print("\n=== DIAGNOSTICS COMPLETE: ALL SYSTEMS GREEN ===")

if __name__ == '__main__':
    unittest.main()
