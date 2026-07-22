import os
import sys
import time

project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from memory_manager import MemoryManager
from arinn_core.ast_evolution import GeneticCodeEngine
from arinn_core.constitution import StagnationDetector, ConstitutionalViolationError
from arinn_core.python_sandbox import SafePythonCrucible
from arinn_core.adversarial_sandbox import AdversarialCrucible
from arinn_core.polyglot_sandbox import PolyglotGeneticEngine, DockerCrucible

# String test block that gets appended to the adversarial code
ADVERSARIAL_TEST_CODE = """
import random
import time as time_module

def run_test():
    try:
        test_array = [random.randint(0, 1000) for _ in range(500)]
        expected_result = sorted(test_array)
        
        start_time = time_module.perf_counter()
        result = fast_sort(test_array.copy())
        end_time = time_module.perf_counter()
        
        if result == expected_result:
            print(end_time - start_time)
        else:
            print("FAIL")
    except Exception:
        print("FAIL")

run_test()
"""

def start_daydreaming():
    print("==================================================")
    print("ARINN DAYDREAMER PROTOCOL ONLINE")
    print("==================================================")
    print("[SYSTEM] Autonomous Experiential Learning Loop Active.")
    print("[SYSTEM] Phase 4.2: Genetic Elitism & Safe Isolation Enabled.\n")
    
    memory = MemoryManager(root=project_root)
    engine = GeneticCodeEngine(population_size=100, mutation_rate=0.4)
    detector = StagnationDetector(max_stagnant_generations=500)
    
    goals = [
        {
            "id": "ADVERSARIAL_SORT", 
            "query": "python sort algorithm with massive delay", 
            "seed": "def fast_sort(arr):\n    # Artificial delay trap that ARINN needs to mutate away to win\n    junk = 0\n    for _ in range(10000):\n        junk = junk + 1\n    \n    # Basic Bubble Sort\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr"
        }
    ]
    
    for goal in goals:
        print(f"--- [NEW ADVERSARIAL GOAL] {goal['id']} ---")
        
        seed_code = goal["seed"]
        print(f"[MEMORY] Memory Retrieved Seed Code:\n{seed_code.strip()}\n")
        
        testing_environment = AdversarialCrucible(ADVERSARIAL_TEST_CODE)
        
        detector.start_new_goal(goal["id"])
        
        try:
            best_code, fitness = engine.evolve(seed_code, testing_environment, generations=2, stagnation_detector=detector)
            
            print("\n[EVOLUTION COMPLETE]")
            print(f"[SUCCESS] ARINN autonomously optimized {goal['id']} through Adversarial Self-Play!")
            print(f"Final Peak Fitness (Speed Score): {fitness:.4f}")
            print(f"Final Synthesized Code:\n{best_code.strip()}\n")
        except ConstitutionalViolationError as e:
            print(f"\n{str(e)}")
            
        time.sleep(2) 

if __name__ == "__main__":
    start_daydreaming()
