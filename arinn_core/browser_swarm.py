
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from .browser_controller import BrowserController

class BrowserSwarm:
    """
    Phase 31: The Shadow Swarm.
    Manages multiple parallel browser instances to devour information quickly.
    """
    def __init__(self, pool_size=3):
        self.pool_size = pool_size
        self.browsers = [] # We'll spawn these on demand or pool them
        
    def _worker_task(self, url):
        """
        Individual worker method. 
        Spawns a FRESH browser for isolation, or could reuse from a pool.
        For stability, we spawn fresh here to ensure clean state.
        """
        # Note: Spawning a browser is heavy. In a real heavy-duty app we'd keep them alive.
        # For this demo, we'll spawn fresh to avoid state leakage.
        try:
            browser = BrowserController(headless=True)
            if not browser.driver:
                return f"Failed to start browser for {url}"
                
            print(f"[SWARM] Agent visiting: {url}")
            browser.navigate(url)
            
            # Extract title as proof of visit
            title = browser.driver.title
            browser.close()
            return f"Visited: {title}"
        except Exception as e:
            return f"Error visiting {url}: {e}"

    def swarm_urls(self, urls):
        """
        Scatters the URLs across the browser pool.
        """
        results = []
        print(f"[SWARM] Unleashing {self.pool_size} agents on {len(urls)} targets...")
        
        with ThreadPoolExecutor(max_workers=self.pool_size) as executor:
            future_to_url = {executor.submit(self._worker_task, url): url for url in urls}
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                    results.append(data)
                except Exception as exc:
                    results.append(f"{url} generated an exception: {exc}")
                    
        return results
