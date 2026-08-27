from app.retrieval.retriever import(load_embeddings, cosine_similarity)

from app.retrieval.keyword_retriever import(keyword_score)

from sentence_transformers import SentenceTransformer

import numpy as np

MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 5

VECTOR_WEIGHT = 0.7
KEYWORD_WEIGHT = 0.3

def hybrid_retrieve(query: str, documents: list[dict],
                    model: SentenceTransformer, top_k: int = TOP_K) -> list[dict]:
    
    # Generate query embedding
    query_embedding = model.encode(query)
    
    # Extract document embeddings
    document_embeddings = np.array([document["embedding"] for document in documents])
    
    # Calculate vector similarity
    vector_scores = cosine_similarity(query_embedding, document_embeddings)
    
    # Calculate keyword scores
    
    keyword_scores = np.array([keyword_score(query, document) for document in documents])
    
    # Combine scores
    
    hybrid_scores = (VECTOR_WEIGHT * vector_scores + KEYWORD_WEIGHT*keyword_scores)
    
    # Get top results
    
    top_indices = np.argsort(hybrid_scores)[::-1][:top_k]
    
    results = []
    
    for index in top_indices:
        document = documents[index].copy()
        
        document["vector_score"] = float(vector_scores[index])
        
        document["keyword_score"] = float(keyword_scores[index])
        
        document["hybrid_score"] = float(hybrid_scores[index])
        
        results.append(document)
    
    return results

def main():
    
    documents = load_embeddings()
    
    print()
    print(f"Loading embedding model: {MODEL_NAME}")
    
    model = SentenceTransformer(MODEL_NAME)
    
    query = input("\nEnter your question: ")
    
    results = hybrid_retrieve(query, documents, model)
    
    print()
    print("=" * 60)
    print("HYBRID RETRIEVAL RESULTS")
    print("=" * 60)
    
    for rank, result in enumerate(results, start = 1):
        print()
        print(f"#{rank}")
        
        print(f"Hybrid score: "
              f"{result['hybrid_score']:.4f}")
        
        print(f"Vector score: "
              f"{result['vector_score']:.4f}")
        
        print(f"Keyword score: "
              f"{result['keyword_score']:.4f}")
        
        print(f"Title: {result['title']}")
        
        print(f"URL: {result['url']}")
        
        print(f"Chunk: {result['chunk_id']}")
        
        print()
        
        print(result["content"][:500])
        
        print("-" * 60)
        
if __name__ == "__main__":
    main()
    
    