import requests
import json
from pathlib import Path
from bs4 import BeautifulSoup

KNOWLEDGE_BASE_DIR = Path("knowledge_base/kubernetes")

def save_document(document: dict):
    KNOWLEDGE_BASE_DIR.mkdir(parents = True, exist_ok = True)
    
    title = document["title"]
    
    filename = (
        title.lower().replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "")
    )
    
    output_path = KNOWLEDGE_BASE_DIR / f"{filename}.json"
    
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            document,
            file,
            ensure_ascii=False,
            indent=2
        )
    print(f"    Saved: {output_path}")

USER_AGENT = "SalesAssistAI-DocumentationResearch/1.0"

def fetch_page(url: str) -> str:
    response = requests.get(url, timeout = 20, headers = {"User-Agent": USER_AGENT})
    
    response.raise_for_status()
    
    return response.text

def extract_document(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove elements that are not useful knowledge
    for element in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header"
    ]):
        element.decompose()
        
    # Kubernetes documentation content
    main = soup.find("main")
    
    if main is None:
        raise ValueError("Could not find main documentation content.")
    
    # Extract title
    title_element = main.find("h1")
    
    if title_element:
        title = title_element.get_text("    ", strip=True)
    else:
        title = "Untitled Document"
        
    # Extract text
    text = main.get_text("\n", strip = True)
    
    return {"title": title,
            "content": text}
    
def extract_from_url(url: str) -> dict:
    html = fetch_page(url)
        
    document = extract_document(html)
        
    document["url"] = url
        
    return document
    
if __name__ == "__main__":
    
    test_url = (
        "https://kubernetes.io/docs/"
        "concepts/workloads/controllers/replicaset/"
    )
    
    print("Downloading documentation page...")
    
    document = extract_from_url(test_url)
    
    print()
    print("=" * 60)
    print("TITLE")
    print("=" * 60)
    print(document["title"])
    
    print()
    print("=" * 60)
    print("URL")
    print("=" * 60)
    print(document["url"])
    
    print()
    print("=" * 60)
    print("CONTENT")
    print("=" * 60)
    print(document["content"])
    