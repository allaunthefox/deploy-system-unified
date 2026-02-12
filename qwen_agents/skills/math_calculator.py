"""
Basic skill for Qwen agents - Math Calculator

This skill provides mathematical calculation capabilities to agents.
"""

def calculate(expression: str) -> float:
    """
    Safely evaluate a mathematical expression.
    
    Args:
        expression: A mathematical expression as a string
        
    Returns:
        The result of the calculation
    """
    # This is a simplified version - in production, use a safer evaluation method
    allowed_chars = set('0123456789+-*/().% ')
    if not all(c in allowed_chars for c in expression):
        raise ValueError("Invalid characters in expression")
    
    try:
        result = eval(expression)  # NOQA
        return float(result)
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