import os
from backend.ingestion import extract_text_with_pages, chunk_by_clauses
from backend.database import get_chroma_collection, index_chunks, retrieve_chunks


def test_imports():
    print("Imports OK")


def test_data_flow(pdf_path):
    print(f"Testing with PDF: {pdf_path}")
    pages = extract_text_with_pages(pdf_path)
    print(f"Extracted {len(pages)} pages")

    chunks = chunk_by_clauses(pages)
    print(f"Created {len(chunks)} chunks")

    collection = get_chroma_collection()
    doc_id = "test_doc"
    num_indexed = index_chunks(doc_id, chunks, collection)
    print(f"Indexed {num_indexed} chunks")

    results = retrieve_chunks("What is the termination date?", doc_id, collection, top_k=3)
    print(f"Retrieved {len(results)} results")
    for r in results:
        print(r)


if __name__ == "__main__":
    test_imports()
    sample_pdf = input("Enter a path to a test PDF (or press Enter to skip): ").strip()
    if sample_pdf and os.path.exists(sample_pdf):
        test_data_flow(sample_pdf)
    else:
        print("No PDF provided, import flow only.")
