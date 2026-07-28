import ollama
from app.core.config import settings

def get_llm_response(prompt: str, system:str = None) -> str:
    messages = []
    if system:
        messages.append({"role":"system", "content":system})
    messages.append({"role":"user","content":prompt})
    
    response = ollama.chat(
        model = settings.LLM_MODEL,
        messages = messages,
        stream = False
    )
    return response['message']['content']

def get_embedding(text: str)->list[float]:
    response = ollama.embeddings(
        model = settings.EMBED_MODEL,
        prompt = text
    )
    return response['embedding']