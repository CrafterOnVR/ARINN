
import time
import random
import os
from arinn_core.scholar import ScholarEngine
from arinn_core.critic import CodeRepairEngine
from arinn_core.archive import ArchiveEngine

def run_marathon():
    print("--------------------------------------------------")
    print("     EPOCH IV: THE MARATHON (INFINITE TRAIN)      ")
    print("--------------------------------------------------")
    print("[MARATHON] Initializing Faculty...")
    
    scholar = ScholarEngine()
    critic = CodeRepairEngine(max_retries=3) # Give it 3 chances to fix itself
    archive = ArchiveEngine()
    
    education_dir = "arinn_education"
    
    try:
        while True:
            # 1. STUDY (Scholar)
            # Find a random text to review (Reinforcement)
            files = [f for f in os.listdir(education_dir) if f.endswith(".txt")]
            if files:
                target = random.choice(files)
                print(f"\n[MARATHON] Period 1: Studying '{target}'...")
                scholar.study(os.path.join(education_dir, target))
            else:
                print("[MARATHON] Library empty. Waiting for books...")
            
            # 2. PRACTICE (Critic)
            # Pick a random concept from memory to "Demonstrate"
            graph = archive.load_memory()
            concepts = [n for n, d in graph.nodes(data=True) if d.get('type') == 'technical_concept']
            
            if concepts:
                concept = random.choice(concepts)
                task_name = f"Practice_{concept.replace(' ', '_')}"
                prompt = f"write a python script that demonstrates usage of {concept}"
                
                print(f"\n[MARATHON] Period 2: Exam. Topic: {concept}")
                success = critic.generate_and_refine(task_name, prompt)
                
                if success:
                    print(f"[MARATHON] Grade: PASS. {concept} mastered.")
                    # Reinforce Memory (Increase Logic Weight?)
                    # Future: graph[concept]['mastery'] += 1
                else:
                    print(f"[MARATHON] Grade: FAIL. {concept} needs more study.")
            else:
                print("[MARATHON] Mind empty. Learn something first.")
                
            print("\n[MARATHON] Sleeping... (Press Ctrl+C to Stop)")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n[MARATHON] Class Dismissed.")

if __name__ == "__main__":
    run_marathon()
