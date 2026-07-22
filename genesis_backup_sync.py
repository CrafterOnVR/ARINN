
import time
import json
import random
import datetime
import psutil
import re
import os
import sys

# Local Modules
from arinn_core.neural_core import NeuralCore
from testing_environment import verify_code
from memory_logger import log_golden_memory, retrieve_relevant_memory
from arinn_core.hivemind import HiveSwarm

RESTART_FLAG = "RESTART_REQUIRED"

class GenesisEngine:
    def __init__(self):
        self.stats = {
            "attempts": 0,
            "successes": 0,
            "last_active": "Never",
            "status": "BOOTING"
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
        
        # Initialize Dual Mind
        print("[GENESIS] Initializing Neural Core...")
        self.neural = NeuralCore()
        
        # Initialize Hivemind (Context System)
        print("[GENESIS] Waking the Hivemind...")
        self.hive = HiveSwarm()

    def check_updates(self):
        if os.path.exists(RESTART_FLAG):
            print("[GENESIS] Update Flag Detected. Initiating Restart Protocol...")
            try:
                os.remove(RESTART_FLAG)
            except:
                pass
            return True
        return False

    def check_resources(self):
        try:
            cpu = psutil.cpu_percent(interval=1)
            if cpu > 80:
                print(f"[GENESIS] High CPU Load ({cpu}%). Hibernating...")
                return True
        except Exception:
            pass
        return False

    def update_dashboard(self, status, stats):
        self.stats["status"] = status
        self.stats["last_active"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        color = "green" if status == "RESEARCHING" else "red"
        if status == "HIBERNATING": color = "orange"
        if status == "BOOTING": color = "cyan"
        
        # In the new Hivemind, we don't have 'status report' per se, 
        # but we can list experts.
        hive_html = "<h3>Active Contexts</h3><ul>"
        hive_html += f"<li>{len(self.hive.experts)} Experts Ready</li>"
        hive_html += "</ul>"

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
                <h1>Genesis Engine v1.3 (Dual Mind)</h1>
                <div class="status">[{status}]</div>
                <hr>
                <table>
                    <tr><td>Attempts:</td><td>{stats['attempts']}</td></tr>
                    <tr><td>Successes:</td><td>{stats['successes']}</td></tr>
                    <tr><td>Last Active:</td><td>{stats['last_active']}</td></tr>
                </table>
                <hr>
                {hive_html}
            </div>
        </body>
        </html>
        """
        try:
            with open("dashboard.html", "w") as f:
                f.write(html.replace("{color}", color))
        except Exception as e:
            print(f"[GENESIS] Dashboard update failed: {e}")

    def train_hivemind(self, task, code):
        """
        Feeds the 'Golden Memory' (Success) to the Hivemind.
        In Context-Switched Hive, this means updating Vector DB (Mnemosyne).
        The Hive 'Broadcast' is now a consultation, not training.
        """
        print(f"[GENESIS] Consulting Hivemind on success: {task[:30]}...")
        # Broadcast to see what experts think (Just for narrative/logging here)
        self.hive.broadcast(f"I just solved: {task}")

    def mode_researcher(self):
        self.update_dashboard("RESEARCHING", self.stats)
        
        # 1. Select Task
        task = random.choice(self.tasks)
        print(f"\n[GENESIS] New Task: {task}")
        self.stats["attempts"] += 1
        
        # 2. Meta-Learning (RAG)
        memory = retrieve_relevant_memory(task)
        memory_context = ""
        if memory:
            print(f"[GENESIS] Recall: Found similar task '{memory['task']}'")
            memory_context = (
                f"\n\n[MEMORY RECALL]\n"
                f"You previously solved: '{memory['task']}'\n"
                f"Code:\n```python\n{memory['solution']}\n```\n"
            )
        
        # 3. Construct Prompt
        prompt = (
            f"You are a strict Python expert. {memory_context}"
            f"Write a self-contained script for: {task}. "
            f"Output ONLY the code inside markdown code blocks."
        )
        
        # 4. Inference (Dual Mind)
        print("[GENESIS] Thinking (Conscious Mind)...")
        thought, cost = self.neural.generate_thought(prompt, max_new_tokens=2048)
        
        # 5. Extraction
        content = thought
        code_match = re.search(r"```python(.*?)```", content, re.DOTALL)
        if not code_match:
            code_match = re.search(r"```(.*?)```", content, re.DOTALL)
            
        if code_match:
            code = code_match.group(1).strip()
        else:
            code = content.strip()
            
        print("[GENESIS] Code generated. Verifying...")

        # 6. Verification
        success = verify_code(code)
        
        # 7. Logging
        if success:
            log_golden_memory(task, code)
            self.stats["successes"] += 1
            print("[GENESIS] Golden Memory Logged.")
            self.train_hivemind(task, code)
        else:
            print("[GENESIS] VerificationFailed.")
            
        self.update_dashboard("COOLDOWN", self.stats)


def main_loop():
    print("[GENESIS] Initializing System v1.3...")
    engine = GenesisEngine()
    engine.update_dashboard("BOOTING", engine.stats)
    
    print("[GENESIS] System Online. Entering Loop.")
    
    while True:
        try:
            # Check for Watcher Protocol updates
            if engine.check_updates():
                sys.exit(42) # Special Code for Watcher to Restart us

            # 1. Resource Check
            if engine.check_resources():
                engine.update_dashboard("HIBERNATING", engine.stats)
                time.sleep(60)
                continue
                
            # 2. Run Research Cycle
            engine.mode_researcher()
            
            # 3. Cooldown
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("[GENESIS] Manual Shutdown.")
            break
        except Exception as e:
            print(f"[GENESIS] Loop Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main_loop()
