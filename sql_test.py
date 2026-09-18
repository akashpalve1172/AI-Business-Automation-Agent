import sqlite3


# =========================================================
# 1. Connect to database
# =========================================================

connection = sqlite3.connect("data/company.db")

cursor = connection.cursor()


# =========================================================
# 2. SQL query
# =========================================================

query = """
SELECT name, department, salary
FROM employees
WHERE department = 'Data'
"""

cursor.execute(query)

results = cursor.fetchall()


# =========================================================
# 3. Display results
# =========================================================

print("\n======================================")
print("DATA DEPARTMENT EMPLOYEES")
print("======================================")

for row in results:
    print(
        f"Name: {row[0]} | "
        f"Department: {row[1]} | "
        f"Salary: ₹{row[2]}"
    )


# =========================================================
# 4. Close connection
# =========================================================

connection.close()