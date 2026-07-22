import ast
import math

class SpatialLogicMapper:
    """
    Vault 4: Topological Logic Mapping (The 3D Code Mind)
    Maps raw Python AST into a non-Euclidean (Hyperbolic) Poincaré ball manifold.
    This allows the AI to calculate the semantic "distance" between two pieces 
    of code based on structural depth rather than linear token distance.
    """
    def __init__(self):
        self.nodes = {}
        
    def _parse_ast_depth(self, node, current_depth=0):
        """Recursively parses AST and assigns structural depth."""
        parsed = []
        for child in ast.iter_child_nodes(node):
            node_type = type(child).__name__
            # Only track major structural nodes to save memory
            if node_type in ['FunctionDef', 'ClassDef', 'AsyncFunctionDef', 'If', 'For', 'While']:
                name = getattr(child, 'name', f"Unnamed_{node_type}_{id(child)}")
                parsed.append({
                    "name": name,
                    "type": node_type,
                    "depth": current_depth + 1
                })
            parsed.extend(self._parse_ast_depth(child, current_depth + 1))
        return parsed
        
    def map_code_to_poincare(self, source_code: str):
        """
        Parses source code into AST and maps it mathematically.
        """
        try:
            tree = ast.parse(source_code)
            structure = self._parse_ast_depth(tree)
            
            # Map depths to a simplified radial distance in a Poincaré ball
            # Values approach 1.0 (the boundary) as depth increases exponentially
            poincare_map = []
            for item in structure:
                r = 1.0 - math.exp(-0.5 * item["depth"])
                # We assign a pseudo-random angle (theta) just for the theoretical 2D projection
                theta = (hash(item["name"]) % 360) * (math.pi / 180.0)
                x = r * math.cos(theta)
                y = r * math.sin(theta)
                
                poincare_map.append({
                    "name": item["name"],
                    "r": r,
                    "x": x,
                    "y": y,
                    "depth": item["depth"]
                })
                
            print(f"[VAULT-4] Successfully mapped {len(poincare_map)} structural nodes into Hyperbolic Space.")
            return poincare_map
            
        except Exception as e:
            print(f"[VAULT-4] AST Parsing failed: {e}")
            return []

    def calculate_hyperbolic_distance(self, node_a, node_b):
        """
        Calculates the distance between two AST nodes in the Poincaré ball manifold.
        d(x,y) = arcosh(1 + 2 * ||x-y||^2 / ((1-||x||^2)(1-||y||^2)))
        """
        def norm_sq(node):
            return node['x']**2 + node['y']**2
            
        def dist_sq(n1, n2):
            return (n1['x'] - n2['x'])**2 + (n1['y'] - n2['y'])**2
            
        ns_a = norm_sq(node_a)
        ns_b = norm_sq(node_b)
        
        # Prevent division by zero if nodes are exactly on the boundary
        if ns_a >= 1.0 or ns_b >= 1.0:
            return float('inf')
            
        delta = 2 * dist_sq(node_a, node_b) / ((1 - ns_a) * (1 - ns_b))
        
        # arcosh(x) = ln(x + sqrt(x^2 - 1))
        x = 1 + delta
        # Using math.acosh for numerical stability
        dist = math.acosh(max(1.0, x))
        
        return dist
