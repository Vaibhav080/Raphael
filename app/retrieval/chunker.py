import json
from pathlib import Path

KNOWLEDGE_BASE_DIR = Path("knowledge_base/kubernetes")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def load_document(directory : Path) -> list[dict]:
    """
    Load all JSON documents from the knowledge base.
    """
    
    documents = []
    
    for file_path in directory.glob("*.json"):
        with file_path.open("r", encoding = "utf-8") as file:
            document = json.load(file)
            
        documents.append(document)
        
    return documents

def chunk_text(text : str, chunk_size : int = CHUNK_SIZE, 
               chunk_overlap : int = CHUNK_OVERLAP) -> list[str]:
    """
    Split text into overlapping chunks.
    Example:
    chunk 1: characters 0 - 1000
    chunk 2: characters 800 - 1800
    chunk 3: characters 1600 - 2600
    
    The overlap helps preserve context between chunks.
    """
    
    if not text:
        return []
    
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")
    
    chunks = []
    
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        
        chunk = text[start:end].strip()
        
        if chunk:
            chunks.append(chunk)
        
        start += chunk_size - chunk_overlap
        
    return chunks

def create_chunks(documents : list[dict]) -> list[dict]:
    """
    Convert documents into smaller chunks while preserving metadata
    """
    
    chunks = []
    
    for document in documents:
        title = document.get("title", "Untitiled Document")
        url = document.get("url", "")
        content = document.get("content", "")
        
        document_chunks = chunk_text(content)
        
        for index, chunk in enumerate(document_chunks):
            chunks.append({
                "chunk_id": f"{title}-{index}",
                "title": title,
                "url": url,
                "chunk_index": index,
                "content": chunk,
            })
    return chunks

def save_chunks(chunks: list[dict], output_path: Path) -> None:
    """
    Save chunks as a json file
    """
    
    output_path.parent.mkdir(parents = True, exist_ok = True)
    
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(chunks, file, indent = 2, ensure_ascii = False)
        
def main():
    
    print("Loading documents...")
    
    documents = load_document(KNOWLEDGE_BASE_DIR)
    
    print(f"Documents loaded: {len(documents)}")
    
    print("Creating chunks...")
    
    chunks = create_chunks(documents)
    
    print(f"Chunks created: {len(chunks)}")
    
    output_path = Path("knowledge_base/chunks.json")
    
    save_chunks(chunks, output_path)
    
    print(f"Chunks saved to: {output_path}")
    
if __name__ == "__main__":
    main()
