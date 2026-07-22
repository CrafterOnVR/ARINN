import json
import os
import urllib.parse
from typing import List, Dict, Any

class TrustManager:
    """
    Manages the 'Circle of Trust' for ARINN.
    Ensures that information is only gathered from verifiable, high-quality sources
    to prevent 'AI Slop' contamination.
    """
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            # Default to adjacent json file
            config_path = os.path.join(os.path.dirname(__file__), 'trusted_sources.json')
            
        self.config_path = config_path
        self.domains = set()
        self.tlds = set()
        self.blocked_keywords = set()
        self._load_config()

    def _load_config(self):
        """Loads trusted sources from JSON."""
        if not os.path.exists(self.config_path):
            # Fallback defaults if file missing
            self.domains = {"wikipedia.org", "arxiv.org", "github.com"}
            self.tlds = {".edu", ".gov"}
            return

        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                self.domains = set(data.get("domains", []))
                self.tlds = set(data.get("tlds", []))
                self.blocked_keywords = set(data.get("blocked_keywords", []))
        except Exception as e:
            print(f"Error loading trusted sources: {e}")

    def is_trusted(self, url: str) -> bool:
        """
        Determines if a URL is from a trusted source.
        """
        try:
            parsed = urllib.parse.urlparse(url)
            domain = parsed.netloc.lower()
            
            # 1. Check Exact Domain or Subdomain
            # e.g. "en.wikipedia.org" ends with "wikipedia.org"
            if any(domain == d or domain.endswith("." + d) for d in self.domains):
                return True
                
            # 2. Check TLD
            # e.g. "mit.edu" ends with ".edu"
            if any(domain.endswith(tld) for tld in self.tlds):
                return True
                
            return False
        except:
            return False

    def is_content_safe(self, text: str) -> bool:
        """
        secondary check: scans content for "slop" keywords.
        """
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in self.blocked_keywords):
            # Simple keyword matching is crude, but a good first line of defense.
            return False
        return True

    def filter_search_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filters search results to keep only trusted ones.
        Expects a list of dicts with a 'href' or 'link' key.
        """
        trusted_results = []
        for r in results:
            url = r.get('href') or r.get('link')
            if url and self.is_trusted(url):
                trusted_results.append(r)
        return trusted_results
