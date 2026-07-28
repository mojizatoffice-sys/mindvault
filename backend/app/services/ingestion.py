import os
import uuid
from pathlib import Path
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings as AppSettings
from app.core.llm import get_embedding

chroma_client = chromadb.PersistentClient(
    path = AppSettings.CHROMA_PATH,
    settings= ChromaSettings(anonymized_telemetry=False)
)

collection = chroma_client.get_or_create_collection(
    name = "mindvault_docs",
    metadata={"hnsw:space":"cosine"}
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 800,
    chunk_overlap = 150,
    length_function = len
)

def extract_text_from_pdf(file_path:str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text+"\n"
    return text

def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
    
def ingest_file(file_path: str, original_filename: str) -> dict:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif suffix in [".txt", ".md"]:
        raw_text = extract_text_from_txt(file_path)
    else:
        raise ValueError("Only PDF, TXT, and MD files are supported right now")

    if not raw_text.strip():
        raise ValueError("No text could be extracted from the file")
    
    chunks = text_splitter.split_text(raw_text)
    
    ids = []
    embeddings = []
    documents = []
    metadata = []
    
    for i, chunk in enumerate(chunks):
        chunk_id = f"{uuid.uuid4()}_{i}"
        embedding = get_embedding(chunk)
        
        ids.append(chunk_id)
        embeddings.append(embedding)
        documents.append(chunk)
        metadata.append({
            "source": original_filename,
            "chunk_index": i
        })
        
    collection.add(
        ids = ids,
        embeddings = embeddings,
        documents = documents,
        metadata = metadata 
    )
    
    return {
        "filename": original_filename,
        "chunks_created": len(chunks),
        "status": "success"
    }