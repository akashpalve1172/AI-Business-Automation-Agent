from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# =========================================================
# Load embedding model
# =========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# Load Chroma database
# =========================================================

vector_store = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=embeddings,
    collection_name="company_policies"
)


# =========================================================
# Search company policies
# =========================================================

def search_policy(question: str) -> str:

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

        output.append(
            f"Source: {source}\n"
            f"{document.page_content}"
        )

    return "\n\n".join(output)