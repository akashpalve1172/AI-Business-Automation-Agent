from workflow_agent import process_business_request


# =========================================================
# Workflow Agent Test
# =========================================================

print("\n==============================================")
print("       TECHNOVA WORKFLOW AGENT")
print("==============================================")


question = input("\nEnter your business request: ").strip()


if not question:

    print("\nPlease enter a request.")

else:

    result = process_business_request(question)

    print("\n==============================================")
    print("WORKFLOW RESULT")
    print("==============================================")

    print(result)