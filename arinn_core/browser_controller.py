
import logging
import time
from typing import Optional, Any

try:
    from selenium import webdriver # type: ignore
    from selenium.webdriver.common.by import By # type: ignore
    from selenium.webdriver.common.keys import Keys # type: ignore
    from selenium.webdriver.support.ui import WebDriverWait # type: ignore
    from selenium.webdriver.support import expected_conditions as EC # type: ignore
    from selenium.webdriver.chrome.options import Options # type: ignore
    from selenium.webdriver.chrome.service import Service # type: ignore
    from webdriver_manager.chrome import ChromeDriverManager # type: ignore
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    webdriver = Any # type: ignore
    By = Any # type: ignore
    Keys = Any # type: ignore
    WebDriverWait = Any # type: ignore
    EC = Any # type: ignore
    Options = Any # type: ignore
    Service = Any # type: ignore
    ChromeDriverManager = Any # type: ignore

class BrowserController:
    """
    Phase 30: Browser Sovereignty.
    Provides Active Control over the web (Clicking, Typing, Navigating).
    """
    def __init__(self, headless=True):
        self.driver: Any = None
        self.headless = headless
        self._init_driver()
        
    def _init_driver(self):
        if not SELENIUM_AVAILABLE:
            logging.warning("[BROWSER] Selenium not installed. Browser Sovereignty disabled.")
            return

        try:
            options = Options()
            if self.headless:
                options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            # Suppress logging
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            
            # Assuming chromedriver is in path or managed by webdriver-manager
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            print("[BROWSER] Controller Online.")
        except Exception as e:
            logging.error(f"[BROWSER] Failed to init driver: {e}")
            self.driver = None

    def navigate(self, url):
        if not self.driver: return False
        assert self.driver is not None
        try:
            self.driver.get(url) # pyre-ignore
            return True
        except Exception as e:
            logging.error(f"Nav failed: {e}")
            return False
            
    def click(self, selector, by=By.CSS_SELECTOR):
        """Robust click with wait."""
        if not self.driver: return False
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((by, selector))
            )
            element.click()
            return True
        except Exception as e:
            logging.error(f"Click failed ({selector}): {e}")
            return False
            
    def type_text(self, selector, text, by=By.CSS_SELECTOR):
        """Robust type with clear."""
        if not self.driver: return False
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((by, selector))
            )
            element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            logging.error(f"Type failed ({selector}): {e}")
            return False

    def press_key(self, selector, key, by=By.CSS_SELECTOR):
        """Sends a key to an element."""
        if not self.driver: return False
        assert self.driver is not None
        try:
            element = self.driver.find_element(by, selector) # pyre-ignore
            element.send_keys(key)
            return True
        except Exception as e:
            logging.error(f"Press key failed ({selector}): {e}")
            return False
            
    def get_text(self, selector, by=By.CSS_SELECTOR):
        if not self.driver: return ""
        try:
            element = self.driver.find_element(by, selector)
            return element.text
        except Exception:
            return ""

    def get_current_url(self):
        """Returns the current URL of the browser."""
        if not self.driver: return ""
        try:
            return self.driver.current_url
        except Exception:
            return ""
            
    def close(self):
        if self.driver:
            assert self.driver is not None
            self.driver.quit() # pyre-ignore

