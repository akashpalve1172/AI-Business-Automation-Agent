from pathlib import Path
import re


# =========================================================
# DOCUMENT LOCATION
# =========================================================

DOCUMENTS_PATH = Path("data/documents")


# =========================================================
# LOAD DOCUMENTS
# =========================================================

def load_documents():
    documents = []

    for file_path in DOCUMENTS_PATH.glob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append({
            "source": file_path.name,
            "text": text
        })

    return documents


# =========================================================
# TOKENIZE
# =========================================================

def tokenize(text):

    return set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text.lower()
        )
    )


# =========================================================
# SPLIT TEXT INTO SENTENCES
# =========================================================

def split_sentences(text):

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


# =========================================================
# RETRIEVE RELEVANT SENTENCES
# =========================================================

def retrieve_documents(question, top_k=1):

    documents = load_documents()

    question_words = tokenize(question)

    candidates = []

    for document in documents:

        sentences = split_sentences(
            document["text"]
        )

        for sentence in sentences:

            sentence_words = tokenize(sentence)

            score = len(
                question_words.intersection(
                    sentence_words
                )
            )

            if score > 0:

                candidates.append({
                    "source": document["source"],
                    "sentence": sentence,
                    "score": score
                })

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return candidates[:top_k]


# =========================================================
# FAST RAG ANSWER
# =========================================================

def fast_rag_answer(question):

    results = retrieve_documents(
        question,
        top_k=1
    )

    if not results:

        return {
            "source": "No matching document",
            "answer": "No relevant company policy was found.",
            "context": "No relevant company policy was found."
        }

    best_result = results[0]

    return {
        "source": best_result["source"],
        "answer": best_result["sentence"],
        "context": best_result["sentence"]
    }