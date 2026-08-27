from app.llm.gemini_client import generate_response

def generate_rag_answer(query: str, results: list[dict]) -> str:
    '''
    Generate an answer using retrieved knowledge-base context
    '''
    
    context_parts = []
    
    for result in results:
        context_parts.append(f"""
                             Title: {result['title']}
                             URL: {result['url']}
                             
                             Content:
                             {result['content']}
                             """)
    context = "\n\n".join(context_parts)
        
    prompt = f"""
You are a helpful technical assistant.

Answer the user's question using the provided Kubernetes
documentation context.

Rules:
- Use the provided documentation as the primary source.
- Do not invent Kubernetes-specific facts that are not supported
  by the context.
- Give a clear and concise answer.
- If the context does not contain enough information, say so.

Kubernetes documentation context:

{context}

User question:
{query}
        """
    return generate_response(prompt)

def generate_fallback_answer(query: str) -> str:
    """
    Generate a general answer when retrieval confidence is low.
    Handles Gemini quota/API failures gracefully.
    """

    prompt = f"""
    You are a helpful technical assistant.

    The user's question could not be answered confidently from the
    available Kubernetes documentation knowledge base.

    Answer the question using your general knowledge.

    Be clear and concise.

    User question:

    {query}
    """

    try:
        return generate_response(prompt)

    except Exception as e:
        print()
        print("=" * 60)
        print("GEMINI FALLBACK ERROR")
        print("=" * 60)
        print(e)

        return (
            "I couldn't generate an answer right now because "
            "the external answer service has reached its quota limit. "
            "Please try again later."
        )

def generate_answer(query: str, results: list[dict], confidence: str) -> tuple[str, str]:
    
    if confidence == "high":
        print("Using Kubernetes documentation context.")
        
        answer = generate_rag_answer(query, results)
        
        return answer, "rag"
    
    print("Using Gemini Fallback")
    
    answer = generate_fallback_answer(query)
    
    return answer, "gemini_fallback"
    
            
    