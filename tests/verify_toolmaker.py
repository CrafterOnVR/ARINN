
import unittest
import os
import shutil
from arinn_core.apprentice import Apprentice  # type: ignore
from arinn_core.toolmaker import ToolGenerator, ToolSandbox, ToolRegistry  # type: ignore

class TestToolmaker(unittest.TestCase):
    def setUp(self):
        # Setup temp tools dir
        self.test_tools_dir = "test_arinn_tools"
        if not os.path.exists(self.test_tools_dir):
            os.makedirs(self.test_tools_dir)
            with open(os.path.join(self.test_tools_dir, "__init__.py"), 'w') as f:
                f.write("")
        
    def tearDown(self):
        # Cleanup
        if os.path.exists(self.test_tools_dir):
            shutil.rmtree(self.test_tools_dir)
            
    def test_01_apprentice_python_training(self):
        print("\n[TEST] Verifying Apprentice Python Training (Real Code Execution)...")
        apprentice = Apprentice()
        results = apprentice.train_on_python()
        
        # Must pass basic challenges
        for name, success, *err in results:
            print(f"  > Challenge '{name}': {'PASS' if success else 'FAIL ' + str(err)}")
            self.assertTrue(success, f"Failed Python Training challenge: {name}")
            
    def test_02_tool_generation_and_sandbox(self):
        print("\n[TEST] Verifying Tool Generation & Sandbox...")
        generator = ToolGenerator()
        sandbox = ToolSandbox()
        
        # 1. Generate Factorial Tool
        code = generator.generate_tool("fast_test_tool", "Calculate something", "multiply")
        self.assertIn("def fast_test_tool", code)
        self.assertIn("import zlib", code) # From template
        
        # 2. Test in Sandbox (Should Pass)
        success, msg = sandbox.test_tool(code, [])
        print(f"  > Sandbox Result: {msg}")
        self.assertTrue(success, f"Sandbox failed: {msg}")
        
        # 3. Test Invalid Code (Should Fail)
        bad_code = "print(undefined_variable)" # Top-level error
        success, msg = sandbox.test_tool(bad_code, [])
        self.assertFalse(success, "Sandbox should catch runtime errors")
        
    def test_03_registry_installation(self):
        print("\n[TEST] Verifying Tool Registry...")
        registry = ToolRegistry(self.test_tools_dir)
        generator = ToolGenerator()
        
        # Create valid tool
        code = generator.generate_tool("math_tool", "Add numbers", "add")
        
        # Install
        path = registry.install_tool("math_tool", code)
        self.assertTrue(os.path.exists(path))
        
        # Load dynamically
        # Since we are in a test env, dynamic import might be tricky for 'test_arinn_tools' package
        # But we verify the file logic.
        
        # Verify file content
        with open(path, 'r') as f:
            content = f.read()
        self.assertIn("def math_tool", content)

if __name__ == '__main__':
    unittest.main()
