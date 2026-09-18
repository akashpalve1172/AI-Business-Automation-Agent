import os
import re

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# =========================================================
# 1. Load API key
# =========================================================

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY was not found in the .env file."
    )


# =========================================================
# 2. Connect to Gemini
# =========================================================

model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key
)


# =========================================================
# 3. Database schema
# =========================================================

SCHEMA = """
Database: SQLite

Table: employees

Columns:
- employee_id       INTEGER
- name              TEXT
- department        TEXT
- salary            INTEGER
- location          TEXT
- experience_years  INTEGER

Allowed table:
- employees

Only SELECT queries are allowed.
"""


# =========================================================
# 4. Generate SQL using Gemini
# =========================================================

def generate_sql_with_llm(question: str) -> str:

    full_prompt = f"""
You are an SQL generation assistant for the TechNova
Solutions employee database.

Your job is to convert the user's natural-language question
into ONE valid SQLite SELECT query.

DATABASE SCHEMA:
{SCHEMA}

STRICT RULES:

1. Use ONLY the employees table.
2. Use ONLY columns listed in the schema.
3. Generate ONLY one SELECT statement.
4. Never generate INSERT.
5. Never generate UPDATE.
6. Never generate DELETE.
7. Never generate DROP.
8. Never generate ALTER.
9. Never generate CREATE.
10. Never generate PRAGMA.
11. Never generate ATTACH or DETACH.
12. Never generate multiple SQL statements.
13. Return ONLY the SQL query.
14. Do not explain the query.
15. Do not use markdown code fences.
16. Use SQLite-compatible SQL.

USER QUESTION:
{question}
"""

    # Direct string input to Gemini
    response = model.invoke(full_prompt)

    # -----------------------------------------------------
    # Get response text
    # -----------------------------------------------------

    if isinstance(response.content, str):

        sql = response.content

    else:

        sql = ""

        for item in response.content:

            if (
                isinstance(item, dict)
                and item.get("type") == "text"
            ):
                sql += item.get("text", "")

    return clean_sql(sql)


# =========================================================
# 5. Clean SQL output
# =========================================================

def clean_sql(raw_sql: str) -> str:

    sql = raw_sql.strip()

    # Remove markdown code fences if Gemini adds them
    sql = re.sub(
        r"^```sql\s*",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r"^```\s*",
        "",
        sql
    )

    sql = re.sub(
        r"\s*```$",
        "",
        sql
    )

    return sql.strip()


# =========================================================
# 6. Standalone test
# =========================================================

if __name__ == "__main__":

    print("\n==============================================")
    print("          LLM SQL GENERATOR")
    print("==============================================")

    question = input(
        "\nEnter your database question: "
    ).strip()

    if not question:

        print("Please enter a question.")

    else:

        sql = generate_sql_with_llm(question)

        print("\n======================================")
        print("GENERATED SQL")
        print("======================================")

        print(sql)