
import threading
import queue
import time
import logging

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("[VOICE] pyttsx3 not found. Voice will be disabled. (pip install pyttsx3)")

class VoiceEngine(threading.Thread):
    """
    Real-Time Text-to-Speech Engine.
    Runs in a background thread to prevent blocking the main cognitive loop.
    """
    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()
        self.running = False
        self.daemon = True
        self.engine = None
        
    def run(self):
        if not TTS_AVAILABLE:
            return

        # Initialize engine in the thread it runs in (important for COM interop on Windows)
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 170)  # Speed
            self.engine.setProperty('volume', 1.0) 
        except Exception as e:
            logging.error(f"Failed to init TTS: {e}")
            return

        self.running = True
        while self.running:
            try:
                text = self.queue.get(timeout=1.0)
                if text == "STOP_VOICE":
                    break
                
                print(f"[VOICE] Speaking: \"{text}\"")
                self.engine.say(text)
                self.engine.runAndWait()
                self.queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Voice Error: {e}")
                
    def speak(self, text):
        if TTS_AVAILABLE:
            self.queue.put(text)
        else:
            print(f"[SILENT VOICE] {text}")

    def stop(self):
        self.running = False
        self.queue.put("STOP_VOICE")
