import re
import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# Common question words

QUESTION_WORDS = {
    "what",
    "why",
    "when",
    "where",
    "who",
    "whom",
    "whose",
    "which",
    "how",
}

QUESTION_AUXILIARIES = {
    "do",
    "does",
    "did",
    "can",
    "could",
    "will",
    "would",
    "shall",
    "should",
    "is",
    "are",
    "am",
    "was",
    "were",
    "have",
    "has",
    "had",
}

QUERY_PHRASES = [
    "tell me",
    "explain",
    "give me information",
    "i want to know",
    "i wanted to know",
    "i would like to know",
    "i'd like to know",
    "i was wondering",
    "i wanted to ask",
    "could you explain",
    "can you explain",
]

def is_query(text: str) -> bool:
    '''
    Determine whether the spoken text is likely to be a customer
    query that should be sent to RAG.
    
    '''
    
    # Basic cleanup
    
    text = text.strip()
    
    if not text:
        return False
    
    normalized_text = text.lower()
    
    # Explicit question mark
    
    if "?" in text:
        return True
    
    # SPOKEN QUESTION PATTERNS
    
    # what is the price
    
    doc = nlp(normalized_text)
    
    if doc:
        first_word = doc[0].text
        
        if first_word in QUESTION_WORDS:
            return True
        
        if first_word in QUESTION_AUXILIARIES:
            return True
        
    # Indirect question phrases
    
    for phrase in QUERY_PHRASES:
        if phrase in normalized_text:
            return True
        
    # Regex for common spoken requests
    
    request_patterns = [
        r"^tell me\b",
        r"^explain\b",
        r"^give me\b.*\b(information|details)\b",
        r"^could you\b.*\b(explain|tell)\b",
        r"^can you\b.*\b(explain|tell)\b",
    ]
    
    for pattern in request_patterns:
        if re.search(pattern, normalized_text):
            return True
        
    # Otherwise, treat it as normal speech
    
    return False
    

def main():
    text_sentences = [
        
        # Direct questions
        
        "What is your premium plan?",
        "Does your product support API access?",
        "How does the pricing work?",
        "Can I cancel my subscription",
        "When does the contract expire",
        "Where can I find the documentation",
        "Who is eligible for the enterprise plan",
        
        # Spoken question without ?
        
        "what is the price of the premium plan",
        "does this include api access",
        "can i upgrade my plan",
        "how much does it cost",
        "do you offer discounts",
        "is there a free trial",
        
        # Indirect questions
        
        "I wanted to know if you offer discounts",
        "I was wondering if the premium plan includes api access",
        "I'd like to know how much the enterprise plan cost",
        "I wanted to ask about your cancellation policy",
        
        # Requests that should probably become SalesAssist queries
        
        "Tell me about the premium plan",
        "Explain the enterprise plan",
        "Give me information about API access",
        "Could you explain the pricing",
        "Tell me how the cancellation policy works",
        
        # Normal Conversation
        
        "The customer wants more information.",
        "Our Premium plan includes API access.",
        "I am interested in the enterprise plan.",
        "The customer is from Mumbai",
        "We discussed the pricing earlier",
        "The meeting is scheduled for tomorrow",
    ]
    
    for sentence in text_sentences:
        result = is_query(sentence)
        
        print(f"Text: {sentence}")
        print(f"Question: {result}")
        print("-" * 60)
        
if __name__ == "__main__":
    main()    
    
    