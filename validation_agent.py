# =========================================================
# Validation Agent
# =========================================================


def validate_rag_result(result: str) -> dict:
    """
    Validate the result returned by the RAG system.
    """

    if not result or not result.strip():
        return {
            "status": "failed",
            "message": "RAG returned no information."
        }

    # Check whether a source is available
    if "Source:" not in result:
        return {
            "status": "warning",
            "message": "RAG returned information but no source was detected."
        }

    return {
        "status": "passed",
        "message": "RAG result contains information and a source."
    }


# =========================================================
# SQL validation
# =========================================================

def validate_sql_result(result: str) -> dict:
    """
    Validate the result returned by the SQL tool.
    """

    if not result or not result.strip():
        return {
            "status": "failed",
            "message": "SQL tool returned no result."
        }

    # Check for known SQL validation/error messages
    error_messages = [
        "SQL validation failed",
        "SQL Error:",
        "Only SELECT queries are allowed",
        "Forbidden SQL keyword detected",
        "Multiple SQL statements are not allowed"
    ]

    for error_message in error_messages:

        if error_message.lower() in result.lower():

            return {
                "status": "failed",
                "message": f"SQL result contains an error: {error_message}"
            }

    return {
        "status": "passed",
        "message": "SQL query executed successfully."
    }


# =========================================================
# Calculator validation
# =========================================================

def validate_calculator_result(result: str) -> dict:
    """
    Validate the result returned by the calculator.
    """

    if not result or not result.strip():
        return {
            "status": "failed",
            "message": "Calculator returned no result."
        }

    error_messages = [
        "Invalid mathematical expression",
        "Unable to calculate"
    ]

    for error_message in error_messages:

        if error_message.lower() in result.lower():

            return {
                "status": "failed",
                "message": f"Calculator error: {error_message}"
            }

    return {
        "status": "passed",
        "message": "Calculation completed successfully."
    }


# =========================================================
# Main validation function
# =========================================================

def validate_result(route: str, result: str) -> dict:
    """
    Select the appropriate validation process based
    on the route.
    """

    if route == "rag":

        return validate_rag_result(result)

    if route == "sql":

        return validate_sql_result(result)

    if route == "calculator":

        return validate_calculator_result(result)

    return {
        "status": "warning",
        "message": "No specialized validator exists for this route."
    }


# =========================================================
# Standalone test
# =========================================================

if __name__ == "__main__":

    print("\n==============================================")
    print("       VALIDATION AGENT TEST")
    print("==============================================")


    # -----------------------------------------------------
    # Test RAG
    # -----------------------------------------------------

    rag_result = """
    Source: data\\documents\\WFH_Policy.txt

    Employees may work from home for a maximum
    of 2 days per week.
    """

    validation = validate_result(
        "rag",
        rag_result
    )

    print("\nRAG VALIDATION:")
    print(validation)


    # -----------------------------------------------------
    # Test SQL
    # -----------------------------------------------------

    sql_result = """
    name | department | salary
    ------------------------------------------------------------
    Rohan | IT | 80000
    Pooja | IT | 72000
    """

    validation = validate_result(
        "sql",
        sql_result
    )

    print("\nSQL VALIDATION:")
    print(validation)


    # -----------------------------------------------------
    # Test Calculator
    # -----------------------------------------------------

    calculator_result = "4000*3 = 12000"

    validation = validate_result(
        "calculator",
        calculator_result
    )

    print("\nCALCULATOR VALIDATION:")
    print(validation)


    # -----------------------------------------------------
    # Test failed SQL
    # -----------------------------------------------------

    failed_sql_result = "SQL validation failed: Only SELECT queries are allowed."

    validation = validate_result(
        "sql",
        failed_sql_result
    )

    print("\nFAILED SQL VALIDATION:")
    print(validation)