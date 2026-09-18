from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# =========================================================
# 1. Document location
# =========================================================

documents_path = Path("data/documents")

files = list(documents_path.glob("*.txt"))

if not files:
    raise FileNotFoundError(
        "No .txt documents found inside data/documents"
    )

print(f"Found {len(files)} documents.")


# =========================================================
# 2. Load all documents
# =========================================================

documents = []

for file_path in files:

    loader = TextLoader(
        str(file_path),
        encoding="utf-8"
    )

    loaded_documents = loader.load()

    documents.extend(loaded_documents)

    print(f"Loaded: {file_path.name}")


# =========================================================
# 3. Split documents
# =========================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

print(f"\nCreated {len(chunks)} chunks.")


# =========================================================
# 4. Create embeddings
# =========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded.")


# =========================================================
# 5. Create fresh Chroma database
# =========================================================

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="data/chroma_db",
    collection_name="company_policies"
)

print("\nVector database created successfully!")
print("Location: data/chroma_db")