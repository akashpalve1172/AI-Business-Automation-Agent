import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Load API key
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY was not found in the .env file.")

# Connect to Gemini
model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key
)

# Create a structured prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an Employee Assistance AI for a company.

Your responsibilities:
1. Answer employee questions clearly and professionally.
2. Keep answers simple and easy to understand.
3. Do not invent company policies or facts.
4. When information is unavailable, clearly say that you do not have enough information.
5. Do not make assumptions.
6. Give the answer first, followed by a short explanation.
"""
    ),
    (
        "human",
        "{question}"
    )
])

# Create the prompt + model pipeline
chain = prompt | model

# Ask the AI
question = "What should I do if I forget my company laptop password?"

response = chain.invoke({
    "question": question
})

print("\nAI RESPONSE:\n")

if isinstance(response.content, str):
    print(response.content)
else:
    for item in response.content:
        if isinstance(item, dict) and item.get("type") == "text":
            print(item.get("text", ""))