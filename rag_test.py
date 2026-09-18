from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Location of our documents
documents_path = Path("data/documents")

# Load WFH policy
file_path = documents_path / "WFH_Policy.txt"

loader = TextLoader(
    str(file_path),
    encoding="utf-8"
)

documents = loader.load()

print("Number of documents loaded:", len(documents))

# Split the document into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print("Number of chunks created:", len(chunks))

# Display chunks
for i, chunk in enumerate(chunks):
    print(f"\n--- CHUNK {i + 1} ---")
    print(chunk.page_content)