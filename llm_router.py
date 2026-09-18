import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


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
# 3. Router prompt
# =========================================================

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a routing system for the TechNova Business Assistant.

Classify the user's request into exactly ONE category:

rag
sql
calculator
workflow
unknown


RAG:
Use RAG when the user asks for information from company
documents, policies, rules, procedures, or internal knowledge.

Examples:
- How many work-from-home days are allowed?
- What is the leave policy?
- What is the hotel reimbursement limit?
- What does the IT security policy say?
- How many sick leave days are provided?
- What are the rules for remote access?


SQL:
Use SQL when the user asks for information from the
employee database.

Examples:
- Show employees from IT.
- Which employees work in Pune?
- What is the average salary?
- Which employees earn above 70000?
- How many employees are there?
- Show employees with more than 5 years of experience.


CALCULATOR:
Use calculator when the request is primarily a
mathematical calculation.

Examples:
- What is 4000 multiplied by 3?
- Calculate 12000 / 4.
- What is 500 + 250?


WORKFLOW:
Use workflow when the user describes an operational
problem, request, incident, or action that needs to
be handled.

Examples:
- My travel reimbursement was rejected.
- I forgot my hotel receipt.
- My expense claim was rejected.
- My company laptop was lost.
- I forgot my company password.
- Create or escalate a support request.


IMPORTANT DISTINCTION:

If the user asks ABOUT a policy:
→ rag

If the user describes a PROBLEM or requests an ACTION:
→ workflow

Examples:

"What is the hotel reimbursement limit?"
→ rag

"My hotel reimbursement was rejected."
→ workflow

"Are receipts required for travel expenses?"
→ rag

"I forgot my travel receipt and my reimbursement was rejected."
→ workflow

"What is the company laptop security policy?"
→ rag

"My company laptop was lost."
→ workflow


UNKNOWN:
Use unknown when the request does not fit any category.


Return ONLY ONE WORD:

rag
sql
calculator
workflow
unknown

Do not explain your answer.
Do not return punctuation.
Do not return markdown.
"""
    ),
    (
        "human",
        "{question}"
    )
])


# =========================================================
# 4. Create router chain
# =========================================================

router_chain = prompt | model


# =========================================================
# 5. LLM Router Function
# =========================================================

def llm_route_question(question: str) -> str:

    response = router_chain.invoke({
        "question": question
    })

    # -----------------------------------------------------
    # Get response text
    # -----------------------------------------------------

    if isinstance(response.content, str):

        route = response.content.strip().lower()

    else:

        route = ""

        for item in response.content:

            if (
                isinstance(item, dict)
                and item.get("type") == "text"
            ):
                route += item.get("text", "")

        route = route.strip().lower()


    # -----------------------------------------------------
    # Clean output
    # -----------------------------------------------------

    route = route.replace("`", "")
    route = route.replace(".", "")
    route = route.replace("\n", "")
    route = route.strip()


    # -----------------------------------------------------
    # Validate route
    # -----------------------------------------------------

    allowed_routes = {
        "rag",
        "sql",
        "calculator",
        "workflow",
        "unknown"
    }

    if route not in allowed_routes:

        return "unknown"

    return route


# =========================================================
# 6. Standalone Router Test
# =========================================================
# IMPORTANT:
# This section runs ONLY when you execute:
# python llm_router.py
#
# It does NOT run when langgraph_workflow.py imports this file.
# =========================================================

if __name__ == "__main__":

    print("\n==============================================")
    print("       TECHNOVA LLM ROUTER")
    print("==============================================")

    print("Available routes:")
    print("- rag")
    print("- sql")
    print("- calculator")
    print("- workflow")
    print("- unknown")

    print("\nType 'exit' to stop.")


    while True:

        question = input("\nQuestion: ").strip()

        if question.lower() == "exit":

            print("\nLLM Router stopped.")
            break

        if not question:

            print("Please enter a question.")
            continue

        route = llm_route_question(question)

        print("\nRoute:", route)