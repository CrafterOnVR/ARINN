
import random
import copy
import logging

class Genome:
    """
    Represents the tunable hyperparameters of a SubBrain.
    """
    def __init__(self, params=None):
        if params:
            self.genes = params
        else:
            # Default Init
            self.genes = {
                "perplexity_threshold": 0.8,
                "attention_budget": 7,
                "decay_rate": 0.1,
                "learning_rate": 0.01,
                "curiosity_factor": 0.5
            }
            
    def mutate(self):
        """Randomly alters genes."""
        gene = random.choice(list(self.genes.keys()))
        val = self.genes[gene]
        
        # Mutation logic
        if isinstance(val, float):
            mutation = random.uniform(-0.1, 0.1)
            self.genes[gene] = max(0.01, val + mutation)
        elif isinstance(val, int):
            mutation = random.choice([-1, 1])
            self.genes[gene] = max(1, val + mutation)
            
    def crossover(self, partner):
        """Mixes genes with a partner."""
        child_genes = {}
        for k in self.genes:
            child_genes[k] = random.choice([self.genes[k], partner.genes[k]])
        return Genome(child_genes)

    def __repr__(self):
        return str(self.genes)

class EvolutionaryOptimizer:
    """
    Manages the population of Brain Configurations.
    """
    def __init__(self, population_size=10):
        self.population = [Genome() for _ in range(population_size)]
        self.generation = 1
        
    def evaluate_fitness(self, genome, consensus_speed, consensus_quality):
        """
        Fitness = Speed (inverse time) * Quality
        """
        # Lower speed (time) is better, higher quality is better
        # Avoid div by zero
        speed_score = 1.0 / max(0.001, consensus_speed) 
        fitness = speed_score * consensus_quality
        return fitness
        
    def evolve(self, scored_population):
        """
        Runs one generation step.
        scored_population: list of (Genome, fitness_score)
        """
        # Sort by fitness desc
        scored_population.sort(key=lambda x: x[1], reverse=True)
        
        # Survivor Selection (Top 50%)
        survivors = [g for g, s in scored_population[:len(self.population)//2]]
        
        # Reproduction
        new_pop = []
        while len(new_pop) < len(self.population):
            parent_a = random.choice(survivors)
            parent_b = random.choice(survivors)
            child = parent_a.crossover(parent_b)
            
            # Mutation Chance
            if random.random() < 0.2:
                child.mutate()
                
            new_pop.append(child)
            
        self.population = new_pop
        self.generation += 1
        
        best = survivors[0]
        print(f"[EVOLUTION] Generation {self.generation} Complete. Best Genome: {best}")
        return best
