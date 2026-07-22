
import torch
import torch.nn as nn
import torch.nn.functional as F
import logging

class RefereeNet(nn.Module):
    """
    The Judge.
    A Meta-Network that evaluates the quality/coherence of expert outputs.
    It doesn't solve the problem itself; it solves "Who is right?".
    """
    def __init__(self, num_experts=20, input_dim=64):
        super(RefereeNet, self).__init__()
        # Input: Concat of all expert outputs [batch, num_experts * 64]? 
        # Too big. Instead, let's take the expert embeddings or just the gating weights + variance.
        
        # Simplified Referee: Takes the aggregated output variance and gating distribution
        self.fc1 = nn.Linear(num_experts, 32)
        self.fc2 = nn.Linear(32, 1) # Output: Confidence Score (0-1)

    def forward(self, gate_weights):
        x = F.relu(self.fc1(gate_weights))
        confidence = torch.sigmoid(self.fc2(x))
        return confidence

class DebateArena:
    """
    Manages the internal debate between asymmetric experts.
    """
    def __init__(self, hivemind):
        self.hivemind = hivemind
        self.referee = RefereeNet(num_experts=hivemind.num_experts).to(hivemind.output_projection.weight.device)
        self.optimizer = torch.optim.Adam(self.referee.parameters(), lr=0.005)

    def conduct_debate(self, x):
        """
        Runs the hivemind forward pass but intercepts expert outputs for analysis.
        """
        # 1. Standard Forward Pass (getting components)
        with torch.no_grad():
             # Re-implementing parts of forward to access internals
             #Ideally Hivemind would expose this, but we can just use the public model
             
             # Project
             expert_input = F.relu(self.hivemind.input_projection(x))
             
             # Gating
             gate_logits = self.hivemind.gating(x)
             gate_weights = F.softmax(gate_logits, dim=1)
             
             # Experts
             expert_outputs = []
             for expert in self.hivemind.experts:
                 expert_outputs.append(expert(expert_input))
                 
             stacked = torch.stack(expert_outputs, dim=1)
             
        # 2. Referee Analysis
        # Referee judges the *distribution* of the gating weights.
         # If gating is sharp (one expert dominates), confidence is high.
         # If gating is flat (disagreement), confidence should be low?
         # But maybe flat means "Consensus"? 
         # Let's train referee to predict "Stability".
        
        confidence = self.referee(gate_weights)
        
        return {
            "gate_weights": gate_weights,
            "expert_outputs": stacked,
            "referee_confidence": confidence.item()
        }

    def train_referee(self, x, target_success):
        """
        Train referee to predict if the hivemind will be correct.
        target_success: 1.0 if hivemind got it right, 0.0 if wrong.
        """
        gate_logits = self.hivemind.gating(x)
        gate_weights = F.softmax(gate_logits, dim=1)
        
        self.optimizer.zero_grad()
        prediction = self.referee(gate_weights)
        loss = F.mse_loss(prediction, torch.tensor([[target_success]]).to(prediction.device))
        loss.backward()
        self.optimizer.step()
        
        return loss.item()
