
import re
from arinn_core.scribe import ScribeEngine
from arinn_core.archive import ArchiveEngine

class ScholarEngine:
    """
    Phase 56: The Scholar Protocol.
    Deep Technical Ingestion.
    """
    def __init__(self):
        self.scribe = ScribeEngine()
        self.archive = ArchiveEngine()
        self.memory_graph = self.archive.load_memory()
        
    def study(self, filepath):
        print(f"\n[SCHOLAR] Studying: {filepath}")
        content = self.scribe.ingest(filepath)
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        
        count = 0
        for sent in sentences:
            # Pattern 1: Definition ("X is a Y")
            # Pattern 2: Usage ("To define X use Y")
            
            # Heuristic for "Usage/Syntax"
            usage_match = re.search(r"To define ([\w\s]+) use the ([\w\s]+) keyword", sent, re.IGNORECASE)
            if usage_match:
                concept = usage_match.group(1).strip().title()
                keyword = usage_match.group(2).strip().lower() # keywords are code
                
                self.memory_graph.add_node(concept, type="technical_concept")
                self.memory_graph.add_node(keyword, type="keyword")
                self.memory_graph.add_edge(concept, keyword, relation="uses_keyword")
                print(f"  > Learned Syntax: {concept} --[uses_keyword]--> {keyword}")
                count += 1
                continue
                
            # Heuristic for "Definition"
            def_match = re.search(r"([\w\s]+) is ([\w\s]+)", sent, re.IGNORECASE)
            if def_match:
                subj = def_match.group(1).strip().title()
                obj = def_match.group(2).strip()
                
                self.memory_graph.add_node(subj, type="technical_concept")
                self.memory_graph.add_edge(subj, obj, relation="is_defined_as")
                print(f"  > Learned Definition: {subj} --[is_defined_as]--> {obj}")
                count += 1
                continue
                
        print(f"[SCHOLAR] Study Session Complete. {count} Technical Facts Absorbed.")
        self.archive.persist_memory(self.memory_graph)

if __name__ == "__main__":
    scholar = ScholarEngine()
    scholar.study("arinn_education/advanced_python.txt")
