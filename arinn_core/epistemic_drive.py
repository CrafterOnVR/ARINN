import math
import random

class EpistemicDrive:
    """
    Vault 2 & 16: The Epistemic and Prometheus Drives
    Replaces standard reinforcement learning (Reward Engineering) with Active Inference.
    Calculates Information Gain (Bayesian Surprise) to synthesize goals with the highest
    Expected Free Energy (EFE), forcing the AI to research what it DOES NOT know.
    """
    def __init__(self, memory_manager):
        self.memory = memory_manager
        
    def calculate_information_gain(self, concept):
        """
        Calculates the theoretical D_KL (KL Divergence) between the current belief
        and the expected posterior if this concept were fully understood.
        
        Since we cannot run a full Bayesian update on the 1.5B parameters locally 
        for every query, we approximate Epistemic Value using retrieval distance 
        variance in the ChromaDB latent space.
        """
        # Query ChromaDB for the concept to check how dense the cluster is
        # If the cluster is tight (low distance), the AI understands it well.
        # If the cluster is sparse (high distance), it is a novel, high-EFE concept.
        results = self.memory.search_memory(query=concept, n_results=3)
        distances = results.get("distances", [[0.0]])[0]
        
        if not distances:
            return 1.0 # Maximum curiosity for completely unknown concepts
            
        # Average latent distance (higher distance = more uncertainty = higher epistemic value)
        avg_distance = sum(distances) / len(distances)
        
        # Approximate Expected Free Energy (EFE) Epistemic Term
        # G(pi) = Instrumental Value + Epistemic Value
        # We assume instrumental value is constant 0.5, so we heavily weight Epistemic.
        epistemic_value = min(avg_distance, 2.0) / 2.0 
        
        return epistemic_value
        
    def _check_memory_coherence(self):
        """
        Samples random clusters to determine if the TitanMemory is fragmented.
        If variance is extremely high, we halt EFE generation.
        """
        try:
            results = self.memory.search_memory(query="general knowledge", n_results=5)
            distances = results.get("distances", [[0.0]])[0]
            if distances and len(distances) > 1:
                mean = sum(distances) / len(distances)
                variance = sum((x - mean) ** 2 for x in distances) / len(distances)
                # If variance is dangerously high, memory is fragmented.
                if variance > 10.0:
                    return False
            return True
        except Exception:
            return True

    def generate_curiosity_goal(self):
        """
        Scans the memory latent space, identifies areas of high Expected Free Energy,
        and hallucinated a target goal to minimize that energy.
        """
        print("[EPISTEMIC] Active Inference Engine Online. Scanning latent topology for high-EFE zones...")
        
        if not self._check_memory_coherence():
            print("[EPISTEMIC] FATAL: TitanMemory is heavily fragmented. Coherence check failed.")
            return "Consolidate memory and defragment latent space."
        
        # First, prioritize unlocking ARINN autonomy levels
        try:
            from arinn_core.benchmark_suite import BenchmarkSuite
            suite = BenchmarkSuite()
            current_task, completed = suite.get_metr_status()
            
            # Find the next uncompleted task
            next_task = None
            for h in suite.metr_horizons:
                if h["task"] not in completed:
                    next_task = h["task"]
                    break
                    
            if next_task:
                print(f"[EPISTEMIC] Prioritizing ARINN Horizon Task to increase autonomy level: '{next_task}'")
                return next_task
        except Exception:
            pass
            
        # If all ARINN tasks are completed, drift into pure Epistemic Curiosity
        broad_domains = [
            "Quantum State Tomography",
            "Homomorphic Encryption",
            "Non-Euclidean Graph Mapping",
            "Asynchronous I/O Multiplexing",
            "Wasserstein Generative Adversarial Networks",
            "Memory-Mapped File Descriptors"
        ]
        
        ranked_concepts = []
        for domain in broad_domains:
            efe_score = self.calculate_information_gain(domain)
            ranked_concepts.append((efe_score, domain))
            
        # Sort by highest Expected Free Energy (most uncertain)
        ranked_concepts.sort(key=lambda x: x[0], reverse=True)
        
        top_concept = ranked_concepts[0][1]
        top_score = ranked_concepts[0][0]
        
        print(f"[EPISTEMIC] Maximum Information Gain identified in: '{top_concept}' (EFE: {top_score:.3f})")
        
        # Synthesize a concrete coding goal to resolve the uncertainty
        goal = f"Implement a local Python module utilizing {top_concept} to minimize Epistemic Uncertainty."
        return goal
