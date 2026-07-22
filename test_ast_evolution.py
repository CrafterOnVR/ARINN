import os
import sys

project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from arinn_core.ast_evolution import GeneticCodeEngine, ASTCrucible

def test_evolution():
    print("="*60)
    print("ARINN AST GENETIC EVOLUTION TEST")
    print("="*60)
    
    # We want ARINN to write a function that multiplies two numbers and adds 10
    # Expected logic: def calculate(a, b): return (a * b) + 10
    
    # The 'seed' code retrieved from ChromaDB is structurally close but mathematically wrong
    # It has the wrong operator (+) instead of (*) and the wrong constant (0) instead of (10)
    seed_code = """
def calculate(a, b):
    return (a + b) + 0
"""
    
    print("\n[SEED CODE FROM CHROMADB]")
    print(seed_code.strip())
    
    # Define the fitness function (The Crucible)
    def fitness_fn(namespace):
        if "calculate" not in namespace:
            return 0.1 # Missing the function
            
        calculate_fn = namespace["calculate"]
        
        # Test cases
        try:
            score = 0.0
            # Test 1: 5 * 2 + 10 = 20
            if calculate_fn(5, 2) == 20:
                score += 0.5
                
            # Test 2: 3 * 3 + 10 = 19
            if calculate_fn(3, 3) == 19:
                score += 0.5
                
            return score
        except Exception:
            return 0.2 # Function threw an error, but it compiled!

    crucible = ASTCrucible(fitness_fn)
    engine = GeneticCodeEngine(population_size=100, mutation_rate=0.3)
    
    # Evolve over 50 generations max
    best_code, best_fitness = engine.evolve(seed_code, crucible, generations=50)
    
    print("\n" + "="*60)
    print("EVOLUTIONARY RESULTS")
    print("="*60)
    print(f"Final Fitness: {best_fitness:.4f}")
    print("Evolved Syntactic Code:")
    print(best_code)
    
if __name__ == "__main__":
    test_evolution()
