import re


# =========================================================
# Question Router
# =========================================================

def route_question(question: str) -> str:

    question_lower = question.lower().strip()


    # =====================================================
    # 1. RAG / Company Policy questions
    # =====================================================
    # Check policy intent FIRST.
    # This prevents words like "employee" or "salary"
    # from incorrectly overriding an obvious policy question.

    policy_keywords = [
        "work from home",
        "working from home",
        "wfh",
        "work remotely",
        "working remotely",
        "remote work",
        "remote",
        "leave policy",
        "annual leave",
        "sick leave",
        "leave",
        "travel policy",
        "business travel",
        "hotel reimbursement",
        "travel reimbursement",
        "expense policy",
        "expense claim",
        "expense",
        "reimbursement",
        "receipt",
        "it policy",
        "it security",
        "password",
        "security incident",
        "lost laptop",
        "lost device",
        "company laptop",
        "software installation",
        "remote access",
        "policy",
    ]

    for keyword in policy_keywords:

        if keyword in question_lower:
            return "rag"


    # =====================================================
    # 2. Calculator questions
    # =====================================================

    calculation_patterns = [
        r"\d+\s*\+\s*\d+",
        r"\d+\s*-\s*\d+",
        r"\d+\s*\*\s*\d+",
        r"\d+\s*/\s*\d+",
        r"what is \d+",
        r"calculate",
        r"multiply",
        r"divide",
        r"subtract",
        r"add"
    ]

    for pattern in calculation_patterns:

        if re.search(pattern, question_lower):
            return "calculator"


    # =====================================================
    # 3. SQL / Employee Database questions
    # =====================================================

    database_keywords = [
        "employee",
        "employees",
        "salary",
        "salaries",
        "department",
        "location",
        "experience",
        "average salary",
        "highest salary",
        "lowest salary",
        "employee count",
        "number of employees",
        "data department",
        "it department",
        "hr department",
        "finance department"
    ]

    for keyword in database_keywords:

        if keyword in question_lower:
            return "sql"


    # =====================================================
    # 4. Unknown question
    # =====================================================

    return "unknown"


# =========================================================
# Test Router
# =========================================================

if __name__ == "__main__":

    print("\n======================================")
    print("TECHNOVA QUESTION ROUTER")
    print("======================================")

    print("Type 'exit' to stop.")

    while True:

        question = input("\nQuestion: ").strip()

        if question.lower() == "exit":
            print("\nRouter stopped.")
            break

        route = route_question(question)

        print("\nRoute:", route)