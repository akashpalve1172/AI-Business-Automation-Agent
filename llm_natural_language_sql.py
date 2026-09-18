from llm_sql_generator import generate_sql_with_llm
from sql_tool import execute_sql


# =========================================================
# Natural Language → LLM → SQL → Validation → Database
# =========================================================

def ask_database(question: str):

    print("\n" + "=" * 55)
    print("USER QUESTION")
    print("=" * 55)
    print(question)

    # -----------------------------------------------------
    # 1. Generate SQL using Gemini
    # -----------------------------------------------------

    sql = generate_sql_with_llm(question)

    if not sql:
        print("\nThe LLM did not generate a SQL query.")
        return

    print("\n" + "=" * 55)
    print("LLM GENERATED SQL")
    print("=" * 55)
    print(sql)

    # -----------------------------------------------------
    # 2. Validate SQL + execute database query
    # -----------------------------------------------------

    result = execute_sql.invoke(sql)

    print("\n" + "=" * 55)
    print("DATABASE RESULT")
    print("=" * 55)
    print(result)


# =========================================================
# Interactive mode
# =========================================================

print("\n==============================================")
print("       TECHNOVA LLM SQL ASSISTANT")
print("==============================================")

print("Ask a question about the employee database.")
print("Type 'exit' to stop.")


while True:

    question = input("\nYour question: ").strip()

    if question.lower() == "exit":
        print("\nLLM SQL Assistant stopped.")
        break

    if not question:
        print("Please enter a question.")
        continue

    ask_database(question)