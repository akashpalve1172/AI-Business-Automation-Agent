from sql_tool import execute_sql


# =========================================================
# Test 1
# =========================================================

query = """
SELECT name, salary
FROM employees
WHERE salary > 65000
ORDER BY salary DESC
"""

result = execute_sql.invoke(query)

print("\n======================================")
print("SQL TOOL RESULT")
print("======================================")

print(result)