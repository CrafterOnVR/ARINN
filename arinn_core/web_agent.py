
import time
import logging
from .browser_controller import BrowserController  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore

class WebNavigator:
    """
    Phase 30: The Navigator.
    Logic layer that translates intents into browser actions.
    """
    def __init__(self, headless=True):
        self.controller = BrowserController(headless=headless)

    def search_web(self, query, engine="duckduckgo"):
        """
        Navigates to a search engine and executes a search.
        """
        print(f"[NAVIGATOR] Searching {engine} for: '{query}'")
        
        if engine == "duckduckgo":
            url = "https://duckduckgo.com"
            input_selector = "input[name='q']" # Standard DDG
        elif engine == "google":
            url = "https://www.google.com"
            input_selector = "textarea[name='q']" # Modern Google uses textarea often
        else:
            return False

        # 1. Navigate
        if not self.controller.navigate(url):
            return False
        
        # 2. Type Query
        if not self.controller.type_text(input_selector, query):
            print("[NAVIGATOR] Failed to find search box.")
            return False
            
        # 3. Submit (Press Enter)
        if not self.controller.press_key(input_selector, Keys.RETURN):
            return False
            
        time.sleep(2) # Wait for results
        return True

    def extract_search_results(self):
        """
        Heuristic extractor for search results (Titles/Links).
        """
        results = []
        # Try generic selectors for DDG/Google
        # DDG specific: .result__title a
        # Google specific: h3
        
        # DDG
        if "duckduckgo" in self.controller.get_current_url():
            # DDG classes change, but often 'article h2 a' or similar works?
            # Let's try to get all links that look like results
            # This is fragile, but "Sovereign" implies trying
            pass
            
        return self.controller.get_current_url()

    def close(self):
        self.controller.close()
