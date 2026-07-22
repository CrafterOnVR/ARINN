import os
import sys
import time

project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from arinn_core.ast_evolution import GeneticCodeEngine
from arinn_core.rsi_sandbox import RSICrucible

def start_rsi():
    print("==================================================")
    print("ARINN RSI META-EVOLUTION PROTOCOL ONLINE")
    print("==================================================")
    print("[SYSTEM] Phase 6: LLM-Free Recursive Self-Improvement Active.")
    print("[WARNING] ARINN is now mutating its own source code.\n")
    
    target_file = "arinn_core/ast_evolution.py"
    target_path = os.path.join(project_root, target_file)
    
    with open(target_path, "r", encoding="utf-8") as f:
        brain_seed_code = f.read()
        
    print(f"[RSI] Loaded Target Architecture: {target_file}")
    
    testing_environment = RSICrucible(project_root, target_file)
    # Extremely aggressive mutation rate for structural changes, but small population due to massive sandbox overhead
    engine = GeneticCodeEngine(population_size=10, mutation_rate=0.5) 
    
    print("[RSI] Beginning Brain Mutation...")
    
    # DEEP THOUGHT TARGETING: We mathematically profile that 'evolve' is the bottleneck
    best_brain_code, fitness = engine.evolve(brain_seed_code, testing_environment, generations=2, target_function="evolve")
    
    print("\n[META-EVOLUTION COMPLETE]")
    print(f"Final Brain Benchmark Speed Score: {fitness:.4f}")
    
    if best_brain_code != brain_seed_code:
        print("[ASCENSION] ARINN has successfully discovered a mathematically superior brain architecture!")
        print("[ASCENSION] Overwriting Core Files...")
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(best_brain_code)
        print("[ASCENSION] Success. The system has reached a higher state of intelligence.")
    else:
        print("[SAFETY] All mutations failed to improve the baseline. Elitism successfully preserved the brain.")

if __name__ == "__main__":
    start_rsi()
