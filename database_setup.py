import sqlite3
from pathlib import Path


# =========================================================
# 1. Database location
# =========================================================

database_folder = Path("data")
database_folder.mkdir(exist_ok=True)

database_path = database_folder / "company.db"


# =========================================================
# 2. Connect to SQLite
# =========================================================

connection = sqlite3.connect(database_path)

cursor = connection.cursor()


# =========================================================
# 3. Create employees table
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary INTEGER NOT NULL,
    location TEXT NOT NULL,
    experience_years INTEGER NOT NULL
)
""")


# =========================================================
# 4. Insert sample employee data
# =========================================================

employees = [
    (101, "Rahul", "Data", 60000, "Pune", 2),
    (102, "Priya", "HR", 45000, "Mumbai", 3),
    (103, "Amit", "Data", 75000, "Pune", 5),
    (104, "Sneha", "Finance", 65000, "Bengaluru", 4),
    (105, "Rohan", "IT", 80000, "Pune", 6),
    (106, "Neha", "HR", 50000, "Delhi", 2),
    (107, "Karan", "Data", 70000, "Mumbai", 4),
    (108, "Pooja", "IT", 72000, "Pune", 3),
    (109, "Vikas", "Finance", 68000, "Mumbai", 5),
    (110, "Anjali", "Data", 55000, "Delhi", 1),
]


cursor.executemany("""
INSERT OR IGNORE INTO employees
(employee_id, name, department, salary, location, experience_years)
VALUES (?, ?, ?, ?, ?, ?)
""", employees)


# =========================================================
# 5. Save changes
# =========================================================

connection.commit()


# =========================================================
# 6. Check records
# =========================================================

cursor.execute("""
SELECT *
FROM employees
""")

rows = cursor.fetchall()

print("\n======================================")
print("EMPLOYEE DATABASE")
print("======================================")

for row in rows:
    print(row)


# =========================================================
# 7. Close database
# =========================================================

connection.close()

print("\nDatabase created successfully!")
print(f"Location: {database_path}")