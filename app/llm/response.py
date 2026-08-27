from dataclasses import dataclass

@dataclass
class Source:
    title: str
    url: str
    chunk_id: str
    score: float
    
@dataclass
class AnswerResponse:
    answer: str
    source: str
    sources: list[Source]