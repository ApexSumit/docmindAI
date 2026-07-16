from utils.loader import load_text
from utils.chunkers import chunk_text
from utils.embedding import get_embedding

# Load document
text = load_text("docmindAI/data/scholarship_rules.txt")

# Split into chunks
chunks = chunk_text(text)

print(f"Total Chunks: {len(chunks)}")

# Generate embedding for first chunk
embedding = get_embedding(chunks[0])

print("\nEmbedding Type:", type(embedding))
print("Embedding Length:", len(embedding))

print("\nFirst 10 Values:")
print(embedding[:10])