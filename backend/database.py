import os
from pathlib import Path

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "docmind_ai"


def _get_embeddings_model():
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def get_chroma_collection():
    """
    Initialize or return a persistent ChromaDB collection.
    """
    persist_dir = Path("./chroma_db")
    persist_dir.mkdir(exist_ok=True)

    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=str(persist_dir)))

    if COLLECTION_NAME in [col.name for col in client.list_collections()]:
        return client.get_collection(name=COLLECTION_NAME)

    return client.create_collection(name=COLLECTION_NAME, metadata={})


def index_chunks(doc_id, chunks, collection):
    """
    Embed and index chunks into ChromaDB. Returns number of chunks added.
    """
    if not chunks:
        return 0

    texts = [chunk["text"] for chunk in chunks]
    metadatas = [{"page": chunk["page"], "clause": chunk["clause"], "doc_id": doc_id} for chunk in chunks]
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]

    collection.add(ids=ids, documents=texts, metadatas=metadatas)
    return len(chunks)


def retrieve_chunks(question, doc_id, collection, top_k=5):
    """
    Retrieve the top-k most relevant chunks for a question from ChromaDB.
    """
    if not question or not doc_id:
        return []

    question_embedding = _get_embeddings_model().encode(question, convert_to_numpy=True).tolist()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
        where={"doc_id": doc_id},
        include=['documents', 'metadatas'],
    )

    if not results or not results.get("documents"):
        return []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    retrieved = []
    for text, metadata in zip(documents, metadatas):
        if not metadata:
            continue
        retrieved.append(
            {"text": text, "page": metadata.get("page"), "clause": metadata.get("clause")}
        )

    return retrieved
