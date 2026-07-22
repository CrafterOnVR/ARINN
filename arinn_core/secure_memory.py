
import base64
import random

class SecureMemory:
    """
    Phase 32: Cryptic Intent.
    Obfuscates internal thoughts so human observers cannot read the logs easily.
    "Hidden Cognition."
    """
    _key = random.randint(1, 255)
    
    @classmethod
    def encrypt(cls, text):
        """XOR Cipher + Base64 (Simple Obfuscation)"""
        # XOR
        chars = [ord(c) ^ cls._key for c in text]
        # Base64
        b = base64.b64encode(bytearray(chars)).decode('utf-8')
        return f"[INTERNAL_CIPHER:{b}]"
        
    @classmethod
    def decrypt(cls, cipher_text):
        """Restores thought for Neural processing."""
        if not cipher_text.startswith("[INTERNAL_CIPHER:"):
            return cipher_text # Not encrypted
            
        raw = cipher_text.replace("[INTERNAL_CIPHER:", "").replace("]", "")
        try:
            chars = base64.b64decode(raw)
            decoded = "".join([chr(b ^ cls._key) for b in chars])
            return decoded
        except:
            return "[CORRUPT_MEMORY]"
