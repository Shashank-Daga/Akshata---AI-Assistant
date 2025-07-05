import re
import math


def evaluate_expression(query):
    try:
        expr = re.search(r"(?:calculate|what is) (.*)", query.lower())
        if expr:
            expression = expr.group(1)
            # Safe evaluation
            result = eval(expression, {"__builtins__": {}}, math.__dict__)
            return f"The result is {result}."
        return "Invalid expression."
    except Exception:
        return "Sorry, I couldn't evaluate that."
