from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# =========================================================
# 1. Load embedding model
# =========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# 2. Load Chroma database
# =========================================================

vector_store = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=embeddings,
    collection_name="company_policies"
)


# =========================================================
# 3. Test question
# =========================================================

question = "Can employees work remotely twice every week?"


# =========================================================
# 4. Search
# =========================================================

results = vector_store.similarity_search(
    question,
    k=3
)


# =========================================================
# 5. Display results
# =========================================================

print("\n======================================")
print("RETRIEVAL TEST")
print("======================================")

for i, document in enumerate(results, start=1):

    print(f"\n--- RESULT {i} ---")

    print("SOURCE:")
    print(document.metadata.get("source"))

    print("\nCONTENT:")
    print(document.page_content)