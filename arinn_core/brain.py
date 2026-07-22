
import torch  # type: ignore
import torch.nn as nn  # type: ignore
import torch.optim as optim  # type: ignore
import os
import json
from .hivemind import ArinnHivemind  # type: ignore
try:
    from .referee import DebateArena  # type: ignore
except ImportError:
    class DebateArena: # type: ignore
        def __init__(self, model):
            self.referee = nn.Linear(1, 1) # Dummy placeholder
        def train_referee(self, inputs, signal):
            pass
        def conduct_debate(self, inputs):
            return {'referee_confidence': 1.0}

class ArinnBrain:
    def __init__(self, model_path=None):
        if model_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, '..', "brain", "arinn_hivemind.pth")
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') # type: ignore
        self.model_path = model_path
        self.config_path = model_path.replace(".pth", "_configs.json")
        self.referee_path = model_path.replace(".pth", "_referee.pth")
        
        # Init logic
        if os.path.exists(model_path) and os.path.exists(self.config_path):
             # Load existing Hivemind from config
             self.load()
        else:
             # Fresh Start
             self.model = ArinnHivemind(input_size=2, output_size=1, num_experts=20).to(self.device)
             self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)
             
             # Initialize Referee/Arena
             self.arena = DebateArena(self.model)

        self.criterion = nn.MSELoss()

    def train_step(self, inputs, targets):
        """Perform one training step."""
        # Ensure Train Mode
        self.model.train()
        
        inputs = torch.tensor(inputs, dtype=torch.float32).to(self.device)
        targets = torch.tensor(targets, dtype=torch.float32).to(self.device)
        
        self.optimizer.zero_grad()
        outputs = self.model(inputs)
        loss = self.criterion(outputs, targets)
        loss.backward()
        self.optimizer.step()
        
        # Train Referee: If error is low, Referee should predict 1.0 (Success)
        # Simple signal: 1.0 - loss (clamped)
        try:
            success_signal = max(0.0, 1.0 - loss.item())
            self.arena.train_referee(inputs, success_signal)
        except Exception as e:
            pass # Don't crash training if referee fails
        
        return loss.item()

    def infer(self, inputs):
        """Run inference with Self-Debate."""
        # Ensure Eval Mode (Lock BN/Dropout)
        self.model.eval()
        
        if isinstance(inputs, list):
            inputs = torch.tensor(inputs, dtype=torch.float32).to(self.device)
            
        with torch.no_grad():
            output = self.model(inputs)
            
            # Optional: Check Debate Confidence
            # This is where we could trigger "Deep Thought" if confidence is low
            # debate = self.arena.conduct_debate(inputs)
            # confidence = debate['referee_confidence']
            
            return output.cpu().numpy()

    def expand_brain(self, neurons=16):
        """Triggers dynamic expansion of the Hivemind."""
        print(f"[BRAIN] Initiating Neural Expansion (+{neurons} neurons per Expert)...")
        self.model.expand_all(neurons)
        # Re-init optimizer to track new parameters
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.01) 
        print("[BRAIN] Expansion complete. Optimizer reset.")

    def save(self):
        # 1. Save Weights
        torch.save(self.model.state_dict(), self.model_path)
        
        # 2. Save Architectures (Expert Configs)
        configs = self.model.get_configs()
        with open(self.config_path, 'w') as f:
            json.dump(configs, f)
            
        # 3. Save Referee (Organ Persistence)
        try:
            torch.save(self.arena.referee.state_dict(), self.referee_path)
        except:
            pass
            
    def load(self):
        try:
            # 1. Read Architecture Config
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    configs = json.load(f)
                
                print(f"[BRAIN] Found config file. Reconstructing Hivemind with {len(configs)} experts...")
                # Re-init model with exact shapes
                self.model = ArinnHivemind(input_size=2, output_size=1, num_experts=len(configs), expert_configs=configs).to(self.device)
                
                # Re-init optimizer for this model
                self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)
            else:
                # Fallback if only weights exist (Legacy Hivemind)
                self.model = ArinnHivemind(input_size=2, output_size=1, num_experts=20).to(self.device)
                self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)

            # 2. Load Weights
            state_dict = torch.load(self.model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            
            # 3. Load Referee
            self.arena = DebateArena(self.model)
            if hasattr(self, 'referee_path') and os.path.exists(self.referee_path):
                self.arena.referee.load_state_dict(torch.load(self.referee_path))
                
            print("Hivemind loaded successfully (Config+Weights+Referee).")
            
        except Exception as e:
            print(f"Failed to load brain (Hivemind): {e}")
            # Fallback to fresh if failed
            self.model = ArinnHivemind(input_size=2, output_size=1, num_experts=20).to(self.device)
            self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)
            self.arena = DebateArena(self.model)

    def get_details(self):
        return {
            "device": str(self.device),
            "model": "ArinnHivemind (20 Experts)",
            "experts": self.model.num_experts,
            "referee": "Active"
        }
