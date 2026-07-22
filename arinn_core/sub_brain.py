
import time
import logging
from collections import deque
from .neural_core import NeuralCore  # type: ignore

class SubBrain:
    """
    A single independent cognitive agent.
    There are 20 of these in the Hivemind.
    Features:
    - Predictive Coding
    - Fast/Slow Modes
    - Hard-Limited Working Memory
    - Energy Awareness
    - Internal Narrator
    """
    def __init__(self, brain_id, domain, genome=None):
        self.id = brain_id
        self.domain = domain
        self.core = NeuralCore()
        
        # Apply Genome or Defaults
        self.genome = genome.genes if genome else {
            "perplexity_threshold": 0.8,
            "attention_budget": 7,
            "curiosity_factor": 0.5
        }
        
        # 5. Hard-Limited Working Memory (Limit from Genome)
        self.working_memory = deque(maxlen=int(self.genome["attention_budget"]))
        self.long_term_summary = ""
        
        # 1. Predictive Coding / 9. Confidence
        self.prediction_error = 0.0
        self.confidence = 0.5
        
        # 7. Energy / Compute Awareness
        self.energy_cost = 0.0
        
        # 4. Fast vs Slow Thinking
        self.mode = "FAST" # Starts in heuristic mode
        
        # 8. Internal Narrator
        self.internal_monologue = "Initialized."
        
    def perceive(self, stimulus):
        """
        3. Sparse Activation Check.
        Returns True if stimulus is relevant to this brain's domain.
        """
        # Predictive check: Do I recognize this pattern?
        relevance = 0.0
        if self.domain.lower() in stimulus.lower():
            relevance = 1.0
            
        # If General domain, we always pay a little attention
        if self.domain == "General":
            relevance = max(relevance, 0.6)
        
        # Surprise / Curiosity
        surprise = self.core.measure_perplexity(stimulus)
        
        # Activation Rules (Evolving Thresholds):
        activate = False
        threshold = self.genome["perplexity_threshold"]
        curiosity = self.genome["curiosity_factor"]
        
        if relevance > threshold:
            activate = True
        elif surprise > threshold and relevance > (1.0 - curiosity):
            activate = True
            
        return activate
        
    def think(self, input_data):
        """
        Main Cognitive Loop.
        Decides Fast vs Slow based on prediction error.
        """
        start_t = time.process_time()
        
        # 1. Predictive Coding: Predict outcome
        surprise = self.core.measure_perplexity(input_data)
        self.prediction_error = surprise
        
        # 4. Switch Mode
        if surprise > 0.7:
             self.mode = "SLOW" # Novelty triggers deliberation
        else:
             self.mode = "FAST" # Routine triggers heuristic
             
        # Process
        if self.mode == "FAST":
            thought = self._think_fast(input_data)
        else:
            thought = self._think_slow(input_data)
            
        # 6. Concept reasoning (Graph/Abstraction)
        self.working_memory.append(thought)
        
        # 7. Cost Tracking
        self.energy_cost += (time.process_time() - start_t)
        
        # 8. Narrate
        self.internal_monologue = f"I chose {self.mode} mode because surprise was {surprise:.2f}. Thought: {thought}"
        
        return thought
        
    def _think_fast(self, input_data):
        """Heuristic Association."""
        # Simple domain stamp
        return f"[{self.domain}:Fast] Recognized pattern in '{input_data[:20]}...'"
        
    def _think_slow(self, input_data):
        """Deliberative Neural Generation."""
        # 2. Abstraction Engine: Compress input
        context = f"Domain: {self.domain}. Input: {input_data}. Analysis:"
        # Real Neural Generation
        thought, cost = self.core.generate_thought(context)
        return f"[{self.domain}:Slow] {thought}"
        
    def report_status(self):
        """14. Diagnosis"""
        return {
            "id": self.id,
            "domain": self.domain,
            "mode": self.mode,
            "error": self.prediction_error,
            "memory": len(self.working_memory),
            "narrative": self.internal_monologue
        }
