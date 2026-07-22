
import logging
import time
import numpy as np
from PIL import ImageGrab

# Optional JIT
try:
    from numba import jit
    JIT_AVAILABLE = True
except ImportError:
    JIT_AVAILABLE = False
    # Mock jit decorator if missing
    def jit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

@jit(nopython=True)
def calculate_entropy(arr):
    # Flatten
    flat = arr.flatten()
    # Histogram
    hist = np.zeros(256, dtype=np.float64)
    for i in range(len(flat)):
        hist[flat[i]] += 1
    
    # Normalize
    hist = hist / len(flat)
    
    entropy = 0.0
    for i in range(256):
        p = hist[i]
        if p > 0:
            entropy -= p * np.log2(p)
    return entropy

class VisionSystem:
    """
    Computer Vision Interface for ARINN.
    Captures and analyzes screen data to provide visual context.
    Uses JIT acceleration if available.
    """
    def __init__(self):
        self.last_capture_time = 0
        self.last_metrics = None
        
    def capture(self):
        """
        Takes a screenshot of the primary monitor.
        Returns PIL Image.
        """
        try:
            return ImageGrab.grab()
        except Exception as e:
            logging.error(f"Screen capture failed: {e}")
            return None
            
    def analyze(self, image=None):
        """
        Computes metrics on the image:
        - Brightness (0-255)
        - Entropy (Complexity)
        - Dynamic Range
        """
        if image is None:
            image = self.capture()
            
        if image is None:
            return {"status": "BLIND"}
            
        # Convert to numpy array for fast processing
        # Resize small for speed logic
        thumb = image.resize((320, 240))
        arr = np.array(thumb.convert('L')) # Grayscale
        
        # 1. Brightness
        brightness = np.mean(arr)
        
        # 2. Dynamic Range / Contrast
        contrast = np.std(arr)
        
        # 3. Entropy (Accelerated)
        entropy = calculate_entropy(arr)
        
        metrics = {
            "brightness": float(brightness),
            "contrast": float(contrast),
            "entropy": float(entropy),
            "resolution": image.size,
            "timestamp": time.time(),
            "accelerated": JIT_AVAILABLE
        }
        
        self.last_metrics = metrics
        return metrics
        
    def describe_scene(self):
        """
        Returns a verbal description based on metrics.
        """
        m = self.analyze()
        if not m or m.get("status") == "BLIND":
            return "Visual Input Offline."
            
        b = m['brightness']
        e = m['entropy']
        jit_status = " (JIT)" if m.get("accelerated") else ""
        
        desc = []
        if b < 50: desc.append("Dark")
        elif b > 200: desc.append("Bright")
        else: desc.append("Moderate Light")
        
        if e < 4.0: desc.append("Low Complexity")
        elif e > 7.0: desc.append("High Complexity")
        else: desc.append("Structured Visuals")
        
        return f"Visible Scene{jit_status}: {', '.join(desc)}. (Entropy: {e:.2f})"
