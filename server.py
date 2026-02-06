from fastmcp import FastMCP
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import asyncio

mcp = FastMCP("Employee RAG Chatbot with FastMCP")

TOP_K = 10
# Read documents
with open("employees.md", "r", encoding="utf-8") as f:
    text = f.read()


# Chunking

def chunk_doc(text, chunk_size = 500, overlap = 100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

chunks = chunk_doc(text)

# Embedding

embedder = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = embedder.encode(chunks).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# MCP tool

@mcp.tool()
def retrieve_doc(query: str, top_k : int= TOP_K) -> list[str]:
    """
    Retrieve relevant employee documents.
    """
    q_embeddings = embedder.encode([query]).astype("float32")
    _, indices = index.search(q_embeddings, top_k)
    return [chunks[i] for i in indices[0]]

if __name__ == "__main__":
    asyncio.run(mcp.run_http_async())