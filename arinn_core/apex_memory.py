
import logging
from .titan_memory import TitanMemory
# We reuse LanguageCorpus for vector storage
from .language_corpus import LanguageCorpus

class ApexMemory:
    """
    Phase 37: Apex Memory (Hybrid Intelligence).
    Fuses Titan (Graph) with Vector (Embedding).
    Enables Neuro-Symbolic Reasoning.
    """
    def __init__(self):
        self.titan = TitanMemory()
        self.vectors = LanguageCorpus()
        
    def memorize(self, concept, text_content, related_to=None):
        """
        Stores a memory in BOTH systems.
        """
        # 1. Store in Titan (Structure)
        self.titan.add_concept(concept, content=text_content)
        if related_to:
            self.titan.link_concepts(related_to, concept, "relates_to")
            
        # 2. Store in Vector DB (Semantic)
        # We store the 'concept' name as metadata or content
        self.vectors.ingest_text(text_content, source=concept)
        print(f"[APEX] Encoded '{concept}' into Neuro-Symbolic Matrix.")
        
    def neuro_symbolic_recall(self, query):
        """
        Hybrid Recall:
        1. Vector Search finds semantically relevant nodes.
        2. Graph Traversal expands to structural neighbors.
        """
        print(f"[APEX] Querying Matrix: '{query}'")
        
        # 1. Vector Search
        # Returns list of matched documents (which contain our concepts)
        vector_hits = self.vectors.query(query, n_results=3)
        # Extract concept names (assuming stored in source or content matches)
        # Simplified: we assume the 'source' metadata holds the concept name
        
        # Mocking extraction for demo since LanguageCorpus return format varies
        # Ideally we parse vector_hits
        print(f"[APEX] Vector Matches: {len(vector_hits)} semantic hits.")
        
        # 2. Graph Expansion
        results = []
        for hit in vector_hits:
            concept = hit if isinstance(hit, str) else hit.get('metadata', {}).get('source', str(hit))
            neighbors = self.titan.associative_recall(concept)
            results.append({"concept": concept, "related": neighbors})
            
        return results
