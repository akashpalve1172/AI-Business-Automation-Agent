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
# 3. Response prompt
# =========================================================

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are the final response agent for TechNova Solutions.

Your job is to turn retrieved system results into a
clear answer for the employee.

Rules:
1. Use ONLY the supplied information.
2. Do not invent facts.
3. Answer the user's question directly.
4. Keep the answer concise.
5. Mention important conditions such as manager approval
   when they are relevant.
6. Do not reproduce large sections of documents.
7. Mention the source document at the end.

Retrieved Information:
{context}
"""
    ),
    (
        "human",
        "{question}"
    )
])


# =========================================================
# 4. Response function
# =========================================================

def generate_final_response(
    question: str,
    context: str
) -> str:

    chain = prompt | model

    response = chain.invoke({
        "question": question,
        "context": context
    })

    if isinstance(response.content, str):
        return response.content

    text = ""

    for item in response.content:

        if (
            isinstance(item, dict)
            and item.get("type") == "text"
        ):
            text += item.get("text", "")

    return text.strip()