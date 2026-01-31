"""Calculator tool for safe math expressions."""

from langchain_core.tools import tool


@tool
def calculator_tool(expression: str) -> str:
    """Evaluate a mathematical expression. Input should be a single expression using numbers and operators: +, -, *, /, **, ( ). Examples: '2 + 3', '10 * 5', '(3 + 2) ** 2'."""
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression.strip()):
        return "Error: Only numbers and + - * / ( ) are allowed."
    try:
        result = eval(expression.strip())
        if isinstance(result, float) and result == int(result):
            result = int(result)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"
