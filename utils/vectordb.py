import chromadb

client = chromadb.PersistentClient(path="docmindAI/chromaDB")

collection = client.get_or_create_collection(
    name="scholarship_rules"
)