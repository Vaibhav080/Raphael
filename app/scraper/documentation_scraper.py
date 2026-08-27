import heapq
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse

from app.scraper.document_extractor import extract_document, save_document

START_URL = "https://kubernetes.io/docs/home/"

ALLOWED_DOMAIN = "kubernetes.io"
ALLOWED_PATH_PREFIX = "/docs/"

MAX_PAGES = 20

USER_AGENT = "SalesAssistAI-DocumentationResearch/1.0"

def fetch_page(url : str) -> str:
    response = requests.get(url, timeout = 20, headers={"User-Agent": "SalesAssistAI-DocumentationResearch/1.0"})
    
    response.raise_for_status()
    
    return response.text

def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    
    # Remove fragment
    path = parsed.path
    
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", "",""))

def is_allowed_url(url : str) -> bool:
    parsed = urlparse(url)
    
    if parsed.scheme not in {"http", "https"}:
        return False
    
    if parsed.netloc != ALLOWED_DOMAIN:
        return False
    
    if not parsed.path.startswith(ALLOWED_PATH_PREFIX):
        return False
    
    if "/_print" in parsed.path:
        return False
    
    if parsed.path in {"/docs/home", "/docs/home/"}:
        return False
    
    return True

def score_url(url: str) -> int:
    """
    
    Give doc pages a relevance score.
    Higher score = crawl earlier
    
    """
    
    path = urlparse(url).path.lower()
    
    score = 0
    
    # Core Kubernetes concepts
    if "/docs/concepts/" in path:
        score += 50
        
    # Practical tasks
    if "/docs/tasks/" in path:
        score += 40
    
    # Tutorials
    if "/docs/tutorials/" in path:
        score += 30
        
    # Important workload docs
    important_topics = {
        "/pods/": 40,
        "/deployments/": 40,
        "/replicaset": 40,
        "/statefulset": 40,
        "/daemonset": 40,
        "/jobs/": 35,
        "/services/": 35,
        "/networking/": 35,
        "/storage/": 35,
        "/configuration/": 35,
        "/security/": 30,
        "/scheduling/": 30
    }
    
    for topic, bonus in important_topics.items():
        if topic in path:
            score += bonus
            
    if "/docs/reference/" in path:
        score -= 30
        
    if "/docs/reference/kubernetes-api/" in path:
        score -= 50
        
    if "/docs/contribute/" in path:
        score -= 100
    
    return score

def extract_links(html: str, current_url: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    
    links = set()
    
    for anchor in soup.find_all("a", href = True):
        href = anchor["href"]
        
        absolute_url = urljoin(current_url, href)
        
        # Normalize before adding to links
        absolute_url = normalize_url(absolute_url)
        
        if is_allowed_url(absolute_url):
            links.add(absolute_url)
            
    return links

def crawl():
    visited = set()
    discovered = set()
    
    # Priority queue
    # heapq is a min heap so we can use negative score
    
    queue = []
    
    start_url = normalize_url(START_URL)
    
    # Fetch the home page only to discover doc link
    print(f"Crawling start page: {start_url}")
    
    try:
        html = fetch_page(start_url)
        
    except requests.RequestException as error:
        print(f"Download error: {error}")
        return
    
    # Discover links from home, but do not count/save them
    links = extract_links(html, start_url)
    
    for link in links:
        if link in discovered:
            continue
        
        discovered.add(link)
        
        link_score = score_url(link)
        
        heapq.heappush(queue, (-link_score, link))
        
    print(f"Initial documentation links discovered: {len(discovered)}")
    
    while queue and len(visited) < MAX_PAGES:
        negative_score, url = heapq.heappop(queue)
        
        if url in visited:
            continue
        
        score = -negative_score
        
        print(f"Crawling: {url}")
        print(f"    Priority score: {score}")
        
        try:
            html = fetch_page(url)
            
        except requests.RequestException as error:
            print(f"    Download error: {error}")
            continue
        
        visited.add(url)
        
        # Extract and save document
        try:
            document = extract_document(html)
            document["url"] = url
            
            save_document(document)
            
            print(f"    Title: {document['title']}")
            print("  Saved: yes")
            
        except Exception as error:
            print(f"    Extraction error: {error}")
            
        # Discover new URLs
        links = extract_links(html, url)
        
        new_links = 0
        
        for link in links:
            if link in discovered:
                continue
            
            discovered.add(link)
            
            link_score = score_url(link)
            
            heapq.heappush(queue, (-link_score, link))
            
            new_links += 1
                
        print(f"    New links: {new_links}")
        print(f"    Visited: {len(visited)}")
        print(f"    Queue: {len(queue)}")
        
    print()
    print("=" * 60)
    print("CRAWL COMPLETE")
    print("=" * 60)
    print(f"Pages visited: {len(visited)}")
    print(f"Pages discovered: {len(discovered)}")

    print()
    print("URLs crawled:")

    for url in sorted(visited):
        print(url)
    
if __name__ == "__main__":
    crawl()