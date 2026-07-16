
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import os

# Import YOUR backend modules
from backend.ingestion import extract_text_with_pages, chunk_by_clauses
from backend.database import get_chroma_collection, index_chunks, retrieve_chunks
from backend.llm_interface import generate_response

app = FastAPI(title="DocMind AI Backend", description="Legal Document RAG API", version="1.0")

# CORS: Allow Next.js frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request/Response Models ---
class ChatRequest(BaseModel):
    doc_id: str
    question: str
    user_role: str = "Legal Professional"
    mode: str = "qa"  # qa, summary, terms, dates

class ChatResponse(BaseModel):
    answer: str
    citations: list

# --- Endpoint 1: Health Check ---
@app.get("/")
def root():
    return {"message": "DocMind AI Backend is running!", "status": "healthy"}

# --- Endpoint 2: Upload PDF ---
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    doc_id = file.filename.replace(".pdf", "").replace(" ", "_")
    
    try:
        # Run ingestion pipeline
        page_texts = extract_text_with_pages(tmp_path)
        if not page_texts:
            raise HTTPException(status_code=400, detail="No text extracted from PDF")
        
        chunks = chunk_by_clauses(page_texts)
        if not chunks:
            raise HTTPException(status_code=400, detail="No clauses found in PDF")
        
        collection = get_chroma_collection()
        chunk_count = index_chunks(doc_id, chunks, collection)
        
        os.unlink(tmp_path)  # Clean up temp file
        
        return {
            "doc_id": doc_id, 
            "message": f"Successfully indexed {chunk_count} clauses",
            "chunk_count": chunk_count
        }
    except Exception as e:
        os.unlink(tmp_path)  # Clean up even on error
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

# --- Endpoint 3: Ask Question / Generate Summary ---
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        collection = get_chroma_collection()
        
        # Retrieve top chunks
        retrieved = retrieve_chunks(
            request.question, 
            request.doc_id, 
            collection, 
            top_k=5
        )
        
        if not retrieved:
            return ChatResponse(
                answer="No relevant clauses found in this document.", 
                citations=[]
            )
        
        # Generate response using your LLM interface
        answer = generate_response(
            request.question, 
            retrieved, 
            mode=request.mode, 
            user_role=request.user_role
        )
        
        # Extract citations for the frontend
        citations = [
            {"page": r["page"], "clause": r["clause"], "text": r["text"][:200]} 
            for r in retrieved[:3]
        ]
        
        return ChatResponse(answer=answer, citations=citations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
