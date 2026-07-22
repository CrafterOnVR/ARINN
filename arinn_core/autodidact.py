
import os
import time
import networkx as nx
from arinn_core.scribe import ScribeEngine
from arinn_core.archive import ArchiveEngine
from arinn_core.sentinel import SentinelEngine

class AutodidactEngine:
    """
    Phase 52: The Autodidact Protocol.
    Self-Directed Learning Loop.
    """
    def __init__(self, education_dir="arinn_education"):
        self.education_dir = education_dir
        if not os.path.exists(self.education_dir):
            os.makedirs(self.education_dir, exist_ok=True)
            
        self.scribe = ScribeEngine()
        self.archive = ArchiveEngine()
        self.memory_graph = self.archive.load_memory()
        self.processed_files = set()
        
    def clean_concept(self, text):
        # Canonicalization logic (Same as Foundation Teacher)
        lower = text.lower()
        if lower.startswith("a "): return text[2:].strip()
        if lower.startswith("an "): return text[3:].strip()
        if lower.startswith("the "): return text[4:].strip()
        return text

    def digest(self, filepath):
        print(f"\n[AUTODIDACT] Consuming: {filepath}")
        content = self.scribe.ingest(filepath)
        
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        new_edges = []
        
        for sent in sentences:
            # Reusing robust parser from Phase 49
            subj, obj, rel = None, None, None
            
            if " is a " in sent:
                parts = sent.split(" is a ")
                subj, obj, rel = parts[0], parts[1], "is_a"
            elif " is " in sent:
                parts = sent.split(" is ")
                subj, obj, rel = parts[0], parts[1], "is"
            elif " contains " in sent:
                parts = sent.split(" contains ")
                subj, obj, rel = parts[0], parts[1], "contains"
            elif " digs for " in sent:
                parts = sent.split(" digs for ")
                subj, obj, rel = parts[0], parts[1], "digs_for"
            
            if subj and obj:
                clean_subj = self.clean_concept(subj.strip())
                clean_obj = self.clean_concept(obj.strip())
                
                self.memory_graph.add_node(clean_subj, type="concept")
                self.memory_graph.add_node(clean_obj, type="concept")
                self.memory_graph.add_edge(clean_subj, clean_obj, relation=rel)
                new_edges.append((clean_subj, clean_obj, rel))
                print(f"  > Learned: {clean_subj} --[{rel}]--> {clean_obj}")
        
        print(f"[AUTODIDACT] Digestion Complete. {len(new_edges)} Facts Learned.")
        self.archive.persist_memory(self.memory_graph)
        return new_edges

    def self_quiz(self, edges):
        print("[AUTODIDACT] Starting Self-Quiz (Reinforcement)...")
        score = 0
        for subj, obj, rel in edges:
            print(f"  > Q: What is relation between '{subj}' and '{obj}'?")
            # Graph Verification
            if self.memory_graph.has_edge(subj, obj):
                actual_rel = self.memory_graph.get_edge_data(subj, obj)['relation']
                if actual_rel == rel:
                    print("  > A: Correct.")
                    score += 1
                else:
                    print(f"  > A: Wrong (Expected {rel}, Got {actual_rel}).")
            else:
                print("  > A: Failed (Target Link Missing).")
        
        print(f"[AUTODIDACT] Quiz Result: {score}/{len(edges)}")

    def start_loop(self):
        print(f"[AUTODIDACT] Online. Watching '{self.education_dir}'.")
        print("[AUTODIDACT] Press Ctrl+C to stop learning.")
        
        # Mark existing files as processed so we don't re-read old ones instantly
        # (Unless we want to re-reinforce, but for now assume fresh start = fresh read of new files)
        # Actually, let's process everything that hasn't been processed in this session scope.
        
        try:
            while True:
                files = [f for f in os.listdir(self.education_dir) if f.endswith(".txt")]
                
                for f in files:
                    full_path = os.path.join(self.education_dir, f)
                    if full_path not in self.processed_files:
                        # New knowledge found!
                        learned_edges = self.digest(full_path)
                        if learned_edges:
                            self.self_quiz(learned_edges)
                        self.processed_files.add(full_path)
                
                time.sleep(2) # Breath
                
        except KeyboardInterrupt:
            print("\n[AUTODIDACT] Offline. Learning session ended.")

if __name__ == "__main__":
    engine = AutodidactEngine()
    engine.start_loop()
