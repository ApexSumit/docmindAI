from utils.embedding import get_embedding
from utils.vectordb import collection

query = "What documents are required for scholarship?"

# Convert question to embedding
query_embedding = get_embedding(query)

# Search ChromaDB
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

print("\nRetrieved Chunks:\n")

for i, doc in enumerate(results["documents"][0], start=1):
    print(f"\n------ Chunk {i} ------\n")
    print(doc)