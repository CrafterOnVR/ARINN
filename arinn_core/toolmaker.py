
import os
import subprocess
import sys
import importlib.util
import json
import logging

class ToolGenerator:
    """
    Writes Python code to solve specific problems.
    Leverages the Hivemind or Apprentice model in the future.
    For now, uses template-based generation grounded in known patterns.
    """
    def generate_tool(self, tool_name, problem_description, requirements, neural_core=None):
        """
        Generates a python file by formally integrating with NeuralCore 
        to execute absolute AI logic synthesis via API completions.
        """
        if neural_core is None:
            try:
                from arinn_core.neural_core import NeuralCore # type: ignore
                neural_core = NeuralCore()
            except ImportError:
                neural_core = None
                
        import random
        seed_variance = random.randint(10000, 99999)
        system_prompt = f"System Variance Seed: {seed_variance}\nWrite a single robust python module with a central function named {tool_name} to solve: {requirements}. You MUST also write a function named `test_suite()` containing strict `assert` statements to mathematically verify your logic. Be EXTREMELY concise. Write ONLY the raw code. Include no markdown wrapping formatting. If you run out of tokens and need more space to finish your code, append exactly `# REQUEST_MORE_TOKENS` to the very end of your response."
        
        try:
            if neural_core is None:
                raise RuntimeError("NeuralCore offline")
                
            import json
            import os
            
            # Dynamically fetch token limit from UI Configuration
            max_tokens = 350
            config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "arinn_runtime_config.json"))
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if "max_tokens" in data:
                            max_tokens = int(data["max_tokens"])
                except Exception:
                    pass
            
            # Scale tokens dynamically based on proven intelligence (ARINN Level)
            # Level 0 gets base tokens. Level 4 gets +2000 tokens.
            try:
                from arinn_core.benchmark_suite import BenchmarkSuite
                current_task, _ = BenchmarkSuite().get_metr_status()
                level = current_task.get("level", 0)
                max_tokens += (level * 500)
                print(f"[TOOLMAKER] ARINN Autonomy Level {level} detected. Scaling max_tokens to {max_tokens}...")
            except Exception:
                pass
            
            # Physical LLM reasoning execution (blocking thread)
            print(f"[TOOLMAKER] Drafting functional structure for {tool_name} via NeuralCore...")
            
            final_code = ""
            while True:
                generated_body, metrics = neural_core.generate_thought(system_prompt, max_tokens=max_tokens)
                final_code += generated_body
                
                # Check if the AI explicitly requested more tokens, or if it got forcefully cut off
                if "# REQUEST_MORE_TOKENS" in generated_body or metrics.get("tokens_generated", 0) >= max_tokens:
                    print(f"[TOOLMAKER] Token Horizon Reached (or explicitly requested). Expanding cognitive window and resuming synthesis...")
                    # Strip out the request tag if it exists
                    final_code = final_code.replace("# REQUEST_MORE_TOKENS", "").strip()
                    
                    # Feed the generated code back in to continue
                    system_prompt = system_prompt + "\n\n[SYSTEM: Horizon Extended. Continue exactly from where you left off. Do not rewrite the code above.]\n" + generated_body
                    
                    # Add another block of tokens to the budget
                    max_tokens += 500
                else:
                    break
            
            # Clean AST output bounds if markdown leaks through
            if "```python" in final_code:
                final_code = final_code.split("```python")[1].split("```")[0].strip()
                
            return final_code
            
        except Exception as e:
            print(f"[TOOLMAKER] NeuralCore unavailable ({e}). Aborting synthesis.")
            raise RuntimeError(f"NeuralCore Synthesis Failed: {e}")

class ToolSandbox:
    """
    Safe execution environment for verifying new tools.
    """
    def test_tool(self, tool_name, code_content, test_cases):
        """
        Runs the generated code in a restricted sandbox.
        test_cases: list of (input_args, expected_output)
        """
        import tempfile
        import ast
        
        # Prevent Reward Hacking: Parse AST to ensure test_suite() actually calls the tool
        try:
            tree = ast.parse(code_content)
            test_suite_node = next((node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'test_suite'), None)
            
            if not test_suite_node:
                return False, "Validation Failed: You must implement a test_suite() function."
                
            calls_tool = any(
                isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == tool_name
                for node in ast.walk(test_suite_node)
            )
            
            if not calls_tool:
                return False, f"Validation Failed (Reward Hacking Detected): Your test_suite() must explicitly invoke '{tool_name}'."
                
        except SyntaxError as e:
            return False, f"Validation Failed: Syntax Error in generated code - {e}"
        
        # 1. Write to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
            tmp.write(code_content)
            # Add strict test harness
            tmp.write("\n\nif __name__ == '__main__':\n")
            tmp.write("    import sys\n")
            tmp.write("    try:\n")
            tmp.write("        test_suite()\n")
            tmp.write("        print('TESTS_PASSED')\n")
            tmp.write("    except Exception as e:\n")
            tmp.write("        sys.stderr.write(str(e) + '\\n')\n")
            tmp.write("        sys.exit(1)\n")
            tmp_path = tmp.name
            
        # 2. Run in subprocess
        try:
            result = subprocess.run(
                [sys.executable, tmp_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Cleanup
            try:
                os.remove(tmp_path)
            except:
                pass
                
            if result.returncode == 0 and "TESTS_PASSED" in result.stdout:
                return True, "Logical Verification Valid, Tests Passed"
            else:
                return False, f"Logical Verification Failed: {result.stderr or result.stdout}"
                
        except Exception as e:
            return False, f"Sandbox Error: {e}"

class ToolRegistry:
    """
    Manages installed tools.
    """
    def __init__(self, tools_dir="arinn_tools"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.tools_dir = os.path.abspath(os.path.join(base_dir, '..', tools_dir))
        if not os.path.exists(self.tools_dir):
            os.makedirs(self.tools_dir)
            # Init package
            with open(os.path.join(self.tools_dir, "__init__.py"), 'w', encoding='utf-8') as f:
                f.write("# ARINN Tools Package\n")
                
    def install_tool(self, tool_name, code_content):
        file_path = os.path.join(self.tools_dir, f"{tool_name}.py")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code_content)
        return file_path
        
    def list_tools(self):
        return [f.replace('.py', '') for f in os.listdir(self.tools_dir) if f.endswith('.py') and f != '__init__.py']

    def load_tool(self, tool_name):
        try:
             spec = importlib.util.spec_from_file_location(tool_name, os.path.join(self.tools_dir, f"{tool_name}.py"))
             if spec is None or spec.loader is None:
                 logging.error(f"Could not create module spec for tool {tool_name}")
                 return None
             loader = spec.loader # pyre-ignore
             module = importlib.util.module_from_spec(spec)
             loader.exec_module(module) # pyre-ignore
             return getattr(module, tool_name)
        except Exception as e:
            logging.error(f"Failed to load tool {tool_name}: {e}")
            return None
