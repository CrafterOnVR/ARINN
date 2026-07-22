
import os
import json
import time
from cryptography.fernet import Fernet
import base64

class SecureMemory:
    """
    Encrypted Memory System with Darwinian Evolution.
    Memories compete for survival based on Utility Scores.
    """
    def __init__(self, key_file="arinn_memory.key", storage_file="arinn_secure_memory.enc"):
        self.key_file = key_file
        self.storage_file = storage_file
        self.key = self._load_or_create_key()
        self.cipher_suite = Fernet(self.key)
        self.memory_cache = {} # Key -> {data, utility, access_count, last_access}
        self._load_memory()

    def _load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
            return key

    def _load_memory(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "rb") as f:
                    encrypted_data = f.read()
                decrypted_data = self.cipher_suite.decrypt(encrypted_data)
                self.memory_cache = json.loads(decrypted_data.decode('utf-8'))
            except Exception as e:
                print(f"Error loading secure memory: {e}. Starting fresh.")
                self.memory_cache = {}
        else:
            self.memory_cache = {}

    def _save_memory(self):
        try:
            data_str = json.dumps(self.memory_cache)
            encrypted_data = self.cipher_suite.encrypt(data_str.encode('utf-8'))
            with open(self.storage_file, "wb") as f:
                f.write(encrypted_data)
        except Exception as e:
            print(f"Error saving secure memory: {e}")

    def store(self, key, value, initial_utility=0.5):
        """
        Encrypt and store a value with evolutionary metadata.
        """
        self.memory_cache[key] = {
            "data": value,
            "utility": initial_utility,
            "access_count": 0,
            "last_access": time.time()
        }
        self._save_memory()

    def retrieve(self, key):
        """
        Retrieve a decrypted value and BOOST its evolutionary fitness.
        """
        record = self.memory_cache.get(key)
        if record:
            # Evolution: Being used increases survival chance
            record['access_count'] += 1
            record['utility'] = min(1.0, record['utility'] + 0.1) # Boost
            record['last_access'] = time.time()
            self._save_memory() # Persist access stats
            
            # Handle legacy format where value might be raw
            if isinstance(record, dict) and "data" in record:
                return record["data"]
            return record # Logic backup
        return None

    def deprioritize_memories(self, retention_ratio=0.8):
        """
        Memory Prioritization (Non-Destructive).
        Instead of getting deleted, low-utility memories are 'Available for Archival' (Priority -> 0).
        Lower priority means harder to retrieve or first to go if HARD disk limit hit.
        """
        if not self.memory_cache: return 0
        
        # Calculate scores
        items = []
        for k, v in self.memory_cache.items():
            if isinstance(v, dict) and "utility" in v:
                score = v['utility'] + (v['access_count'] * 0.01)
                items.append((k, score))
            else:
                items.append((k, 0.5))
        
        # Sort by score ascending (lowest first)
        items.sort(key=lambda x: x[1])
        
        # Determine cutoff
        count = len(items)
        cut_index = int(count * (1.0 - retention_ratio)) 
        
        if cut_index == 0: return 0
        
        keys_to_demote = [x[0] for x in items[:cut_index]]
        demoted_count = 0
        
        for k in keys_to_demote:
            # Demote utility to near zero, but keep data
            if self.memory_cache[k]['utility'] > 0.1:
                self.memory_cache[k]['utility'] = 0.05 
                self.memory_cache[k]['priority'] = 'ARCHIVE'
                demoted_count += 1
            
        self._save_memory()
        return demoted_count

    def get_heat_map(self):
        """
        Returns a heat map of memory temperatures.
        Temperature = Utility + (AccessCount / Age)
        Hot = Active/Useful. Cold = Archival Candidates.
        """
        heat_map = {}
        curr_time = time.time()
        for k, v in self.memory_cache.items():
            if isinstance(v, dict):
                age = max(1.0, curr_time - v.get('last_access', curr_time))
                temp = v.get('utility', 0.0) + (v.get('access_count', 0) / age)
                heat_map[k] = temp
        return heat_map

    def archive_cold_memories(self, temp_threshold=0.01):
        """
        Hyper-Efficiency: Move Cold memories to deep storage (Compression).
        """
        heat_map = self.get_heat_map()
        cold_keys = [k for k, temp in heat_map.items() if temp < temp_threshold]
        
        count = 0
        for k in cold_keys:
            if self.memory_cache[k].get('priority') != 'ARCHIVE':
                self.memory_cache[k]['priority'] = 'ARCHIVE'
                self.memory_cache[k]['utility'] *= 0.5 # Decay utility
                count += 1
                
        if count > 0: self._save_memory()
        return count

    # Legacy alias for compatibility, but safe now
    def prune_memories(self, retention_ratio=0.8):
        return self.deprioritize_memories(retention_ratio)

    def list_keys(self):
        return list(self.memory_cache.keys())
