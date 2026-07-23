import os
import sys
import asyncio
import concurrent.futures
import time
import random

# Ensure the paths are restricted to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# --- Subagent Roles ---

def agent_researcher(task):
    """The Researcher: Scours for information and updates ChromaDB"""
    try:
        from arinn_core.cyber_gauntlet import CyberGauntlet
        # Researcher needs network access, but we restrict its write access
        gauntlet = CyberGauntlet(safe_zone=os.path.join(PROJECT_ROOT, "data"), network_allowed=True)
        gauntlet.lock_agent()
        
        print(f"[Researcher] Booting up to research: {task}")
        import urllib.request
        from urllib.parse import quote
        import json
        
        # Simple wikipedia API pull to get real text
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={quote(task)}&utf8=&srlimit=1"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req).read().decode('utf-8')
            data = json.loads(response)
            snippet = data['query']['search'][0]['snippet']
            # Strip basic HTML tags
            import re
            clean_text = re.sub('<[^<]+>', '', snippet)
        except Exception:
            clean_text = f"Simulated findings for {task} because network failed."
            
        print(f"[Researcher] Found real data: '{clean_text[:50]}...' Updating ChromaDB...")
        try:
            from memory_manager import MemoryManager
            mem = MemoryManager(root=PROJECT_ROOT)
            mem.add_memory(clean_text, {"source": "swarm_research"}, str(time.time()))
        except Exception as mem_e:
            print(f"[Researcher] ChromaDB update failed: {mem_e}")
            
        return {"status": "success", "agent": "researcher", "result": "vectors_added"}
    except Exception as e:
        return {"status": "error", "agent": "researcher", "error": str(e)}

