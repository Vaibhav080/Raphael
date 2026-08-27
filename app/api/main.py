from fastapi import FastAPI, HTTPException
import traceback
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware

from app.retrieval.retriever import load_embeddings
from app.llm.rag_pipeline import run_pipeline

MODEL_NAME = "all-MiniLM-L6-v2"

app = FastAPI(title = "Voice-Enabled Kubernetes Assistant", description = 
              "A Kubernetes RAG assistant with voice interaction support.", version = "1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173",], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

class AskRequest(BaseModel):
    query: str
    
class AskResponse(BaseModel):
    answer: str
    source: str
    sources: list
    
print("Loading documents...")
documents = load_embeddings()

print(f"Documents loaded: {len(documents)}")

print(f"Loading embedding model: {MODEL_NAME}")

model = SentenceTransformer(MODEL_NAME)

print("Backend ready!")

@app.get("/")
def root():
    return {
        "message": "Voice-Enabled Kubernetes Assistant API",
        "status": "running"
    }
    
@app.post("/ask", response_model=AskResponse)

def ask(request: AskRequest):

    try:
        print()
        print("=" * 60)
        print("API REQUEST")
        print("=" * 60)
        print(f"Query: {request.query}")

        response = run_pipeline(
            request.query,
            documents,
            model
        )

        print("✅ Pipeline completed successfully")

        return response

    except Exception as e:
        print()
        print("=" * 60)
        print("❌ API ERROR")
        print("=" * 60)

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )