from policy_tool import search_policy
from sql_generator import generate_sql
from sql_tool import execute_sql
from calculator_tool import calculate
from workflow_agent import process_business_request


# =========================================================
# Test counters
# =========================================================

passed = 0
failed = 0


# =========================================================
# Helper function
# =========================================================

def record_test(
    test_name: str,
    condition: bool,
    details: str
):
    global passed, failed

    if condition:

        print(f"[PASS] {test_name}")
        passed += 1

    else:

        print(f"[FAIL] {test_name}")
        print(f"       {details}")
        failed += 1


# =========================================================
# 1. RAG Tests
# =========================================================

print("\n==============================================")
print("RAG TESTS")
print("==============================================")


# Test 1
result = search_policy(
    "How many days can employees work from home?"
)

record_test(
    "WFH policy retrieval",
    "2 days per week" in result,
    "Expected the WFH allowance to be retrieved."
)


# Test 2
result = search_policy(
    "How many annual paid leave days are provided?"
)

record_test(
    "Annual leave retrieval",
    "24 days" in result,
    "Expected 24 annual paid leave days."
)


# Test 3
result = search_policy(
    "What is the hotel reimbursement limit?"
)

record_test(
    "Travel policy retrieval",
    "4,000" in result or "4000" in result,
    "Expected hotel limit of INR 4,000 per night."
)


# =========================================================
# 2. SQL Tests
# =========================================================

print("\n==============================================")
print("SQL TESTS")
print("==============================================")


# Test 4
sql = generate_sql(
    "Show me employees from the IT department"
)

record_test(
    "Department SQL generation",
    "WHERE department = 'IT'" in sql,
    "Expected SQL filter for IT department."
)


# Test 5
sql = generate_sql(
    "Show me Data employees earning more than 65000"
)

record_test(
    "Salary-filter SQL generation",
    "salary > 65000" in sql
    and "department = 'Data'" in sql,
    "Expected Data department and salary filter."
)


# Test 6
sql = generate_sql(
    "What is the average salary?"
)

record_test(
    "Average salary SQL generation",
    "AVG(salary)" in sql,
    "Expected AVG(salary) query."
)


# Test 7
sql = generate_sql(
    "Show me employees from the IT department"
)

database_result = execute_sql.invoke(sql)

record_test(
    "SQL database execution",
    "Rohan" in database_result
    and "Pooja" in database_result,
    "Expected IT employees in database result."
)


# =========================================================
# 3. Calculator Tests
# =========================================================

print("\n==============================================")
print("CALCULATOR TESTS")
print("==============================================")


# Test 8
result = calculate("4000*3")

record_test(
    "Multiplication",
    result == "12000",
    "Expected 4000 * 3 = 12000."
)


# Test 9
result = calculate("12000/4")

record_test(
    "Division",
    result == "3000.0",
    "Expected 12000 / 4 = 3000."
)


# =========================================================
# 4. Workflow Tests
# =========================================================

print("\n==============================================")
print("WORKFLOW TESTS")
print("==============================================")


# Test 10
result = process_business_request(
    "My travel reimbursement was rejected because I forgot the hotel receipt."
)

record_test(
    "Travel reimbursement workflow",
    "Travel Reimbursement" in result
    and "hotel receipt" in result.lower()
    and "Pending employee action" in result,
    "Expected reimbursement workflow with missing receipt."
)


# Test 11
result = process_business_request(
    "My company laptop was lost."
)

record_test(
    "Lost equipment workflow",
    "Lost Company Equipment" in result
    and "IT Support" in result,
    "Expected lost-device workflow."
)


# Test 12
result = process_business_request(
    "I forgot my company password."
)

record_test(
    "Password assistance workflow",
    "IT Password Assistance" in result
    and "IT Support" in result,
    "Expected password-support workflow."
)


# =========================================================
# Final report
# =========================================================

total = passed + failed

print("\n==============================================")
print("EVALUATION SUMMARY")
print("==============================================")

print(f"Total tests : {total}")
print(f"Passed      : {passed}")
print(f"Failed      : {failed}")

if failed == 0:

    print("\nOverall result: ALL TESTS PASSED")

else:

    print(
        f"\nOverall result: {failed} test(s) need attention."
    )