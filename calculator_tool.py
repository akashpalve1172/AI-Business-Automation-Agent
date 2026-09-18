import re
from langchain_core.tools import tool


# =========================================================
# Basic Calculation Function
# =========================================================

def calculate(expression: str):
    """
    Safely evaluate a basic arithmetic expression.
    Example:
        4000 * 3
        100 + 50
        500 / 5
    """

    expression = expression.strip()

    # Allow only numbers, decimal points, spaces and operators
    if not re.fullmatch(r"[0-9+\-*/().\s]+", expression):
        raise ValueError("Invalid mathematical expression.")

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return result

    except Exception as e:
        raise ValueError(
            f"Could not calculate expression: {e}"
        )


# =========================================================
# LangChain Tool
# =========================================================

@tool
def calculator_tool(expression: str) -> str:
    """
    Calculate a basic arithmetic expression.
    """

    try:
        result = calculate(expression)
        return f"Result: {result}"

    except Exception:
        return "Could not understand the calculation."


# =========================================================
# Natural Language Calculator
# =========================================================

def convert_words_to_expression(text: str) -> str:

    text = text.lower()

    replacements = {
        "multiplied by": "*",
        "times": "*",
        "plus": "+",
        "added to": "+",
        "minus": "-",
        "subtracted by": "-",
        "divided by": "/",
        "divide by": "/",
    }

    for phrase, operator in replacements.items():
        text = text.replace(
            phrase,
            f" {operator} "
        )

    return text


def natural_language_calculation(question: str):

    question = convert_words_to_expression(question)

    numbers = re.findall(
        r"\d+(?:\.\d+)?",
        question
    )

    if len(numbers) < 2:
        return "Could not understand the calculation."

    lower_question = question.lower()

    if "*" in question:
        expression = "*".join(numbers)

    elif "+" in question:
        expression = "+".join(numbers)

    elif "-" in question:
        expression = "-".join(numbers)

    elif "/" in question:
        expression = "/".join(numbers)

    elif "multiply" in lower_question:
        expression = "*".join(numbers)

    elif "plus" in lower_question:
        expression = "+".join(numbers)

    elif "minus" in lower_question:
        expression = "-".join(numbers)

    elif "divide" in lower_question:
        expression = "/".join(numbers)

    else:
        return "Could not understand the calculation."

    try:
        result = calculate(expression)

        return f"{expression} = {result}"

    except Exception:
        return "Could not understand the calculation."


# =========================================================
# Test
# =========================================================

if __name__ == "__main__":

    test_questions = [
        "4000 multiplied by 3",
        "100 plus 50",
        "500 divided by 5",
        "200 minus 75",
    ]

    for question in test_questions:

        print("\nQuestion:", question)

        print(
            "Answer:",
            natural_language_calculation(question)
        )