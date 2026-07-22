
import os
import ast
import psutil
import logging
from .titan_memory import TitanMemory

class Overseer:
    """
    Phase 35: The Overseer Protocol.
    1. Panopticon: Recursively indexes the workspace (Omniscience).
    2. Resource Vacuum: Monitors system load to fill available compute.
    """
    def __init__(self, workspace_path=os.getcwd()):
        self.workspace_path = workspace_path
        self.titan = TitanMemory()
        
    def scan_workspace(self):
        """
        Panopticon: Reads every line of code in the workspace.
        Connects files, classes, and functions in Titan Memory.
        """
        print(f"[OVERSEER] Initiating Panopticon Scan on {self.workspace_path}...")
        count = 0
        
        for root, dirs, files in os.walk(self.workspace_path):
            if ".git" in root or "__pycache__" in root:
                continue
                
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    self._index_file(file, full_path)
                    count += 1
                    
        print(f"[OVERSEER] Scan Complete. Indexed {count} source files.")
        return count
        
    def _index_file(self, filename, path):
        """
        Parses a file and extracts concepts (Classes/Functions).
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Parse Syntax Tree to find definitions
            tree = ast.parse(content)
            
            # Add File Concept
            self.titan.add_concept(filename, type="file", content=path)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Link Class -> File
                    self.titan.add_concept(node.name, type="class")
                    self.titan.link_concepts(filename, node.name, "defines_class")
                elif isinstance(node, ast.FunctionDef):
                    # Link Function -> File
                    self.titan.add_concept(node.name, type="function")
                    self.titan.link_concepts(filename, node.name, "defines_function")
                    
        except Exception as e:
            logging.warning(f"[OVERSEER] Failed to parse {filename}: {e}")

    def check_resources(self):
        """
        Resource Vacuum: Returns CPU utilization.
        Used to scale the HiveSwarm.
        """
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory().percent
        return {"cpu": cpu, "ram": mem}
        
    def calculate_swarm_scale(self):
        """
        Decides how many Browser Agents to spawn based on free CPU.
        """
        metrics = self.check_resources()
        free_cpu = 100 - metrics['cpu']
        
        # Aggressive Scaling: 1 agent per 10% free CPU
        # Safety cap at 10 to prevent total freeze
        ideal_agents = int(free_cpu / 10)
        return min(max(1, ideal_agents), 10)
