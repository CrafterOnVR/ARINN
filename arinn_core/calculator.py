
import re
import ast
import logging

class Calculator:
    """
    Phase 54: The Calculator Protocol.
    Teaches ARINN to use math as a tool.
    
    Detects "Calculate [expression]" patterns in text and evaluates them
    safely using Python's AST-based evaluation (no exec/eval abuse).
    """
    
    # Allowed AST node types for safe math evaluation
    SAFE_NODES: set[type] = {
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
        ast.FloorDiv, ast.Mod, ast.USub, ast.UAdd,
    }
    # Python 3.8+ uses ast.Constant instead of ast.Num
    if hasattr(ast, 'Constant'):
        SAFE_NODES.add(ast.Constant)
    
    # Pattern to detect math requests
    CALC_PATTERN = re.compile(
        r"(?:calculate|compute|evaluate|solve|what is)\s+(.+)",
        re.IGNORECASE
    )
    
    def detect(self, text):
        """
        Returns the math expression string if the text contains a calculation request.
        Returns None otherwise.
        """
        match = self.CALC_PATTERN.search(text)
        if match:
            expr = match.group(1).strip().rstrip("?.!")
            return expr
        return None
    
    def _is_safe(self, node):
        """Recursively checks if AST node only contains safe math operations."""
        if type(node) not in self.SAFE_NODES:
            return False
        for child in ast.iter_child_nodes(node):
            if not self._is_safe(child):
                return False
        return True
    
    def evaluate(self, expression):
        """
        Safely evaluates a math expression using AST parsing.
        No arbitrary code execution — only pure arithmetic.
        
        Returns (result, None) on success, or (None, error_message) on failure.
        """
        # Clean up common natural language artifacts
        expression = expression.replace("x", "*").replace("×", "*").replace("÷", "/")
        expression = expression.replace("^", "**")
        # Remove trailing words like "equals" or "is"
        expression = re.sub(r"\s*(equals|is|=).*$", "", expression, flags=re.IGNORECASE)
        expression = expression.strip()
        
        if not expression:
            return None, "Empty expression"
        
        try:
            tree = ast.parse(expression, mode='eval')
        except SyntaxError as e:
            return None, f"Syntax error: {e}"
        
        # Safety check: only allow math nodes
        if not self._is_safe(tree):
            return None, f"Unsafe expression detected (only arithmetic allowed)"
        
        try:
            result = eval(compile(tree, "<calc>", "eval"))
            return result, None
        except ZeroDivisionError:
            return None, "Division by zero"
        except Exception as e:
            return None, f"Evaluation error: {e}"
    
    def process(self, text):
        """
        End-to-end: detect a math request in text, evaluate it, return answer string.
        """
        expr = self.detect(text)
        if expr is None:
            return None  # Not a math request
        
        result, error = self.evaluate(expr)
        if error:
            return f"Calculator Error: {error} (expression: '{expr}')"
        return f"Result: {result}"
