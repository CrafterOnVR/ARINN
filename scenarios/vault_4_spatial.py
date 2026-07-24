import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from arinn_core.spatial_logic import SpatialLogicMapper

def run_scenario():
    print("=== EXECUTING VAULT 4 (Topological Logic Mapping) SCENARIO ===")
    
    sample_code = """
class NeuralNetwork:
    def __init__(self):
        self.layers = []
        
    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
            if x is None:
                return None
        return x
    """
    
    mapper = SpatialLogicMapper()
    print("[VAULT-4] Parsing autoregressive token stream into Hyperbolic Manifold...")
    poincare_map = mapper.map_code_to_poincare(sample_code)
    
    if len(poincare_map) >= 2:
        node_a = poincare_map[0]
        node_b = poincare_map[-1]
        
        print(f"[VAULT-4] Node A: {node_a['name']} (Depth: {node_a['depth']})")
        print(f"[VAULT-4] Node B: {node_b['name']} (Depth: {node_b['depth']})")
        
        distance = mapper.calculate_hyperbolic_distance(node_a, node_b)
        print(f"[VAULT-4] Semantic non-Euclidean distance calculated: {distance:.4f}")

if __name__ == "__main__":
    run_scenario()
