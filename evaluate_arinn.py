import os
import sys
import torch
import torch.nn.functional as F

project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from arinn_core.neural_core import NeuralCore, HybridTransformer
from memory_manager import MemoryManager

def evaluate():
    print("="*60)
    print("ARINN HYBRID EVALUATION SEQUENCE")
    print("="*60)
    
    device = torch.device("cpu")
    model = HybridTransformer().to(device)
    
    weights_path = os.path.join(project_root, "data", "hybrid_brain.pth")
    if not os.path.exists(weights_path):
        print("Error: hybrid_brain.pth not found. Train the model first.")
        return
        
    model.load_state_dict(torch.load(weights_path, weights_only=True))
    model.eval()
    print("Loaded trained Hybrid Brain weights.")
    
    memory = MemoryManager(root=project_root)
    
    test_prompts = [
        "def fibonacci(n):",
        "The core principle of recursive self-improvement is",
        "class AutonomousAgent:"
    ]
    
    print("\nRunning Generative Inference Tests...")
    
    with torch.no_grad():
        for prompt in test_prompts:
            print(f"\n--- PROMPT: '{prompt}' ---")
            
            # Get Semantic Vector from ChromaDB
            emb = memory.embedding_function([prompt])[0]
            semantic_vec = torch.tensor(emb, dtype=torch.float32).unsqueeze(0).to(device)
            
            # ASCII mock tokenization
            tokens = [ord(c) % 50000 for c in prompt]
            input_ids = torch.tensor(tokens, dtype=torch.long).unsqueeze(0).to(device)
            
            # Generate 20 tokens (characters) autoregressively
            generated_tokens = tokens.copy()
            for _ in range(20):
                logits = model(input_ids, semantic_vec)
                # Get the last token's logits
                next_token_logits = logits[0, -1, :]
                
                # Sample or Argmax
                # Using greedy decoding (argmax) for deterministic testing
                next_token = torch.argmax(next_token_logits).item()
                
                generated_tokens.append(next_token)
                input_ids = torch.tensor(generated_tokens, dtype=torch.long).unsqueeze(0).to(device)
                
            # Decode ASCII
            output_text = "".join([chr(t) for t in generated_tokens])
            print(f"OUTPUT:\n{output_text}")
            
if __name__ == "__main__":
    evaluate()
