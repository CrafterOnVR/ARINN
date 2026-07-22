
import time
import math
import networkx as nx # pyre-ignore
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional

# Constants
W_SOURCE = 0.4
W_CROSS = 0.4
W_TIME = 0.2

@dataclass
class ProvenanceRecord:
    source_url: str
    timestamp: float
    author: str = "Unknown"
    cross_verified_by: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "source_url": self.source_url,
            "timestamp": self.timestamp,
            "author": self.author,
            "cross_verified_by": self.cross_verified_by
        }

class ConfidenceScorer:
    """
    Calculates reliability score (0.0 - 1.0).
    """
    @staticmethod
    def calculate(provenance: ProvenanceRecord) -> float:
        # 1. Source Reputation
        r_source = 0.1
        if "arxiv.org" in provenance.source_url or "python.org" in provenance.source_url:
            r_source = 1.0
        elif provenance.source_url.startswith("https://"):
            r_source = 0.5
            
        # 2. Cross Validation
        v_cross = 0.5
        if provenance.cross_verified_by:
            count = len(provenance.cross_verified_by)
            v_cross = 1.0 if count >= 2 else 0.5 + (count * 0.2)
            
        # 3. Time Decay
        # Age in years
        age_seconds = time.time() - provenance.timestamp
        age_years = age_seconds / (365 * 24 * 3600)
        d_time = 1.0 / (1.0 + math.log(1.0 + age_years))
        
        score = (W_SOURCE * r_source) + (W_CROSS * v_cross) + (W_TIME * d_time)
        return round(float(min(1.0, score)), 3) # pyre-ignore

class TruthGraph:
    """
    Wrapper for Titan Memory that enforces Truth/Provenance.
    """
    def __init__(self, nx_graph: nx.Graph):
        self.graph = nx_graph
        
    def add_fact(self, subject, relation, object_, provenance: ProvenanceRecord):
        """
        Adds a fact with mandatory provenance.
        """
        confidence = ConfidenceScorer.calculate(provenance)
        
        # Add Nodes
        self.graph.add_node(subject, confidence=confidence, provenance=provenance.to_dict())
        self.graph.add_node(object_, confidence=confidence, provenance=provenance.to_dict())
        
        # Add Edge
        self.graph.add_edge(subject, object_, relation=relation, confidence=confidence)
        
        print(f"[TRUTH] Learned: {subject} -> {relation} -> {object_} (Conf: {confidence})")
        return confidence
        
    def garbage_collect(self, threshold=0.3):
        """
        Prunes low-confidence knowledge.
        """
        to_remove = []
        for node, data in self.graph.nodes(data=True):
            conf = data.get('confidence', 0.1) # Default low if missing
            if conf < threshold:
                to_remove.append(node)
                
        if to_remove:
            print(f"[TRUTH] Reaper Pruning {len(to_remove)} low-confidence facts...")
            self.graph.remove_nodes_from(to_remove)
            
        return len(to_remove)
