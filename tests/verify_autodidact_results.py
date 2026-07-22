
import unittest
from arinn_core.archive import ArchiveEngine

class TestAutodidact(unittest.TestCase):
    def test_autonomous_learning(self):
        print("\n[TEST] Verifying Autodidact Protocol (Result Inspection)...")
        
        archive = ArchiveEngine()
        graph = archive.load_memory()
        
        # Check for Lesson 3 Concepts
        # "Python is a Language" -> Python, Language
        # "Efficiency is Automation" -> Efficiency, Automation
        
        has_python = graph.has_node("Python")
        has_efficiency = graph.has_node("Efficiency")
        
        print(f"  > Memory contains 'Python'? {has_python}")
        print(f"  > Memory contains 'Efficiency'? {has_efficiency}")
        
        self.assertTrue(has_python, "Failed to learn 'Python' autonomously.")
        self.assertTrue(has_efficiency, "Failed to learn 'Efficiency' autonomously.")
        
        # Check Edge
        if has_python:
            has_edge = graph.has_edge("Python", "Language")
            print(f"  > Edge 'Python -> Language' exists? {has_edge}")
            self.assertTrue(has_edge)
            
        print("  > Autodidact Protocol Verified.")

if __name__ == '__main__':
    unittest.main()
