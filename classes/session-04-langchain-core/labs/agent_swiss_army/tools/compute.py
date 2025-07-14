"""
Python Computation Tool for data processing and analysis
Safe Python execution environment for agent use
"""

import ast
import sys
import io
import contextlib
import traceback
import pandas as pd
import numpy as np
import json
from typing import Dict, Any
from langchain.tools import Tool


class SafePythonREPL:
    """
    Safe Python execution environment with whitelisted modules and functions
    """
    
    # Allowed modules and functions
    ALLOWED_MODULES = {
        'pandas': pd,
        'numpy': np,
        'json': json,
        'math': __import__('math'),
        'datetime': __import__('datetime'),
        'collections': __import__('collections'),
        're': __import__('re'),
    }
    
    # Dangerous functions to block
    BLOCKED_FUNCTIONS = {
        'eval', 'exec', 'compile', 'open', 'input', 'raw_input',
        '__import__', 'globals', 'locals', 'vars', 'dir',
        'getattr', 'setattr', 'delattr', 'hasattr'
    }
    
    def __init__(self):
        self.globals_dict = {
            '__builtins__': {
                # Safe built-ins only
                'print': print,
                'len': len,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'sorted': sorted,
                'sum': sum,
                'min': min,
                'max': max,
                'abs': abs,
                'round': round,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'set': set,
                'tuple': tuple,
                'type': type,
                'isinstance': isinstance,
            }
        }
        
        # Add allowed modules
        self.globals_dict.update(self.ALLOWED_MODULES)
        
        # Add common aliases
        self.globals_dict['pd'] = pd
        self.globals_dict['np'] = np
    
    def _is_safe_code(self, code: str) -> bool:
        """
        Check if code is safe to execute
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return False
        
        for node in ast.walk(tree):
            # Check for dangerous function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in self.BLOCKED_FUNCTIONS:
                        return False
            
            # Check for dangerous imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name not in self.ALLOWED_MODULES:
                        return False
            
            if isinstance(node, ast.ImportFrom):
                if node.module not in self.ALLOWED_MODULES:
                    return False
        
        return True
    
    def execute(self, code: str) -> str:
        """
        Execute Python code safely and return the result
        
        Args:
            code: Python code to execute
            
        Returns:
            String representation of the execution result
        """
        # Clean the code
        code = code.strip()
        
        if not code:
            return "No code provided"
        
        # Security check
        if not self._is_safe_code(code):
            return "Error: Code contains unsafe operations"
        
        # Capture output
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = io.StringIO()
        redirected_error = io.StringIO()
        
        try:
            # Redirect stdout and stderr
            sys.stdout = redirected_output
            sys.stderr = redirected_error
            
            # Execute the code
            try:
                # Try to evaluate as expression first
                result = eval(code, self.globals_dict)
                if result is not None:
                    print(result)
            except SyntaxError:
                # If it's not an expression, execute as statement
                exec(code, self.globals_dict)
            
            # Get the output
            output = redirected_output.getvalue()
            error_output = redirected_error.getvalue()
            
            if error_output:
                return f"Error: {error_output.strip()}"
            
            if output:
                return output.strip()
            else:
                return "Code executed successfully (no output)"
                
        except Exception as e:
            error_msg = traceback.format_exc()
            return f"Execution error: {error_msg}"
        
        finally:
            # Restore stdout and stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr


def create_python_tool() -> Tool:
    """
    Create a safe Python REPL tool for data processing
    
    Returns:
        LangChain Tool object for Python execution
    """
    repl = SafePythonREPL()
    
    return Tool.from_function(
        name="python_repl",
        description="""Execute Python code for data processing, calculations, and analysis. 
        Available modules: pandas (pd), numpy (np), json, math, datetime, collections, re.
        Use this for data manipulation, statistical calculations, and processing structured data.
        Example: 'pd.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]}).mean()'""",
        func=repl.execute
    )


def create_math_tool() -> Tool:
    """
    Create a simple math calculation tool
    
    Returns:
        LangChain Tool object for mathematical calculations
    """
    def calculate(expression: str) -> str:
        """
        Safely evaluate mathematical expressions
        """
        import re
        import math
        
        # Clean the expression
        expression = expression.strip()
        
        # Allow only mathematical operations and functions
        allowed_pattern = r'^[0-9+\-*/().\s,sqrt()log()sin()cos()tan()exp()pow()]+$'
        
        # Replace common math functions
        expression = expression.replace('sqrt', 'math.sqrt')
        expression = expression.replace('log', 'math.log')
        expression = expression.replace('sin', 'math.sin')
        expression = expression.replace('cos', 'math.cos')
        expression = expression.replace('tan', 'math.tan')
        expression = expression.replace('exp', 'math.exp')
        expression = expression.replace('pow', 'math.pow')
        
        try:
            # Safe evaluation
            result = eval(expression, {"__builtins__": {}, "math": math})
            return str(result)
        except Exception as e:
            return f"Math error: {str(e)}"
    
    return Tool.from_function(
        name="calculator",
        description="Perform mathematical calculations. Supports basic arithmetic (+, -, *, /) and math functions (sqrt, log, sin, cos, tan, exp, pow). Example: 'sqrt(25) + 10 * 2'",
        func=calculate
    )


# Test function
def test_python_tool():
    """Test the Python REPL tool"""
    print("🐍 Testing Python REPL Tool...")
    
    tool = create_python_tool()
    
    # Test cases
    test_cases = [
        "2 + 2",
        "import pandas as pd; pd.DataFrame({'x': [1,2,3]}).sum()",
        "list(range(5))",
        "[x**2 for x in range(5)]",
        "import numpy as np; np.mean([1,2,3,4,5])"
    ]
    
    for i, test_code in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_code}")
        result = tool.func(test_code)
        print(f"Result: {result}")
    
    print("\n✅ Python tool test completed")


def test_math_tool():
    """Test the math calculation tool"""
    print("🧮 Testing Math Tool...")
    
    tool = create_math_tool()
    
    test_cases = [
        "2 + 2",
        "sqrt(25)",
        "sin(3.14159/2)",
        "log(10)",
        "pow(2, 3)"
    ]
    
    for test_expr in test_cases:
        result = tool.func(test_expr)
        print(f"{test_expr} = {result}")
    
    print("✅ Math tool test completed")


if __name__ == "__main__":
    test_python_tool()
    print()
    test_math_tool()