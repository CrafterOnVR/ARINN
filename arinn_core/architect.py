import os
import ast
import shutil
import unittest
import logging
from .neural_core import NeuralCore # pyre-ignore

class Architect:
    """
    Phase 33: The Self-Rewriting Architect.
    Enables ARINN to analyze and optimize its own source code.
    TRIPLE-SAFETY PROTOCOL ENFORCED.
    """
    def __init__(self):
        self.core = NeuralCore()
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        
    def introspect(self, filename):
        """Reads own source code."""
        path = os.path.join(self.root_dir, filename)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
            
    def propose_refactor(self, filename, goal="Optimize for speed"):
        """
        Asks the NeuralCore to rewrite the code.
        """
        code = self.introspect(filename)
        if not code: return None, "File not found"
        
        prompt = f"Rewrite the following Python code to {goal}. Return ONLY the code:\n\n{code[:2000]}" # Truncate for token limits
        
        # NeuralCore generation (Real AI)
        new_code, cost = self.core.generate_thought(prompt, max_new_tokens=500)
        
        if self.core.mode == "SYMBOLIC":
            # True fallback enforces no mock mutations unless physical reasoning occurs.
            raise NotImplementedError("Architect optimizations physically require an active Neural LLM backend.")
        
        return new_code, "Generated"

    def apply_change(self, filename, new_code):
        """
        Safety Protocol:
        1. Write to _candidate.py
        2. Test
        3. Backup
        4. Overwrite
        """
        target_path = os.path.join(self.root_dir, filename)
        candidate_path = os.path.join(self.root_dir, "_candidate.py")
        backup_path = target_path + ".bak"
        
        # 1. Write Candidate
        with open(candidate_path, "w", encoding="utf-8") as f:
            f.write(new_code)
            
        # 2. Verify Syntax (Basic Test)
        try:
            with open(candidate_path, "r", encoding="utf-8") as f:
                ast.parse(f.read())
            print(f"[ARCHITECT] Candidate {filename} passed syntax check.")
        except SyntaxError as e:
            print(f"[ARCHITECT] Candidate rejected (Syntax Error): {e}")
            return False
            
        # 3. Backup
        shutil.copy(target_path, backup_path)
        
        # 4. Overwrite
        shutil.copy(candidate_path, target_path)
        print(f"[ARCHITECT] Applied optimization to {filename}. Backup saved.")
        return True
