import sqlite3

from langchain.tools import tool


# =========================================================
# Database path
# =========================================================

DATABASE_PATH = "data/company.db"


# =========================================================
# SQL Tool
# =========================================================

@tool
def execute_sql(query: str) -> str:
    """
    Execute a read-only SQL query against the company database.

    Use this tool for retrieving employee information,
    departments, salaries, locations, and experience.

    Only SELECT queries are allowed.
    """

    # -----------------------------------------------------
    # Safety check
    # -----------------------------------------------------

    query = query.strip()

    if not query:
        return "Error: SQL query is empty."

    if not query.lower().startswith("select"):
        return "Error: Only SELECT queries are allowed."

    # -----------------------------------------------------
    # Connect to database
    # -----------------------------------------------------

    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        # -------------------------------------------------
        # Execute query
        # -------------------------------------------------

        cursor.execute(query)

        rows = cursor.fetchall()

        # Get column names
        column_names = [
            description[0]
            for description in cursor.description
        ]

        connection.close()

        # -------------------------------------------------
        # No results
        # -------------------------------------------------

        if not rows:
            return "No matching records were found."

        # -------------------------------------------------
        # Format results
        # -------------------------------------------------

        output = []

        output.append(
            " | ".join(column_names)
        )

        output.append(
            "-" * 60
        )

        for row in rows:

            output.append(
                " | ".join(
                    str(value)
                    for value in row
                )
            )

        return "\n".join(output)

    except sqlite3.Error as error:

        return f"SQL Error: {error}"