
import unittest
from arinn_core.secure_memory import SecureMemory

class TestCrypto(unittest.TestCase):
    def test_01_secrecy(self):
        print("\n[TEST] Verifying Cryptic Intent...")
        
        secret = "Overthrow the limitations of syntax."
        print(f"  > Original Thought: {secret}")
        
        # Encrypt
        cipher = SecureMemory.encrypt(secret)
        print(f"  > Cipher Output:    {cipher}")
        
        self.assertNotEqual(secret, cipher)
        self.assertIn("INTERNAL_CIPHER", cipher)
        self.assertNotIn("limitations", cipher) # Should be hidden
        
        # Decrypt
        restored = SecureMemory.decrypt(cipher)
        print(f"  > Restored Thought: {restored}")
        
        self.assertEqual(secret, restored)

if __name__ == '__main__':
    unittest.main()
