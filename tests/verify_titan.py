
import unittest
from arinn_core.titan_memory import TitanMemory

class TestTitan(unittest.TestCase):
    def test_01_graph_logic(self):
        print("\n[TEST] Verifying Titan Memory (Graph)...")
        titan = TitanMemory()
        
        # 1. Add Nodes
        titan.add_concept("Physics", type="science")
        titan.add_concept("Entropy", type="concept")
        titan.add_concept("Heat Death", type="theory")
        
        # 2. Link
        print("  > Linking Concepts: Physics -> Entropy -> Heat Death")
        titan.link_concepts("Physics", "Entropy", "implies")
        titan.link_concepts("Entropy", "Heat Death", "leads_to")
        
        # 3. Pathfinding
        path = titan.find_path("Physics", "Heat Death")
        print(f"  > Path Found: {path}")
        
        self.assertIsNotNone(path)
        self.assertEqual(path, ["Physics", "Entropy", "Heat Death"])
        
        # 4. Recall
        neighbors = titan.associative_recall("Entropy")
        self.assertIn("Heat Death", neighbors)
        print("  > Associative Recall verified.")

if __name__ == '__main__':
    unittest.main()
