# =============================================================================
# Audit Event Identifier: DSU-PYS-500117
# Last Updated: 2026-02-28
# =============================================================================
"""
Basic skill for Qwen agents - Math Calculator

This skill provides mathematical calculation capabilities to agents.
"""

import ast
import operator as op

# Supported operators
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.BitXor: op.xor,
    ast.USub: op.neg
}

def eval_node(node):
    """Safely evaluate an AST node."""
    if isinstance(node, ast.Num):  # Python < 3.8
        return node.n
    elif isinstance(node, ast.Constant):  # Python >= 3.8
        return node.value
    elif isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](eval_node(node.left), eval_node(node.right))
    elif isinstance(node, ast.UnaryOp):
        return OPERATORS[type(node.op)](eval_node(node.operand))
    else:
        raise TypeError(f"Unsupported node type: {type(node)}")

def calculate(expression: str) -> float:
    """
    Safely evaluate a mathematical expression using AST parsing.
    
    Args:
        expression: A mathematical expression as a string
        
    Returns:
        The result of the calculation
    """
    try:
        # Parse the expression into an AST
        node = ast.parse(expression, mode='eval').body
        return float(eval_node(node))
    except Exception as e:
        raise ValueError(f"Could not evaluate expression: {str(e)}")


# Example usage
if __name__ == "__main__":
    # Test the calculator
    test_expressions = [
        "2 + 2",
        "10 * 5",
        "(3 + 5) * 2",
        "100 / 4"
    ]
    
    for expr in test_expressions:
        try:
            result = calculate(expr)
            print(f"{expr} = {result}")
        except ValueError as e:
            print(f"Error calculating '{expr}': {e}")