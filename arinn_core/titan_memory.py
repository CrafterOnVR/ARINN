
import networkx as nx
import logging

class TitanMemory:
    """
    Phase 34: The Titan Memory.
    A holographic knowledge graph connecting disparate concepts.
    Replaces linear lists with relational understanding.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def add_concept(self, name, type="general", content=""):
        """Adds a node to the graph."""
        if name not in self.graph:
            self.graph.add_node(name, type=type, content=content)
            logging.info(f"[TITAN] Learned concept: {name}")
            
    def link_concepts(self, source, target, relation="related_to"):
        """Creates an edge."""
        if source not in self.graph or target not in self.graph:
            logging.warning(f"[TITAN] Cannot link unknown concepts: {source}->{target}")
            return
            
        self.graph.add_edge(source, target, relation=relation)
        logging.info(f"[TITAN] Linked {source} --{relation}--> {target}")
        
    def associative_recall(self, concept, depth=1):
        """
        Returns neighbors of the concept. "What does this remind me of?"
        """
        if concept not in self.graph:
            return []
            
        # Get immediate neighbors
        neighbors = list(self.graph.successors(concept))
        # Simple depth 1 support
        return neighbors
        
    def find_path(self, start, end):
        """
        Finds the logical chain between two ideas.
        "How is Python related to Gravity?"
        """
        try:
            path = nx.shortest_path(self.graph, start, end)
            return path
        except nx.NetworkXNoPath:
            return None
        except Exception:
            return None
