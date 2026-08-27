import json
import re
from pathlib import Path

EMBEDDINGS_FILE = Path("knowledge_base/embeddings.json")

TOP_K = 5

STOPWORDS = [
    "a",
    "an",
    "the",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "what",
    "which",
    "who",
    "where",
    "when",
    "why",
    "how",
    "does",
    "do",
    "did",
    "of",
    "to",
    "in",
    "on",
    "for",
    "with",
    "and",
    "or",
    "this",
    "that",
    "these",
    "those",
    "it",
    "its",
    "can",
    "could",
    "should",
    "would",
]

def load_documents() -> list[dict]:
    print("Loading documents....")
    
    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as file:
        documents = json.load(file)
        
    print(f"Documents loaded: {len(documents)}")
    
    return documents

def tokenize(text: str) -> list[str]:
    '''
    Covert text into lowercase words/tokens.
    '''
    
    text = text.lower()
    tokens = re.findall(r"\b[a-zA-Z0-9_-]+\b", text)
    
    tokens = [token for token in tokens
              if token not in STOPWORDS
              ]
    
    return tokens

def keyword_score(query: str, document: dict) -> float:
    '''
    Calculate keyword overlap between the query and a document chunk.
    '''
    
    query_tokens = set(tokenize(query))
    
    if not query_tokens:
        return 0.0
    
    title_tokens = set(tokenize(document["title"]))
    
    content_tokens = set(tokenize(document["content"]))
    
    matches = query_tokens.intersection(title_tokens.union(content_tokens))
    
    return len(matches) / len(query_tokens)

def retrieve_keyword(query: str, 
                     documents: list[dict], top_k: int = TOP_K) -> list[dict]:
    scored_documents =[]
    
    for document in documents:
        score = keyword_score(query, document)
        
        result = document.copy()
        
        result["keyword_score"] = score
        
        scored_documents.append(result)
        
    # Highest score first
    scored_documents.sort(key=lambda document: document["keyword_score"],
                          reverse = True)
    
    return scored_documents[:top_k]

def main():
    documents = load_documents()
    
    query = input("\nEnter your question: ")
    
    results = retrieve_keyword(query, documents)
    
    print()
    print("=" * 60)
    print("KEYWORD RETRIEVAL RESULTS")
    print("=" * 60)
    
    for rank, result in enumerate(results, start = 1):
        print()
        print(f"#{rank}")
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
    
    
    