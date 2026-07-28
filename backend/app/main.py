import os
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.core.config import settings
from app.services.ingestion import ingest_file
from app.services.retrieval import chat_with_documents

Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.CHROMA_PATH).mkdir(parents=True, exist_ok=True)

app = FastAPI(title="MindVault", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatResponse(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message":"MindVault is running.",
            "description":"Fully Offline personal knowledge base."
            }

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    allowed = {".pdf",".txt",".md"}
    ext = Path(file.filename).suffix.lower()
    
    if ext not in allowed:
        raise HTTPException(400, "Only PDF, TXT and MD files are supported.")
    file_path =  os.path.join(settings.UPLOAD_DIR, file.filename)
    
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    
    try:
        result = ingest_file(file_path,file.filename)
        return result
    except Exception as e:
        raise HTTPException(500, f"Ingest Failed: {str(e)}")
    
@app.post("/chat")
def chat(request: ChatResponse):
    if not request.question.strip():
        raise HTTPException(400, "Question cannot be empty")
    result = chat_with_documents(request.question)
    return result