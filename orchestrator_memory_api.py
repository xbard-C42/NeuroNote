# memory/vector_store.py
from typing import List
import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(persist_directory="./data/chroma"))
collection = client.get_or_create_collection("neuronote_memory")

def store_note(user_id: str, text: str, metadata: dict):
    collection.add(documents=[text], metadatas=[metadata], ids=[user_id + "::" + str(hash(text))])

def search_notes(query: str, n_results: int = 5) -> List[dict]:
    results = collection.query(query_texts=[query], n_results=n_results)
    return [
        {"text": doc, "score": score, "metadata": meta}
        for doc, score, meta in zip(results["documents"][0], results["distances"][0], results["metadatas"][0])
    ]
