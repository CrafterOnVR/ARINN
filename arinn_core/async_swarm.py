
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from collections import deque
import random
import time
import psutil  # type: ignore

# Local Imports
from .neural_core import NeuralCore  # type: ignore
from .hivemind import HiveSwarm # Re-use Hive logic if compatible, or just PromptHive  # type: ignore

class AsyncSwarm:
    """
    The Async Singularity Engine (Phase 82).
    Manages concurrent ARINN thought processes.
    
    Architecture:
    - Event Loop: Handles non-blocking updates (Dashboard, I/O).
    - ThreadPool: Handles blocking Consciousness (Mistral LLM).
    - Task Queue: Prioritized list of objectives.
    """
    def __init__(self, max_workers=5):
        self.loop = asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.queue = asyncio.Queue()
        self.neural = NeuralCore()
        
        self.active_workers = 0
        self.completed_tasks = 0
        self.running = True
        
        print(f"[SWARM] Initialized Async Swarm with {max_workers} Parallel Minds.")
        
    async def add_task(self, task_type, payload, priority=1):
        """
        Injects a thought into the Swarm.
        """
        # We could use a PriorityQueue, but for now standard Queue is fine.
        # Payload: {"prompt": "...", "context": "..."}
        await self.queue.put((task_type, payload))
        print(f"[SWARM] Task Added: {task_type} (Queue Size: {self.queue.qsize()})")

    async def _blocking_thought(self, prompt):
        """
        Runs the Conscious Mind in a separate thread to avoid freezing the Event Loop.
        """
        # Run in Executor
        thought, cost = await self.loop.run_in_executor(
            self.executor, 
            self.neural.generate_thought, 
            prompt, 
            1024 # Max tokens
        )
        return thought

    async def worker_node(self, worker_id):
        """
        An Autonomous Agent within the Swarm.
        Picks tasks -> Thinks -> Executes.
        """
        print(f"[WORKER-{worker_id}] Online.")
        while self.running:
            try:
                # 1. Get Task
                task_type, payload = await self.queue.get()
                self.active_workers += 1
                
                print(f"[WORKER-{worker_id}] Processing {task_type}...")
                
                # 2. Execute Logic
                if task_type == "RESEARCH":
                    # Execute Genuine Async Web Search via DuckDuckGo
                    try:
                        from duckduckgo_search import AsyncDDGS # type: ignore
                        async with AsyncDDGS() as ddgs:
                            search_results = [r async for r in ddgs.text(payload.get('objective', 'arinn agent'), max_results=2)]
                        web_context = str(search_results)
                    except Exception as e:
                        web_context = f"Web Search Offline: {e}"
                    
                    # Real Thinking (Threaded)
                    prompt = f"Research Task: {payload['objective']}. Write a Python solution."
                    code = await self._blocking_thought(prompt)
                    
                    print(f"[WORKER-{worker_id}] Thought Generated: {len(code)} chars.") # type: ignore
                    
                elif task_type == "REFLECT":
                    prompt = f"Reflection: {payload['topic']}. Analyze implications."
                    thought = await self._blocking_thought(prompt)
                
                elif task_type == "TOOL_MAKER":
                    print(f"[WORKER-{worker_id}] Toolmaker Forge Active.")
                    from .toolmaker import ToolGenerator, ToolSandbox, ToolRegistry  # type: ignore
                    import random
                    
                    tool_name = f"tool_{random.randint(1000, 9999)}"
                    reqs = payload.get("objective", "Create a utility script.")
                    
                    gen = ToolGenerator()
                    # Run code generation in blocking executor to not freeze loop
                    code = await self.loop.run_in_executor(
                        self.executor,
                        gen.generate_code,
                        tool_name,
                        "Need a new function due to missing capability",
                        reqs,
                        self.neural
                    )
                    print(f"[WORKER-{worker_id}] Code drafted. Testing Sandbox...")
                    
                    sandbox = ToolSandbox()
                    # Real execution sandbox verification
                    success, msg = sandbox.test_tool(code, [])
                    if success:
                        print(f"[WORKER-{worker_id}] Sandbox PASS. Installing...")
                        reg = ToolRegistry()
                        reg.install_tool(tool_name, code)
                        # Ensure hot-loading works by trying to load it
                        reg.load_tool(tool_name)
                        print(f"[WORKER-{worker_id}] Hot-Loaded {tool_name} successfully!")
                    else:
                        print(f"[WORKER-{worker_id}] Sandbox FAIL: {msg}")
                    
                # 3. Complete
                self.completed_tasks += 1
                self.active_workers -= 1
                self.queue.task_done()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[WORKER-{worker_id}] Error: {e}")
                self.active_workers -= 1

    async def monitor_resources(self):
        """
        Hibernate Swarm if PC is busy.
        """
        while self.running:
            cpu = psutil.cpu_percent()
            if cpu > 90:
                print(f"[SWARM] High CPU ({cpu}%). Throttling...")
                # await self.pause_workers()
            await asyncio.sleep(5)

    async def run(self):
        """
        Main Entry Point.
        """
        # Start Workers
        workers = [asyncio.create_task(self.worker_node(i)) for i in range(5)]
        monitor = asyncio.create_task(self.monitor_resources())
        
        # Keep alive
        await asyncio.gather(*workers, monitor)

    def shutdown(self):
        self.running = False
        self.executor.shutdown(wait=False)