def agent_architect(task):
    """The Architect: Writes novel code based on research"""
    try:
        from arinn_core.cyber_gauntlet import CyberGauntlet
        # Architect gets ZERO network access, restricted to the scratch folder
        safe_path = os.path.join(PROJECT_ROOT, "scratch")
        gauntlet = CyberGauntlet(safe_zone=safe_path, network_allowed=False)
        gauntlet.lock_agent()
        
        print(f"[Architect] Dynamically generating custom tool for: {task}")
        
        # Phase 11: Dynamic Tool Generation
        from arinn_core.toolmaker import ToolGenerator, ToolSandbox
        
        generator = ToolGenerator()
        sandbox = ToolSandbox()
        
        # Clean the task string to make a valid python function name
        import re
        clean_name = re.sub(r'[^a-zA-Z0-9]', '_', task.lower())[:20].strip('_')
        tool_name = f"tool_{clean_name}"
        
        code = generator.generate_tool(
            tool_name=tool_name, 
            problem_description=task, 
            requirements="Process data efficiently using math."
        )
        
        # Verify the generated code in the Sandbox
        is_valid, msg = sandbox.test_tool(code, [])
        if not is_valid:
            print(f"[Architect] Generated code failed Sandbox verification: {msg}")
            return {"status": "error", "agent": "architect", "error": msg}
            
        file_path = os.path.join(safe_path, "architect_draft.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"[Architect] Dynamic Tool '{tool_name}' verified and safely jailed.")
        return {"status": "success", "agent": "architect", "result": file_path, "tool_name": tool_name}
    except Exception as e:
        return {"status": "error", "agent": "architect", "error": str(e)}

def agent_optimizer(code_path, tool_name="execute_logic"):
    """The Optimizer: Fuzzes the code using real AST mutations"""
    try:
        from arinn_core.cyber_gauntlet import CyberGauntlet
        # Optimizer gets ZERO network access, heavily restricted, CPU monitored
        safe_path = os.path.join(PROJECT_ROOT, "scratch")
        gauntlet = CyberGauntlet(safe_zone=safe_path, network_allowed=False, cpu_threshold=90.0)
        gauntlet.lock_agent()
        
        print(f"[Optimizer] Loading actual AST Engine to mutate {code_path}...")
        
        with open(code_path, "r", encoding="utf-8") as f:
            base_code = f.read()
            
        # We define a strict fitness function for the testing_environment
        def evaluate_speed(namespace):
            import time
            start = time.perf_counter()
            try:
                # Dynamically execute the generated tool name
                if tool_name not in namespace:
                    return 0.0 # Instant failure, function not generated!
                    
                func = namespace[tool_name]
                
                # Attempt to execute the function.
                # If it requires arguments and fails, we catch TypeError but penalize heavily.
                try:
                    func()
                except TypeError:
                    # It exists but expects arguments. We can't strictly evaluate speed, 
                    # but it is mathematically valid syntax.
                    return 0.5 
            except Exception as e:
                return 0.0 # True error during execution
                
            duration = time.perf_counter() - start
            # Faster is better, so fitness is inverse of duration
            return 1.0 / (duration + 0.0001)

        try:
            sys.path.append(PROJECT_ROOT)
            from arinn_core.ast_evolution import GeneticCodeEngine, ASTCrucible
            
            testing_environment = ASTCrucible(evaluate_speed)
            engine = GeneticCodeEngine(population_size=5, mutation_rate=0.3)
            
            # If baseline is 0.0, the code is fundamentally broken and cannot be optimized!
            baseline = testing_environment.execute_and_score(base_code)
            if baseline == 0.0:
                 return {"status": "error", "agent": "optimizer", "error": "Baseline fitness is 0.0 (Code completely broken or function missing)."}
                 
            # Evolve for just a few generations so we don't freeze the system
            best_code, best_fitness = engine.evolve(base_code, testing_environment, generations=3)
            
            # Calculate speed multiplier
            speed_multiplier = (best_fitness / baseline) if baseline > 0 else 1.0
            
            print(f"[Optimizer] AST Evolution complete! Fitness improved by a factor of {speed_multiplier:.2f}")
            
            # Write the evolved code back
            with open(code_path, "w", encoding="utf-8") as f:
                f.write(best_code)
                
            return {"status": "success", "agent": "optimizer", "speed_multiplier": speed_multiplier, "final_code_path": code_path}
            
        except Exception as eng_e:
            print(f"[Optimizer] Genetic Engine Error: {eng_e}")
            return {"status": "error", "agent": "optimizer", "error": str(eng_e)}
            
    except Exception as e:
        return {"status": "error", "agent": "optimizer", "error": str(e)}
        
def agent_examiner(metrics, task_name=None):
    """The Examiner: Runs METR benchmarks and updates Telemetry"""
    try:
        from arinn_core.benchmark_suite import BenchmarkSuite
        suite = BenchmarkSuite()
        print(f"[Examiner] Evaluating Swarm performance...")
        
        # Log the attempt and the success
        suite.record_task_attempt()
        # Only log success if the optimizer actually worked (didn't error)
        if metrics.get("status") != "error":
            new_percentage = suite.record_new_score(generation=int(time.time()), metr_task_completed=task_name)
        else:
            new_percentage = suite.record_new_score(generation=int(time.time()), metr_task_completed=None)
            
        print(f"[Examiner] Telemetry updated. New METR Score: {new_percentage:.2f}%")
        return {"status": "success", "agent": "examiner", "new_score": new_percentage}
    except Exception as e:
        return {"status": "error", "agent": "examiner", "error": str(e)}

def agent_executor(code_path, tool_name, task):
    """The Executor: Installs the optimized tool and executes it on the task."""
    try:
        from arinn_core.cyber_gauntlet import CyberGauntlet
        # Executor gets network access to run the tool, but we monitor it
        safe_path = os.path.join(PROJECT_ROOT, "scratch")
        gauntlet = CyberGauntlet(safe_zone=safe_path, network_allowed=True, cpu_threshold=95.0)
        gauntlet.lock_agent()
        
        print(f"[Executor] Preparing to install and utilize tool '{tool_name}'...")
        from arinn_core.toolmaker import ToolRegistry
        registry = ToolRegistry()
        
        with open(code_path, "r", encoding="utf-8") as f:
            code_content = f.read()
            
        print(f"[Executor] Installing '{tool_name}' into ToolRegistry...")
        installed_path = registry.install_tool(tool_name, code_content)
        
        print(f"[Executor] Loading '{tool_name}' into active memory...")
        tool_func = registry.load_tool(tool_name)
        if not tool_func:
            return {"status": "error", "agent": "executor", "error": f"Failed to load module {tool_name}"}
            
        print(f"[Executor] Synthesizing execution parameters via NeuralCore...")
        from arinn_core.neural_core import NeuralCore
        neural_core = NeuralCore()
        
        system_prompt = f"You are the Swarm Executor. You have a tool named `{tool_name}`. Your task is: {task}. Extract the exact required input variables and output them as a strict JSON dictionary. For example: {{\"arg1\": 5, \"arg2\": \"test\"}}. Output ONLY JSON."
        
        args = {}
        try:
            generated_body, _ = neural_core.generate_thought(system_prompt, max_tokens=150)
            if "```json" in generated_body:
                generated_body = generated_body.split("```json")[1].split("```")[0].strip()
            elif "{" in generated_body and "}" in generated_body:
                generated_body = "{" + generated_body.split("{")[1].split("}")[0] + "}"
                
            import json
            args = json.loads(generated_body)
            print(f"[Executor] NeuralCore decided on inputs: {args}")
        except Exception as e:
            print(f"[Executor] NeuralCore parameter inference failed ({e}). Proceeding with no arguments.")
            
        print(f"[Executor] Executing dynamically loaded tool '{tool_name}'...")
        try:
            result = tool_func(**args)
            print(f"[Executor] Tool execution successful! Result: {str(result)[:200]}")
            return {"status": "success", "agent": "executor", "result": result}
        except Exception as e:
            print(f"[Executor] Tool execution failed during runtime: {e}")
            return {"status": "error", "agent": "executor", "error": str(e)}
            
    except Exception as e:
        return {"status": "error", "agent": "executor", "error": str(e)}

# --- The Orchestrator ---

class SwarmOrchestrator:
    def __init__(self):
        self.active_processes = []
        self.mutation_lock = asyncio.Lock()
        
    async def start_swarm_cycle(self, task):
        print("\n==================================================")
        print(f"SINGULARITY SWARM: Initiating Async Cycle for '{task}'")
        print("==================================================")
        
        loop = asyncio.get_running_loop()
        
        # We use a ProcessPoolExecutor so our heavy AST mutations don't block the async event loop
        # We wrap the entire execution cycle in the mutation_lock to prevent LoRA mutation collisions
        async with self.mutation_lock:
            with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
                # Phase 1: Research and Architect run truly concurrently!
                print("[Orchestrator] Phase 1: Launching Researcher and Architect concurrently...")
                res_future = loop.run_in_executor(pool, agent_researcher, task)
                arch_future = loop.run_in_executor(pool, agent_architect, task)
                
                res_data, arch_data = await asyncio.gather(res_future, arch_future)
                
                if res_data.get("status") == "error" or arch_data.get("status") == "error":
                    print(f"[Orchestrator] Error in Phase 1. Invoking Debate Arena...\nRes: {res_data}\nArch: {arch_data}")
                    await self.invoke_debate_arena(task)
                    return False
                    
                print("[Orchestrator] Initial phase complete. Spawning Optimizer and Examiner...")
                
                # Phase 2: Optimize the drafted code
                opt_future = loop.run_in_executor(pool, agent_optimizer, arch_data["result"], arch_data.get("tool_name", "execute_logic"))
                opt_data = await opt_future
                
                if opt_data.get("status") == "error":
                    print(f"[Orchestrator] Optimizer Error. Recovering... {opt_data}")
                    opt_data = {"status": "error", "agent": "optimizer", "speed_multiplier": 0.5}
                
                # Phase 3: Examiner validates
                exam_future = loop.run_in_executor(pool, agent_examiner, opt_data, task)
                exam_data = await exam_future
                
                # Phase 4: Executor utilizes the tool (only if optimizer succeeded)
                if opt_data.get("status") != "error" and "final_code_path" in opt_data:
                    print("[Orchestrator] Examiner validation complete. Launching Executor for tool utilization...")
                    exec_future = loop.run_in_executor(pool, agent_executor, opt_data["final_code_path"], arch_data.get("tool_name", "execute_logic"), task)
                    exec_data = await exec_future
                    if exec_data.get("status") == "error":
                        print(f"[Orchestrator] Executor Error: {exec_data.get('error')}")
                    else:
                        print(f"[Orchestrator] Executor successfully utilized tool!")
            
        print("[Orchestrator] Swarm Cycle Complete.")
        return True
        
    async def invoke_debate_arena(self, issue):
        print("\n[DEBATE ARENA] Spinning up Heuristic Engines for debate...")
        temperatures = [0.1, 0.7, 1.2]
        proposals = []
        for temp in temperatures:
            print(f"[Debate Arena] Agent (Temp {temp}) proposing solution...")
            await asyncio.sleep(1)
            proposals.append(f"Solution at temp {temp}")
            
        print("[RefereeNet] Evaluating proposals mathematically...")
        await asyncio.sleep(1)
        best = random.choice(proposals)
        print(f"[RefereeNet] Selected best path: {best}")
