from typing import Dict, List
import time
import random

try:
    from ddgs import DDGS  # type: ignore
except ImportError:
    try:
        from duckduckgo_search import DDGS # type: ignore
    except ImportError:
        DDGS = None

class Searcher:
    def __init__(self, max_results: int = 10):
        self.max_results = max_results

    def search(self, query: str) -> List[Dict]:
        if DDGS is None:
            return []
        results = []
        try:
            # Physical Anti-Ban Throttle (Randomized wait to prevent DDGS from recognizing automated scraping)
            time.sleep(random.uniform(2.0, 5.0))
            
            with DDGS(timeout=20) as ddgs:
                # Eagerly evaluate the generator to trap rate limits *inside* this try/except block
                for r in ddgs.text(query, max_results=self.max_results, region="wt-wt", safesearch="Moderate"):
                    results.append(r)
        except Exception as e:
            # Catch RateLimitException and connection aborts natively so they don't break the agent loop
            print(f"[SEARCHER] DDGS Throttle Enforced on query '{query}'. (Exception handled natively)")
            
        return results

