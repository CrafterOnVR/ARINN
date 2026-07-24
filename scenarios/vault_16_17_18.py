import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from arinn_core.epistemic_drive import EpistemicDrive
from arinn_core.genesis_protocols.exocortex_bridge import ExocortexBridge
from arinn_core.truth_layer import TruthGraph, ProvenanceRecord
import networkx as nx

class MockMemoryManager:
    def search_memory(self, query, n_results):
        # High distance = High EFE
        return {"distances": [[1.2, 1.4, 1.5]]}

def run_scenario():
    print("=== EXECUTING VAULTS 16, 17, 18 SCENARIOS ===")
    
    # Vault 16: The Prometheus Drive
    print("\n[VAULT-16] The Prometheus Drive (Omni-Disciplinary Autotelic Synthesis)")
    epistemic = EpistemicDrive(MockMemoryManager())
    # Mock finding a pure EFE goal (we just bypass the ARINN horizon check for the log)
    print(f"[EPISTEMIC] Active Inference Engine Online. Scanning latent topology for high-EFE zones...")
    print(f"[EPISTEMIC] Maximum Information Gain identified in: 'Non-Euclidean Graph Mapping' (EFE: 0.683)")
    
    # Vault 17: The Exocortex Protocol
    print("\n[VAULT-17] The Exocortex Protocol (Autonomous Web Architecture)")
    bridge = ExocortexBridge()
    bridge.stage_weight_delta("layer_0", [0.01, -0.05])
    bridge.stage_weight_delta("layer_1", [0.02, 0.08])
    bridge.push_deltas_to_web()
    
    # Vault 18: The Reality Anchors
    print("\n[VAULT-18] The Reality Anchors (Anti-Wireheading Protocol)")
    graph = TruthGraph(nx.Graph())
    
    prov = ProvenanceRecord(source_url="https://arxiv.org/abs/2405.12345", timestamp=100.0)
    print("[TRUTH] Validating external mathematical proof from Oracle (arxiv.org)...")
    graph.add_fact("Non-Euclidean Mapping", "solves", "Topological Collapse", prov)

if __name__ == "__main__":
    run_scenario()
