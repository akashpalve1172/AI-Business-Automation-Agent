from router import route_question
from policy_tool import search_policy
from sql_generator import generate_sql
from sql_tool import execute_sql
from calculator_tool import calculate


# =========================================================
# Execute user request
# =========================================================

def process_question(question: str):

    print("\n" + "=" * 55)
    print("USER QUESTION")
    print("=" * 55)

    print(question)

    # -----------------------------------------------------
    # 1. Determine route
    # -----------------------------------------------------

    route = route_question(question)

    print("\n" + "=" * 55)
    print("ROUTER DECISION")
    print("=" * 55)

    print("Selected route:", route)

    # -----------------------------------------------------
    # 2. RAG
    # -----------------------------------------------------

    if route == "rag":

        result = search_policy(question)

        print("\n" + "=" * 55)
        print("RAG RESULT")
        print("=" * 55)

        print(result)

        return

    # -----------------------------------------------------
    # 3. SQL
    # -----------------------------------------------------

    if route == "sql":

        sql = generate_sql(question)

        if not sql:

            print("\nCould not generate SQL for this question.")
            return

        print("\n" + "=" * 55)
        print("GENERATED SQL")
        print("=" * 55)

        print(sql)

        result = execute_sql.invoke(sql)

        print("\n" + "=" * 55)
        print("SQL RESULT")
        print("=" * 55)

        print(result)

        return

    # -----------------------------------------------------
    # 4. Calculator
    # -----------------------------------------------------

    if route == "calculator":

        # For our current prototype, extract arithmetic
        # expression or handle common multiplication wording.

        import re

        expression_match = re.search(
            r"\d+(?:\s*[\+\-\*/]\s*\d+)+",
            question
        )

        if expression_match:

            expression = expression_match.group()

        else:

            numbers = re.findall(
                r"\d+(?:\.\d+)?",
                question
            )

            if len(numbers) >= 2:

                if "multiply" in question.lower():
                    expression = "*".join(numbers)

                elif "add" in question.lower():
                    expression = "+".join(numbers)

                elif "subtract" in question.lower():
                    expression = "-".join(numbers)

                elif "divide" in question.lower():
                    expression = "/".join(numbers)

                else:
                    print("\nCould not understand the calculation.")
                    return

            else:

                print("\nCould not understand the calculation.")
                return

        result = calculate(expression)

        print("\n" + "=" * 55)
        print("CALCULATION RESULT")
        print("=" * 55)

        print(f"{expression} = {result}")

        return

    # -----------------------------------------------------
    # 5. Unknown
    # -----------------------------------------------------

    print("\nI could not determine how to handle this question.")


# =========================================================
# Interactive application
# =========================================================

print("\n==============================================")
print("      TECHNOVA LOCAL AI WORKFLOW")
print("==============================================")

print("Available capabilities:")
print("- Company Policy Search")
print("- Employee Database")
print("- Calculator")

print("\nType 'exit' to stop.")


while True:

    question = input("\nYour question: ").strip()

    if question.lower() == "exit":

        print("\nWorkflow stopped.")
        break

    if not question:

        print("Please enter a question.")
        continue

    process_question(question)