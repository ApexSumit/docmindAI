from utils.loader import load_text
from utils.chunkers import chunk_text
from utils.embedding import get_embedding
from utils.vectordb import collection

text = load_text("docmindAI/data/scholarship_rules.txt")

chunks = chunk_text(text)

for i, chunk in enumerate(chunks):

    embedding = get_embedding(chunk)

    collection.add(
        ids=[str(i)],
        documents=[chunk],
        embeddings=[embedding],
        metadatas=[{"chunk_id": i}]
    )

print(f"Stored {len(chunks)} chunks successfully!")