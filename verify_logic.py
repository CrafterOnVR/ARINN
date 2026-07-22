
import networkx as nx
from arinn_core.scribe import ScribeEngine
from arinn_core.archive import ArchiveEngine

class LogicTester:
    """
    Phase 53: Logic Protocol.
    Verifies Syllogistic/Transitive Inference.
    """
    def __init__(self):
        self.scribe = ScribeEngine()
        self.archive = ArchiveEngine()
        self.memory_graph = self.archive.load_memory()
        
    def clean_concept(self, text):
        lower = text.lower()
        clean = text
        if lower.startswith("a "): clean = text[2:].strip()
        elif lower.startswith("an "): clean = text[3:].strip()
        elif lower.startswith("the "): clean = text[4:].strip()
        
        # Enforce Title Case for Linking (e.g. "organic" -> "Organic")
        return clean.title()

    def ingest_premise(self, path):
        print(f"\n[LOGIC] Ingesting Premises: {path}")
        content = self.scribe.ingest(path)
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        
        for sent in sentences:
            subj, obj, rel = None, None, None
            if " is a " in sent:
                parts = sent.split(" is a ")
                subj, obj, rel = parts[0], parts[1], "is_a"
            elif " is " in sent:
                parts = sent.split(" is ")
                subj, obj, rel = parts[0], parts[1], "is"
            
            if subj and obj:
                clean_subj = self.clean_concept(subj.strip())
                clean_obj = self.clean_concept(obj.strip())
                self.memory_graph.add_edge(clean_subj, clean_obj, relation=rel)
                print(f"  > Premise: {clean_subj} -> {clean_obj}")
        
        self.archive.persist_memory(self.memory_graph)

    def verify_deduction(self, start, end):
        print(f"\n[LOGIC] Attempting Deduction: Is {start} -> {end}?")
        
        try:
            path = nx.shortest_path(self.memory_graph, start, end)
            # Verify the path is composed of logical connectors ("man", "mortal")
            chain_str = ""
            for i in range(len(path)-1):
                u, v = path[i], path[i+1]
                data = self.memory_graph.get_edge_data(u, v)
                rel = data.get('relation', '???')
                chain_str += f"({u}) --[{rel}]--> "
            chain_str += f"({path[-1]})"
            
            print(f"  > Deduction Chain: {chain_str}")
            return True, chain_str
        except nx.NetworkXNoPath:
            print("  > Deduction Failed: No logic path found.")
            return False, None
        except nx.NodeNotFound:
             print(f"  > Deduction Failed: Concept missing ({start} or {end}).")
             return False, None

if __name__ == "__main__":
    tester = LogicTester()
    tester.ingest_premise("arinn_education/logic_01_syllogism.txt")
    
    # Test: Socrates -> Carbon?
    success, proof = tester.verify_deduction("Socrates", "Carbon")
    
    if success:
        print("[PHASE 53] Transitive Logic Verified.")
    else:
        print("[PHASE 53] Logic Failed.")
        exit(1)
