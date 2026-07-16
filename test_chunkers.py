from utils.loader import load_text
from utils.chunkers import chunk_text

# Load the text
text = load_text("docmindAI/data/scholarship_rules.txt")

# Create chunks
chunks = chunk_text(text)

print("Total Chunks:", len(chunks))

print("\nFirst Chunk:\n")
print(chunks[0])

print("\nSecond Chunk:\n")
print(chunks[1]) 