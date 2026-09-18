import re


# =========================================================
# Database schema
# =========================================================

SCHEMA = """
Table: employees

Columns:
- employee_id       INTEGER
- name              TEXT
- department        TEXT
- salary            INTEGER
- location          TEXT
- experience_years  INTEGER
"""


# =========================================================
# Department mapping
# =========================================================

DEPARTMENT_MAP = {
    "data": "Data",
    "hr": "HR",
    "finance": "Finance",
    "it": "IT"
}


# =========================================================
# Location mapping
# =========================================================

LOCATION_MAP = {
    "pune": "Pune",
    "mumbai": "Mumbai",
    "delhi": "Delhi",
    "bengaluru": "Bengaluru"
}


# =========================================================
# Natural Language → SQL
# =========================================================

def generate_sql(question: str) -> str:

    question_lower = question.lower().strip()

    # -----------------------------------------------------
    # 1. Department detection
    # -----------------------------------------------------

    department = None

    for key, value in DEPARTMENT_MAP.items():
        if re.search(rf"\b{key}\b", question_lower):
            department = value
            break

    # -----------------------------------------------------
    # 2. Salary condition
    # -----------------------------------------------------

    salary_match = re.search(
        r"(?:more than|above|over|greater than|higher than)\s*₹?\s*(\d+)",
        question_lower
    )

    if department and salary_match:

        salary = salary_match.group(1)

        return f"""
SELECT name, department, salary
FROM employees
WHERE department = '{department}'
AND salary > {salary}
ORDER BY salary DESC;
""".strip()

    # -----------------------------------------------------
    # 3. Employees by department
    # -----------------------------------------------------

    department_phrases = [
        "employees from",
        "employees in",
        "employees of",
        "employees belonging to",
        "people in",
        "people from",
        "staff in",
        "staff from",
        "which employees",
        "show me employees",
        "show employees",
        "list employees",
        "list all employees"
    ]

    if department:

        for phrase in department_phrases:

            if phrase in question_lower:

                return f"""
SELECT name, department, salary
FROM employees
WHERE department = '{department}'
ORDER BY salary DESC;
""".strip()

    # -----------------------------------------------------
    # 4. Employees by location
    # -----------------------------------------------------

    location = None

    for key, value in LOCATION_MAP.items():

        if re.search(rf"\b{key}\b", question_lower):
            location = value
            break

    if location:

        return f"""
SELECT name, department, salary, location
FROM employees
WHERE location = '{location}'
ORDER BY salary DESC;
""".strip()

    # -----------------------------------------------------
    # 5. Average salary
    # -----------------------------------------------------

    if (
        "average salary" in question_lower
        or "avg salary" in question_lower
        or "mean salary" in question_lower
    ):

        return """
SELECT AVG(salary) AS average_salary
FROM employees;
""".strip()

    # -----------------------------------------------------
    # 6. Employees above average salary
    # -----------------------------------------------------

    if (
        "above the average" in question_lower
        or "above average salary" in question_lower
        or "greater than average salary" in question_lower
        or "higher than average salary" in question_lower
        or "more than the average salary" in question_lower
    ):

        return """
SELECT name, department, salary
FROM employees
WHERE salary > (
    SELECT AVG(salary)
    FROM employees
)
ORDER BY salary DESC;
""".strip()

    # -----------------------------------------------------
    # 7. Highest salary
    # -----------------------------------------------------

    if (
        "highest salary" in question_lower
        or "highest paid" in question_lower
        or "maximum salary" in question_lower
        or "top paid employee" in question_lower
    ):

        return """
SELECT name, department, salary
FROM employees
ORDER BY salary DESC
LIMIT 1;
""".strip()

    # -----------------------------------------------------
    # 8. Lowest salary
    # -----------------------------------------------------

    if (
        "lowest salary" in question_lower
        or "lowest paid" in question_lower
        or "minimum salary" in question_lower
    ):

        return """
SELECT name, department, salary
FROM employees
ORDER BY salary ASC
LIMIT 1;
""".strip()

    # -----------------------------------------------------
    # 9. Employee count
    # -----------------------------------------------------

    if (
        "how many employees" in question_lower
        or "employee count" in question_lower
        or "number of employees" in question_lower
    ):

        return """
SELECT COUNT(*) AS employee_count
FROM employees;
""".strip()

    # -----------------------------------------------------
    # 10. Unsupported question
    # -----------------------------------------------------

    return ""


# =========================================================
# Test
# =========================================================

if __name__ == "__main__":

    question = input("\nEnter your question: ").strip()

    sql = generate_sql(question)

    print("\n======================================")
    print("GENERATED SQL")
    print("======================================")

    if sql:
        print(sql)
    else:
        print("I don't know how to convert this question yet.")