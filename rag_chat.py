import os

from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
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
# 2. Load embedding model
# =========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# 3. Load existing Chroma database
# =========================================================

vector_store = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=embeddings,
    collection_name="company_policies"
)

print("\nVector database loaded successfully.")


# =========================================================
# 4. Connect to Gemini
# =========================================================

model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key
)


# =========================================================
# 5. Create RAG prompt
# =========================================================

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an enterprise employee assistance AI for TechNova Solutions.

Your task is to answer employee questions using ONLY the
information provided in the retrieved company documents.

Rules:
1. Do not invent company policies or facts.
2. Do not use outside knowledge when answering company-policy questions.
3. If the retrieved context does not contain enough information,
   say exactly:

   "I could not find this information in the available company documents."

4. Give a clear and professional answer.
5. Keep the answer concise.
6. Mention the relevant source document.
7. If the policy contains conditions or approval requirements,
   mention them when relevant.

Retrieved Context:
{context}
"""
    ),
    (
        "human",
        "{question}"
    )
])


# =========================================================
# 6. Function to ask a question
# =========================================================

def ask_question(question: str):

    # -----------------------------------------------------
    # Search for the most relevant document chunks
    # -----------------------------------------------------

    results = vector_store.similarity_search(
        question,
        k=5
    )

   
    # -----------------------------------------------------
    # Check if anything was retrieved
    # -----------------------------------------------------

    if not results:
        print("\nNo relevant information was found.")
        return

    # -----------------------------------------------------
    # Combine retrieved chunks into context
    # -----------------------------------------------------

    context = "\n\n".join(
        document.page_content
        for document in results
    )

    # -----------------------------------------------------
    # Send context + question to Gemini
    # -----------------------------------------------------

    chain = prompt | model

    response = chain.invoke({
        "context": context,
        "question": question
    })

    # -----------------------------------------------------
    # Display answer
    # -----------------------------------------------------

    print("\n" + "=" * 50)
    print("AI ANSWER")
    print("=" * 50)

    if isinstance(response.content, str):
        print(response.content)

    else:
        for item in response.content:
            if isinstance(item, dict) and item.get("type") == "text":
                print(item.get("text", ""))

    # -----------------------------------------------------
    # Display sources
    # -----------------------------------------------------

    print("\n" + "=" * 50)
    print("SOURCES")
    print("=" * 50)

    sources = set()

    for document in results:
        source = document.metadata.get("source")

        if source:
            sources.add(source)

    for source in sources:
        print(source)


# =========================================================
# 7. Interactive question loop
# =========================================================

print("\n==============================================")
print("   TECHNOVA AI EMPLOYEE ASSISTANT")
print("==============================================")
print("Ask a question about company policies.")
print("Type 'exit' to close the application.")


while True:

    question = input("\nYour question: ").strip()

    if question.lower() == "exit":
        print("\nThank you for using TechNova AI Assistant.")
        break

    if not question:
        print("Please enter a question.")
        continue

    ask_question(question)