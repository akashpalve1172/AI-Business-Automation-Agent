import os
import re

from dotenv import load_dotenv

from langchain.tools import tool
from langchain.agents import create_agent

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI


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
# 2. Load embedding model
# =========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# 3. Load Chroma vector database
# =========================================================

vector_store = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=embeddings,
    collection_name="company_policies"
)


# =========================================================
# 4. Create Policy Search Tool
# =========================================================

@tool
def search_company_policy(question: str) -> str:
    """
    Search TechNova Solutions company policy documents
    and return relevant information.

    Use this tool for questions about:
    - Work from home
    - Leave
    - Travel
    - Expenses
    - IT and security policies
    """

    results = vector_store.similarity_search(
        question,
        k=3
    )

    if not results:
        return "No relevant company policy information was found."

    output = []

    for document in results:

        source = document.metadata.get(
            "source",
            "Unknown source"
        )

        content = document.page_content

        output.append(
            f"SOURCE: {source}\n"
            f"CONTENT:\n{content}"
        )

    return "\n\n".join(output)


# =========================================================
# 5. Create Calculator Tool
# =========================================================

@tool
def calculator(expression: str) -> str:
    """
    Perform basic arithmetic calculations.

    Supported operations:
    +  addition
    -  subtraction
    *  multiplication
    /  division
    """

    # Allow only numbers, spaces and basic operators
    if not re.fullmatch(
        r"[0-9+\-*/().\s]+",
        expression
    ):
        return "Invalid mathematical expression."

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception:
        return "Unable to calculate the expression."


# =========================================================
# 6. Create Gemini model
# =========================================================

model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key
)


# =========================================================
# 7. Create AI Agent
# =========================================================

agent = create_agent(
    model=model,
    tools=[
        search_company_policy,
        calculator
    ],
    system_prompt="""
You are the TechNova Solutions AI Business Assistant.

You have access to tools that help you answer user questions.

AVAILABLE TOOLS:

1. search_company_policy
Use this for questions about company policies,
employee rules, WFH, leave, travel, expenses,
IT security, and other company information.

2. calculator
Use this for mathematical calculations.

RULES:

- Decide which tool is appropriate for the user's request.
- Use a tool when it is needed.
- Do not invent company policy information.
- For policy questions, rely on the policy-search tool.
- Give clear and concise answers.
- Mention the relevant policy source when available.
"""
)


# =========================================================
# 8. Function to run the agent
# =========================================================

def ask_agent(question: str):

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    messages = result.get("messages", [])

    if not messages:
        print("No response received.")
        return

    final_message = messages[-1]

    print("\n" + "=" * 50)
    print("AI AGENT ANSWER")
    print("=" * 50)

    content = final_message.content

    if isinstance(content, str):
        print(content)

    else:
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    print(item.get("text", ""))


# =========================================================
# 9. Interactive loop
# =========================================================

print("\n==============================================")
print("     TECHNOVA AI BUSINESS AGENT")
print("==============================================")

print("The agent can use:")
print("- Company Policy Search")
print("- Calculator")

print("\nType 'exit' to close the application.")


while True:

    question = input("\nYour question: ").strip()

    if question.lower() == "exit":
        print("\nAgent stopped.")
        break

    if not question:
        print("Please enter a question.")
        continue

    ask_agent(question)