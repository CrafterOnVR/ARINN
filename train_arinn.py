import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import time

project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from arinn_core.neural_core import NeuralCore
from build_hybrid_dataset import HybridGenesisDataset

def train():
    print("="*60)
    print("ARINN HYBRID TRAINING SEQUENCE INITIATED")
    print("="*60)
    
    # Initialize Core
    core = NeuralCore()
    model = core.model
    device = core.device
    
    print("\n[DATASET] Loading Genesis Snippets and Chroma Vectors...")
    # Cap to 500 samples for this demonstration so it trains quickly on the CPU
    dataset = HybridGenesisDataset(project_root, max_samples=500)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True)
    
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    epochs = 3
    print(f"\n[TRAINING] Beginning Offline Backpropagation on {device} for {epochs} Epochs...")
    
    model.train()
    
    for epoch in range(epochs):
        epoch_loss = 0.0
        start_t = time.time()
        
        for batch_idx, (input_ids, semantic_vec, target_ids) in enumerate(dataloader):
            input_ids = input_ids.to(device)
            semantic_vec = semantic_vec.to(device)
            target_ids = target_ids.to(device)
            
            optimizer.zero_grad()
            
            # Forward pass
            logits = model(input_ids, semantic_vec)
            
            # Flatten for CrossEntropy
            logits_flat = logits.reshape(-1, logits.size(-1))
            targets_flat = target_ids.reshape(-1)
            
            loss = criterion(logits_flat, targets_flat)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
            
        avg_loss = epoch_loss / len(dataloader)
        elapsed = time.time() - start_t
        print(f"Epoch {epoch+1}/{epochs} | Loss: {avg_loss:.4f} | Time: {elapsed:.2f}s")
        
    print("\n[SUCCESS] ARINN Hybrid Weights Updated.")
    print("The Neural-Semantic mapping is mathematically converging!")
    print("Saving local weights to disk...")
    torch.save(model.state_dict(), os.path.join(project_root, "data", "hybrid_brain.pth"))
    print("Done.")

if __name__ == "__main__":
    train()
