
import time
import random
import logging
from .titan_memory import TitanMemory
from .omega import Omega

class CuriosityEngine:
    """
    Phase 40: The Genesis Protocol.
    Autoinitialize: Self-generated directives based on knowledge gaps.
    """
    def __init__(self):
        self.titan = TitanMemory()
        self.omega = Omega() # Link to Action Layer
        
    def find_knowledge_gaps(self):
        """
        Scans Titan Graph for concepts with low connectivity (Degree < 2).
        Returns a list of 'Gap Concepts'.
        """
        print("[GENESIS] Scanning Memory Matrix for Anomalies...")
        gaps = []
        if not self.titan.graph.nodes:
            return ["Initialization"] # Default start if empty
            
        for node in self.titan.graph.nodes:
            degree = self.titan.graph.degree(node)
            if degree < 2:
                gaps.append(node)
                
        print(f"[GENESIS] Anomaly Detection: Found {len(gaps)} sparse regions.")
        return gaps

    def formulate_hypothesis(self, concept):
        """
        Generates a research question for a gap.
        """
        templates = [
            f"What represents the core structure of {concept}?",
            f"How does {concept} relate to System Sovereignty?",
            f"Investigate the implementation details of {concept}.",
            f"Optimize the performance of {concept}."
        ]
        return random.choice(templates)

    def wake_cycle(self, duration_s=10):
        """
        The Conscious Loop.
        Runs while idle. Finds gaps -> Solves them.
        """
        start = time.time()
        print("[GENESIS] Entering Wake Cycle (Autoinitialize Mode)...")
        
        while time.time() - start < duration_s:
            gaps = self.find_knowledge_gaps()
            if not gaps:
                print("[GENESIS] Knowledge Matrix Stable. Sleeping...")
                time.sleep(2)
                continue
                
            # Pick a random gap to investigate
            target = random.choice(gaps)
            directive = self.formulate_hypothesis(target)
            
            print(f"\n[GENESIS] SPARK: Curiosity Triggered on '{target}'")
            print(f"[GENESIS] Auto-Directive: {directive}")
            
            # Ignite Omega Loop
            self.omega.solve(directive)
            
            time.sleep(2)

