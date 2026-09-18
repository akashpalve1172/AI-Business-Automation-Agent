from sql_generator import generate_sql
from sql_tool import execute_sql


# =========================================================
# Natural Language → SQL → Database
# =========================================================

def ask_database(question: str):

    print("\n======================================")
    print("USER QUESTION")
    print("======================================")
    print(question)

    # -----------------------------------------------------
    # 1. Generate SQL from the user's question
    # -----------------------------------------------------

    sql = generate_sql(question)

    if not sql:
        print("\nI don't know how to convert this question yet.")
        return

    print("\n======================================")
    print("GENERATED SQL")
    print("======================================")
    print(sql)

    # -----------------------------------------------------
    # 2. Execute SQL through our safe SQL tool
    # -----------------------------------------------------

    result = execute_sql.invoke(sql)

    print("\n======================================")
    print("DATABASE RESULT")
    print("======================================")
    print(result)


# =========================================================
# Interactive mode
# =========================================================

print("\n==============================================")
print("       NATURAL LANGUAGE SQL ASSISTANT")
print("==============================================")

print("Ask questions about the employee database.")
print("Type 'exit' to stop.")


while True:

    question = input("\nYour question: ").strip()

    if question.lower() == "exit":
        print("\nSQL assistant stopped.")
        break

    if not question:
        print("Please enter a question.")
        continue

    ask_database(question)