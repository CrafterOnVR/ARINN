import os
import sys
import torch
from torch.utils.data import Dataset, DataLoader
import sqlite3
import numpy as np

project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from memory_manager import MemoryManager

class HybridGenesisDataset(Dataset):
    def __init__(self, root_dir, max_samples=None):
        self.root_dir = root_dir
        self.memory = MemoryManager(root=root_dir)
        
        # Connect to SQLite to get the actual texts
        db_path = os.path.join(root_dir, "data", "research.db")
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        print("Extracting Genesis Data from SQLite...")
        # We only take snippets here for faster training
        cur.execute("SELECT id, text FROM snippets WHERE text IS NOT NULL")
        rows = cur.fetchall()
        if max_samples:
            rows = rows[:max_samples]
            
        self.samples = []
        
        # We need a basic tokenizer for demonstration. 
        # In a full system, we'd use Byte-Pair Encoding.
        print("Synthesizing Neural-Semantic Mappings...")
        for row_id, content in rows:
            # We query ChromaDB to get the semantic embedding for this content
            # To get the embedding without searching, we just compute it using the memory's embedder
            try:
                emb = self.memory.embedding_function([content[:500]])[0]
                self.samples.append({
                    "text": content,
                    "embedding": emb
                })
            except Exception as e:
                pass
                
        conn.close()
        print(f"Successfully built dataset with {len(self.samples)} hybrid samples.")
        
    def __len__(self):
        return len(self.samples)
        
    def __getitem__(self, idx):
        sample = self.samples[idx]
        text = sample["text"]
        emb = sample["embedding"]
        
        # Extremely basic mock tokenization for the proof of concept (ASCII values)
        # Sequence length capped at 128 tokens
        tokens = [ord(c) % 50000 for c in text[:128]]
        if len(tokens) < 128:
            tokens += [0] * (128 - len(tokens))
            
        input_ids = torch.tensor(tokens, dtype=torch.long)
        # The target is the same sequence shifted by 1 (standard causal language modeling)
        target_ids = torch.tensor(tokens[1:] + [0], dtype=torch.long)
        semantic_vec = torch.tensor(emb, dtype=torch.float32)
        
        return input_ids, semantic_vec, target_ids

if __name__ == "__main__":
    dataset = HybridGenesisDataset(project_root, max_samples=100)
    print("Sample 0 Input Shape:", dataset[0][0].shape)
    print("Sample 0 Semantic Shape:", dataset[0][1].shape)
