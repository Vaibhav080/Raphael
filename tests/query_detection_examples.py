# Test examples for SalesAssist AI query detection.
#
# expected=True  -> SalesAssist should treat the text as a query
# expected=False -> SalesAssist should ignore the text


TEST_CASES = [

    # Direct questions

    ("What is your premium plan?", True),
    ("Does your product support API access?", True),
    ("How does the pricing work?", True),
    ("Can I cancel my subscription", True),
    ("When does the contract expire", True),
    ("Where can I find the documentation", True),
    ("Who is eligible for the enterprise plan", True),

    # Spoken questions without punctuation

    ("what is the price of the premium plan", True),
    ("does this include api access", True),
    ("can i upgrade my plan", True),
    ("how much does it cost", True),
    ("do you offer discounts", True),
    ("is there a free trial", True),

    # Indirect questions

    ("I wanted to know if you offer discounts", True),
    ("I was wondering if the premium plan includes api access", True),
    ("I'd like to know how much the enterprise plan costs", True),
    ("I wanted to ask about your cancellation policy", True),

    # Information requests
    # These aren't grammatical questions,
    # but SalesAssist should answer them.

    ("Tell me about the premium plan", True),
    ("Explain the enterprise plan", True),
    ("Give me information about API access", True),
    ("Could you explain the pricing", True),
    ("Tell me how the cancellation policy works", True),

    # Normal conversation
    # These should NOT trigger RAG.

    ("The customer wants more information", False),
    ("Our premium plan includes API access", False),
    ("I am interested in the enterprise plan", False),
    ("The customer is from Mumbai", False),
    ("We discussed the pricing earlier", False),
    ("The meeting is scheduled for tomorrow", False),
]