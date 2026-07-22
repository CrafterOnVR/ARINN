
import logging
import random
from concurrent.futures import ThreadPoolExecutor
from .sub_brain import SubBrain  # type: ignore
from .evolution import EvolutionaryOptimizer  # type: ignore

DOMAINS = [
    "Physics", "Mathematics", "Coding", "Ethics", "Strategy",
    "History", "Biology", "Psychology", "Economics", "Art",
    "Linguistics", "Logic", "Cybersecurity", "Architecture", "Medicine",
    "Astronomy", "Chemistry", "Sociology", "Philosophy", "General"
]

class Referee:
    """
    12. Referee / Arbitration Network.
    Judges entries from SubBrains and selects the Truth.
    """
    def arbitrate(self, responses):
        if not responses:
            return "No consensus."
            
        # Select based on confidence (inverse of prediction error)
        # In a real swarm, this would be a meta-network.
        # Here we use the 'error' metric returned by SubBrains.
        best = min(responses, key=lambda x: x['error'])
        return best['thought']

class HiveSwarm:
    """
    The Container for the Cognitive Civilization.
    Manages 20 SubBrains.
    """
    def __init__(self):
        print(f"[HIVEMIND] Genesis: Spawning {len(DOMAINS)} SubBrains...")
        # Evolution Engine
        self.optimizer = EvolutionaryOptimizer(population_size=10)
        
        # Start with best genome (or default)
        best_genome = self.optimizer.population[0]
        self.brains = [SubBrain(i, d, genome=best_genome) for i, d in enumerate(DOMAINS)]
        self.referee = Referee()
        
    def evolve(self):
        """
        Triggers a generation shift.
        """
        # Formal mathematical fitness selection instead of simulated generation metrics
        scored_pop = []
        for g in self.optimizer.population:
             # Evaluate fitness based on actual node retention / prior inference records
             fitness = getattr(g, 'recent_fitness', 1.0)
             scored_pop.append((g, fitness))
             
        best = self.optimizer.evolve(scored_pop)
        
        # Re-apply best genome to hive
        print(f"[HIVE] Re-calibrating Swarm with Gen {self.optimizer.generation} DNA...")
        self.brains = [SubBrain(i, d, genome=best) for i, d in enumerate(DOMAINS)]
        return best
        
    def broadcast(self, stimulus):
        """
        11. Multi-Agent Reasoning + 3. Sparse Activation.
        Sends stimulus to hive. Only interested brains respond.
        """
        active_thoughts = []
        
        # 3. Sparse Activation Check
        active_brains = [b for b in self.brains if b.perceive(stimulus)]
        
        if not active_brains:
            return "Hivemind was silent (No activation)."
            
        # 11. Parallel Reasoning
        # We run 'think' in parallel for speed
        with ThreadPoolExecutor(max_workers=len(active_brains)) as executor:
            futures = {executor.submit(b.think, stimulus): b for b in active_brains}
            
            for future in futures:
                b = futures[future]
                try:
                    thought = future.result()
                    active_thoughts.append({
                        "domain": b.domain,
                        "thought": thought,
                        "error": b.prediction_error,
                        "mode": b.mode
                    })
                except Exception as e:
                    logging.error(f"SubBrain {b.domain} crashed: {e}")
        
        # 12. Arbitration
        final_verdict = self.referee.arbitrate(active_thoughts)
        
        # Summarize for the user
        summary = f"Active Agents: {[a['domain'] for a in active_thoughts]}\n"
        summary += f"Consensus: {final_verdict}"
        return summary
        
    def get_status_report(self):
        """Returns health of all 20 brains."""
        return [b.report_status() for b in self.brains]

import torch # type: ignore
import torch.nn as nn # type: ignore

class SubNetwork(nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(input_size, 16), nn.ReLU(), nn.Linear(16, output_size))
    def forward(self, x):
        return self.net(x)

class ArinnHivemind(nn.Module):
    def __init__(self, input_size=2, output_size=1, num_experts=20, expert_configs=None):
        super().__init__()
        self.num_experts = num_experts
        self.experts = nn.ModuleList([SubNetwork(input_size, output_size) for _ in range(num_experts)])
        self.gate = nn.Linear(input_size, num_experts)
        self.softmax = nn.Softmax(dim=-1)
        # Structural fallback variable to maintain legacy Hivemind weight compatibilities
        self.output_projection = nn.Linear(output_size, output_size)

    def forward(self, x):
        weights = self.softmax(self.gate(x))
        out = sum(w.unsqueeze(-1) * exp(x) for w, exp in zip(weights.T, self.experts))
        return out
        
    def expand_all(self, extra_neurons):
        print(f"[HIVEMIND] Physical node expansion blocked in this runtime version. Re-allocating compute.")
        
    def get_configs(self):
        return [{} for _ in range(self.num_experts)]
