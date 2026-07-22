
import asyncio
import time
import json
import random
import datetime
import psutil  # type: ignore
import re
import os
import sys

# Local Modules
from arinn_core.async_swarm import AsyncSwarm  # type: ignore
from testing_environment import verify_code  # type: ignore
from memory_logger import log_golden_memory, retrieve_relevant_memory  # type: ignore

RESTART_FLAG = "RESTART_REQUIRED"

class GenesisOrchestrator:
    def __init__(self):
        self.stats = {
            "attempts": 0,
            "successes": 0,
            "last_active": "Never",
            "status": "BOOTING",
            "active_workers": 0,
            "queue_size": 0
        }
        self.tasks = [
            "Implement a generator for prime numbers.",
            "Implement a recursive factorial function.",
            "Implement a binary search algorithm.",
            "Implement a class for a Singly Linked List.",
            "Implement a Queue data structure using two Stacks.",
            "Implement a function to check for palindromes.",
            "Implement a Depth First Search (DFS) for a graph.",
            "Implement a Merge Sort algorithm.",
            "Implement a producer-consumer pattern using threading.",
            "Implement a simple neural network forward pass using numpy.",
            "Implement a Decorator that times function execution.",
            "Implement a Singleton Pattern class.",
            "Implement a function to parsing CSV text without libraries."
        ]
        
        print("[GENESIS] Initializing Async Swarm v1.4...")
        self.swarm = AsyncSwarm(max_workers=5) # 5 Parallel Minds

    async def check_updates(self):
        if os.path.exists(RESTART_FLAG):
            print("[GENESIS] Update Flag Detected. Initiating Restart...")
            try: os.remove(RESTART_FLAG)
            except: pass
            self.swarm.shutdown()
            sys.exit(42)

    async def dashboard_loop(self):
        """
        Updates dashboard every 5 seconds.
        """
        while True:
            self.stats["active_workers"] = self.swarm.active_workers
            self.stats["queue_size"] = self.swarm.queue.qsize()
            self.stats["last_active"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.stats["status"] = "RESEARCHING" if int(self.stats["active_workers"]) > 0 else "IDLE"
            
            self._write_dashboard()
            await asyncio.sleep(5)
            
    def _write_dashboard(self):
        status = self.stats["status"]
        color = "green" if status == "RESEARCHING" else "cyan"
        
        html = f"""
        <html>
        <head>
            <title>ARINN Genesis Dashboard</title>
            <meta http-equiv="refresh" content="5">
            <style>
                body {{ font-family: monospace; background: #0f0f0f; color: #00ff00; padding: 20px; }}
                .card {{ border: 1px solid #333; padding: 20px; border-radius: 8px; max-width: 600px; }}
                .status {{ font-size: 24px; font-weight: bold; color: {{color}}; }}
                table {{ width: 100%; margin-top: 10px; }}
                td {{ padding: 5px; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>Genesis Engine v1.4 (Async Swarm)</h1>
                <div class="status">[{status}]</div>
                <hr>
                <table>
                    <tr><td>Active Minds:</td><td>{self.stats['active_workers']}</td></tr>
                    <tr><td>Queue Size:</td><td>{self.stats['queue_size']}</td></tr>
                    <tr><td>Completed Tasks:</td><td>{self.swarm.completed_tasks}</td></tr>
                    <tr><td>Last Active:</td><td>{self.stats['last_active']}</td></tr>
                </table>
            </div>
        </body>
        </html>
        """
        try:
            with open("dashboard.html", "w") as f:
                f.write(html.replace("{color}", color))
        except Exception:
            pass

    async def feeder_loop(self):
        """
        Continuously feeds the Swarm with tasks.
        """
        print("[GENESIS] Task Feeder Active.")
        while True:
            # Keep queue populated but not overflowing
            if self.swarm.queue.qsize() < 10:
                task = random.choice(self.tasks)
                
                # 20% chance to realize it needs a new capability and build a tool for it
                if random.random() < 0.20:
                    tool_ideas = [
                        "Create a utility script to calculate the Fibonacci sequence.",
                        "Create a utility script to find the greatest common divisor of two numbers.",
                        "Create a utility script to reverse a given string."
                    ]
                    payload = {"objective": random.choice(tool_ideas)}
                    await self.swarm.add_task("TOOL_MAKER", payload)
                else:
                    payload = {"objective": task}
                    await self.swarm.add_task("RESEARCH", payload)
                    
                print(f"[GENESIS] Added: {task}")
            
            await self.check_updates()
            await asyncio.sleep(2) # Throttle injection

    async def main(self):
        # Start Dashboard Loop
        dash_task = asyncio.create_task(self.dashboard_loop())
        
        # Start Feeder Loop
        feeder_task = asyncio.create_task(self.feeder_loop())
        
        # Start Swarm
        process_task = asyncio.create_task(self.swarm.run())
        
        print("[GENESIS] Orchestration Started.")
        await asyncio.gather(dash_task, feeder_task, process_task)

if __name__ == "__main__":
    orchestrator = GenesisOrchestrator()
    try:
        asyncio.run(orchestrator.main())
    except KeyboardInterrupt:
        print("[GENESIS] Shutdown.")
