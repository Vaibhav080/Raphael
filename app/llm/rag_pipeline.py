from app.retrieval.hybrid_retriever import hybrid_retrieve
from app.retrieval.retriever import load_embeddings

from app.llm.answer_generator import generate_answer

from app.llm.response import AnswerResponse, Source

from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

def get_retrieval_confidence(results: list[dict]) -> str:
    """
    Determine whether the retrieved Kubernetes context is relevant enough to use for RAG
    """

    if not results:
        return "low"
    
    top_result = results[0]
    
    vector_score = top_result["vector_score"]
    keyword_score = top_result["keyword_score"]
    hybrid_score = top_result["hybrid_score"]
    
    # Strong semantic/domain match
    if vector_score >= 0.6 and hybrid_score >= 0.8:
        return "high"
    
    # Strong keyword/domain match
    if keyword_score >= 0.5 and hybrid_score >= 0.8:
        return "high"

    return "low"

def run_pipeline(query: str, documents: list[dict], model: SentenceTransformer):
    '''
    Run the complete RAG pipeline.
    
    1. Retrieve relevant chunks using hybrid retrieval.
    2. Check retrieval confidence.
    3. Generate an answer using either:
       - Kubernetes documentation context
       - Gemini fallback
    
    '''
    
    print()
    print("=" * 60)
    print("RAG PIPELINE")
    print("=" * 60)
    
    print()
    print(f"Question: {query}")
    
    # Step 1: hybrid retrieval
    print()
    print("Running hybrid retrieval...")
    
    results = hybrid_retrieve(query, documents, model)
    
    print()
    
    print("Retrieval Scores: ")
    
    for rank, result in enumerate(results, start = 1):
        print(f"#{rank}"
              f"Vector: {result['vector_score']:.4f} | "
              f"Keyword: {result['keyword_score']:.4f} | "
              f"Hybrid: {result['hybrid_score']:.4f}")
    
    print(f"Retrieved chunks: {len(results)}")
    
    confidence = get_retrieval_confidence(results)
    
    if results:
        print(f"Top retrieval score: {results[0]['hybrid_score']:.4f}")
    
    print(f"Retrieval confidence: {confidence.upper()}")
    
    answer, source = generate_answer(query, results, confidence)

    sources = []
    
    if source == "rag":
        
        for result in results:
            sources.append(
                Source(
                    title = result["title"],
                    url = result["url"],
                    chunk_id = result["chunk_id"],
                    score = float(result["hybrid_score"])
                )
            )
            
        
        print()
        print("=" * 60)
        print("SOURCES")
        print("=" * 60)
        
        for rank, result in enumerate(results, start = 1):
            print()
            print(f"#{rank}")
            print(f"Title: {result['title']}")
            print(f"URL: {result['url']}")
            print(f"Chunk: {result['chunk_id']}")
            print(f"Hybrid score: "
                  f"{result['hybrid_score']:.4f}")
            
        
    response = AnswerResponse(answer = answer,
                              source = source,
                              sources = sources)
    
    print()
    
    print("=" * 60)
    print("ANSWER")
    print("=" * 60)
    
    print(answer)
    
    print()
    print("=" * 60)
    print("ANSWER SOURCE")
    print("=" * 60)
    
    print(source)
    
    return response

def main():
    
    # Load embeddings
    print("Loading documents...")
    
    documents = load_embeddings()
    
    print(f"Documents loaded: {len(documents)}")
    
    # Load embedding model
    print()
    print(f"Loading embedding model: {MODEL_NAME}")
    
    model = SentenceTransformer(MODEL_NAME)
    
    # Get User Query
    
    query = input("\nEnter your question: ")
    
    response = run_pipeline(query, documents, model)
    
    print()
    print("Response Object: ")
    print(response)
    
if __name__ == "__main__":
    main()
    