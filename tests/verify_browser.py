
import unittest
import os
import time
from arinn_core.browser_controller import BrowserController  # type: ignore

class TestBrowser(unittest.TestCase):
    def setUp(self):
        # Create dummy HTML
        self.html_path = os.path.abspath("temp_test.html")
        with open(self.html_path, "w") as f:
            f.write("""
            <html>
                <body>
                    <input id="user-input" type="text">
                    <button id="submit-btn" onclick="document.getElementById('result').innerText='Clicked'">Submit</button>
                    <div id="result">Waiting</div>
                </body>
            </html>
            """)
            
    def tearDown(self):
        if os.path.exists(self.html_path):
            os.remove(self.html_path)
            
    def test_01_interaction(self):
        print("\n[TEST] Verifying Browser Sovereignty...")
        
        # Initialize Controller (Headless)
        browser = BrowserController(headless=True)
        if not browser.driver:
            print("  > SKIP: Driver not initialized (Chrome missing?)")
            return
            
        try:
            # 1. Navigate
            url = f"file:///{self.html_path.replace(os.sep, '/')}"
            print(f"  > Navigating to {url}")
            browser.navigate(url)
            
            # 2. Type
            print("  > Typing 'Phase30'...")
            success = browser.type_text("#user-input", "Phase30")
            self.assertTrue(success, "Failed to type")
            
            # Verify Value
            val = browser.driver.find_element("id", "user-input").get_attribute("value")
            self.assertEqual(val, "Phase30")
            
            # 3. Click
            print("  > Clicking Submit...")
            success = browser.click("#submit-btn")
            self.assertTrue(success, "Failed to click")
            
            # 4. Verify Result
            res = browser.get_text("#result")
            self.assertEqual(res, "Clicked")
            print("  > Interaction Verified: Form filled & Button clicked.")
            
        finally:
            browser.close()

if __name__ == '__main__':
    unittest.main()
