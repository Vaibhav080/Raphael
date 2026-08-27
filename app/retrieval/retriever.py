import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

EMBEDDINGS_FILE = Path("knowledge_base/embeddings.json")

MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 5

def load_embeddings() -> list[dict]:
    print("Loading embeddings...")
    
    with open(EMBEDDINGS_FILE, "r", encoding = "utf-8") as file:
        data = json.load(file)
        
    print(f"Embeddings loaded: {len(data)}")
    
    return data

def cosine_similarity(query_vector, document_vectors):
    
    query_vector = np.array(query_vector)
    query_norm = np.linalg.norm(query_vector)
    
    document_norms = np.linalg.norm(document_vectors, axis = 1)
    
    similarities = np.dot(document_vectors, query_vector) / (document_norms * query_norm)
    
    return similarities

def retrieve(query: str, documents: list[dict], model: SentenceTransformer,
             top_k: int = TOP_K) -> list[dict]:
    print()
    print(f"Query: {query}")
    
    # Convert the user's question into an embedding
    query_embedding = model.encode(query)
    
    # Extract document embeddings
    document_embeddings = [document["embedding"] for document in documents]

    
    print("Query embedding shape:", np.array(query_embedding).shape)
    print("Document embeddings shape:", np.array(document_embeddings).shape)
        
    # Calculate similarity
    similarities = cosine_similarity(query_embedding, document_embeddings)
    
    # Get indices of the highest scoring chunks
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    
    for index in top_indices:
        document = documents[index].copy()
        
        document["similarity"] = float(similarities[index])
        
        results.append(document)
        
    return results

def main():
    documents = load_embeddings()
    
    print()
    print(f"Loading embedding model: {MODEL_NAME}")
    
    model = SentenceTransformer(MODEL_NAME)
    
    query = input("\nEnter your question: ")
    
    results = retrieve(query, documents, model)
    
    print()
    print("=" * 60)
    print("RETRIEVAL RESULTS")
    print("=" * 60)
    
    for rank, result in enumerate(results, start = 1):
        
        print()
        print(f"#{rank}")
        print(f"Similarity: {result['similarity']:.4f}")
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Chunk: {result['chunk_id']}")
        
        print()
        print(result["content"][:500])
        
        print("-" * 60)
        
if __name__ == "__main__":
    main()