from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    doc_id: str
    question: str
    user_role: str = "Legal Professional"
    mode: str = "qa"

@app.get("/")
def root():
    return {"message": "DocMind AI Backend is running!"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    return {"message": "Upload endpoint works!", "filename": file.filename}

@app.post("/chat")
async def chat(request: ChatRequest):
    return {"answer": "Chat endpoint works!", "question": request.question}
