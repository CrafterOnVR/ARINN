
import unittest
import os
import shutil
import time
from arinn_core.language_corpus import LanguageCorpus
from arinn_core.voice_engine import VoiceEngine, TTS_AVAILABLE

class TestSingularity(unittest.TestCase):
    def setUp(self):
        # Temp DB path with unique ID to avoid collision if previous wasn't deleted
        self.test_db = f"test_arinn_lang_{int(time.time())}.db"
        if os.path.exists(self.test_db):
            try:
                shutil.rmtree(self.test_db)
            except: pass
            
    def tearDown(self):
        # ChromaDB holds file handles, might fail to delete immediately on Windows
        try:
            if os.path.exists(self.test_db):
                shutil.rmtree(self.test_db)
        except PermissionError:
            print("[TEST] Warning: Could not delete temp ChromaDB (File Locked). Ignored.")
        except Exception:
            pass
            
    def test_01_language_corpus(self):
        print("\n[TEST] Verifying Language RAG (ChromaDB)...")
        corpus = LanguageCorpus(db_path=self.test_db)
        
        # Ingest
        text = "The quick brown fox jumps over the lazy dog. Acceleration is key."
        count = corpus.ingest_text(text, source="test_source")
        self.assertGreater(count, 0, "Should ingest text chunks")
        
        # Retrieve
        result = corpus.recall_relevant("acceleration")
        print(f"  > Query 'acceleration' -> '{result}'")
        self.assertTrue(len(result) > 0, "Should retrieve relevant text")
        
        # Result is a list of strings. Check if substring exists in first result.
        found_match = any("Acceleration" in s for s in result) if isinstance(result, list) else "Acceleration" in result
        self.assertTrue(found_match, f"Keywords not found in retrieval: {result}")
        
    def test_02_voice_engine(self):
        print("\n[TEST] Verifying Voice Engine...")
        if not TTS_AVAILABLE:
            print("  > TTS not installed, skipping audio test (PASS).")
            return
            
        voice = VoiceEngine()
        voice.start()
        
        # Queue text
        voice.speak("System diagnostics initiated.")
        time.sleep(2) # Give it time to say it
        
        # Stop
        voice.stop()
        voice.join(timeout=2)
        self.assertFalse(voice.is_alive(), "Voice thread should stop")
        print("  > Voice test complete.")

if __name__ == '__main__':
    unittest.main()
