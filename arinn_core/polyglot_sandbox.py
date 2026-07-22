import os
import subprocess
import random
import tempfile

class UniversalStringMutator:
    """
    Mutates raw strings for Polyglot (C++, Rust) evolution where Python AST fails.
    """
    def __init__(self, mutation_rate=0.4):
        self.mutation_rate = mutation_rate
        # A list of common syntactic errors and corrections in C++
        self.mutations = [
            ("cout >>", "cout <<"),
            ("<< endl", ">> endl"),
            ('\"Hello\"', '\"Hello World\"'),
            ('return 1;', 'return 0;'),
            ('std::cout', 'cout'),
            ('print(', 'cout << '),
        ]
        
    def mutate(self, code: str) -> str:
        mutated_code = code
        for target, replacement in self.mutations:
            if target in mutated_code and random.random() < self.mutation_rate:
                mutated_code = mutated_code.replace(target, replacement, 1)
        return mutated_code

class DockerCrucible:
    """
    Compiles and executes polyglot code inside a secure Docker container.
    """
    def __init__(self, fitness_function):
        self.fitness_function = fitness_function

    def execute_and_score(self, source_code: str) -> float:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = os.path.join(temp_dir, "main.cpp")
            with open(source_path, "w") as f:
                f.write(source_code)
                
            docker_cmd = [
                "docker", "run", "--rm", 
                "-v", f"{temp_dir}:/usr/src/app", 
                "-w", "/usr/src/app", 
                "gcc:latest", 
                "bash", "-c", "g++ main.cpp -o main && ./main"
            ]
            
            try:
                result = subprocess.run(
                    docker_cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=15 
                )
                
                output = result.stdout.strip()
                error = result.stderr.strip()
                return self.fitness_function(output, result.returncode, error)
            except subprocess.TimeoutExpired:
                return 0.0
            except Exception as e:
                return 0.0

class PolyglotGeneticEngine:
    def __init__(self, population_size=10, mutation_rate=0.4):
        self.pop_size = population_size
        self.mutation_rate = mutation_rate

    def evolve(self, base_code: str, testing_environment: DockerCrucible, generations=10, stagnation_detector=None):
        print(f"[POLYGLOT ENGINE] Initiating Docker Genetic Evolution (Gen: {generations}, Pop: {self.pop_size})")
        
        # 1. ESTABLISH ABSOLUTE BASELINE
        baseline_fitness = testing_environment.execute_and_score(base_code)
        
        population = [base_code] * (self.pop_size - 1)
        best_code = base_code
        best_fitness = baseline_fitness
        print(f"[POLYGLOT ENGINE] Baseline Seed Fitness: {baseline_fitness:.4f}")
            
        for gen in range(1, generations + 1):
            scored_population = []
            
            # 2. EVALUATE FITNESS (Mutations)
            for candidate_code in population:
                fitness = testing_environment.execute_and_score(candidate_code)
                scored_population.append((candidate_code, fitness))
                
            # 3. ENFORCE ELITISM
            scored_population.append((best_code, best_fitness))
                
            scored_population.sort(key=lambda x: x[1], reverse=True)
            gen_best_code, gen_best_fitness = scored_population[0]
            
            if gen_best_fitness > best_fitness:
                best_fitness = gen_best_fitness
                best_code = gen_best_code
                
            print(f"Gen {gen} | Best Fitness: {gen_best_fitness:.4f}")
            
            if stagnation_detector:
                stagnation_detector.evaluate_generation(gen_best_fitness)
            
            if best_fitness >= 1.0:
                print(f"[POLYGLOT ENGINE] PERFECT FITNESS ACHIEVED in Generation {gen}!")
                break
                
            survivors = [p[0] for p in scored_population[:self.pop_size // 2]]
            
            new_population = []
            while len(new_population) < self.pop_size - 1: # Leave room for elite
                parent_code = random.choice(survivors)
                mutator = UniversalStringMutator(self.mutation_rate)
                child_code = mutator.mutate(parent_code)
                new_population.append(child_code)
                
            population = new_population
            
        print("[POLYGLOT ENGINE] Evolution Complete.")
        return best_code, best_fitness
