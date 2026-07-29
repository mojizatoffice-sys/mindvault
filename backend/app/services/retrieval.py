from app.core.llm import get_llm_response, get_embedding
from app.services.ingestion import collection

SYSTEM_PROMPT = """You are MindVault, a precise assistant that answers questions using only the provided context from the user's documents.
Rules:
- Use only the information in the context.
- If the answer is not in the context, clearly say: "I could not find this information in your uploaded documents."
- Be concise and accurate.
- At the end, list the source file(s) you used.
"""

def retrieve_relevant_chunks(query: str, n_results: int = 4)-> list[dict]:
    query_embedding = get_embedding(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    chunks = []
    if results["documents"] and results["documents"][0]:
        for i,doc in enumerate(results["documents"][0]):
            chunks.append({
                "text": doc,
                "source": results["metadatas"][0][i].get("source","unknown"),
                "distance": results["distances"][0][i] if results.get("distances") else None
            })
    return chunks

def chat_with_documents(question:str)-> dict:
    relevant_chunks = retrieve_relevant_chunks(question)
    
    if not relevant_chunks:
        return {
            "answer": "No documents have been uploaded yet, or nothing relevant was found.",
            "sources": []
        }
    context = "\n\n".join([f"[Source: {c['source']}]\n{c['text']}" for c in relevant_chunks])
    prompt = f""" Context from user's documents:
    
    {context}
    
    ---------
    
    Question: {question}
    
    Answer:"""
    
    answer = get_llm_response(prompt=prompt, system=SYSTEM_PROMPT)
    sources = list(set([c["source"] for c in relevant_chunks]))
    
    return {
        "answer": answer,
        "sources": sources,
        "chunk_used": len(relevant_chunks)
    }