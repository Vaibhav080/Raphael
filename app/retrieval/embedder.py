import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

CHUNKS_FILE = Path("knowledge_base/chunks.json")
EMBEDDINGS_FILE = Path("knowledge_base/embeddings.json")

MODEL_NAME = "all-MiniLM-L6-v2"

def load_chunks() -> list[dict]:
    print("Loading chunks....")
    
    with open(CHUNKS_FILE, "r", encoding = "utf-8") as file:
        chunks = json.load(file)
        
    print(f"Chunks loaded: {len(chunks)}")
    
    return chunks

def create_embeddings(chunks: list[dict]) -> list[dict]:
    print()
    print(f"Loading embedding model: {MODEL_NAME}")
    
    model = SentenceTransformer(MODEL_NAME)
    
    texts = [chunk["content"] for chunk in chunks]
    
    print("Creating embeddings...")
    
    embeddings = model.encode(texts, show_progress_bar = True)
    
    results = []
    
    for chunk, embedding in zip(chunks, embeddings):
        results.append({
            "chunk_id": chunk["chunk_id"],
            "title": chunk["title"],
            "url": chunk["url"],
            "chunk_index": chunk["chunk_index"],
            "content": chunk["content"],
            "embedding": embedding.tolist()
        })
        
    return results

def save_embeddings(data: list[dict]) -> None:
    EMBEDDINGS_FILE.parent.mkdir(parents = True, exist_ok = True)
    
    with open(EMBEDDINGS_FILE, "w", encoding = "utf-8") as file:
        json.dump(data, file)
        
    print()
    print(f"Embeddings saved to: {EMBEDDINGS_FILE}")
    
def main():
    chunks = load_chunks()
    
    print()
    print("Creating embeddings...")
    
    data = create_embeddings(chunks)
    
    save_embeddings(data)
    
    print()
    print("=" * 60)
    print("EMBEDDING COMPLETE")
    print("=" * 60)
    print(f"Chunks embedded: {len(data)}")
    
if __name__ == "__main__":
    main()