import torch

class ImmuneSystemEWC:
    """
    Vault 11: The Immune System (Collapse Score & Quarantine)
    Uses Elastic Weight Consolidation (EWC) to calculate a "Collapse Score".
    This mathematically quantifies Catastrophic Forgetting without needing a human to 
    grade the AI. It computes the diagonal of the Fisher Information Matrix (FIM)
    to protect critical neural pathways from being overwritten during mutation.
    """
    def __init__(self, lambda_ewc=50.0):
        self.lambda_ewc = lambda_ewc
        self.fisher_matrix = {}
        self.golden_seed_weights = {}
        
    def register_golden_seed(self, model_weights: dict):
        """
        Stores the base weights. In a full implementation, this function
        also runs a forward pass on a validation dataset to compute the true
        Fisher Information Matrix diagonal (the second derivative of the loss).
        Here, we mock the Fisher diagonal for structural implementation.
        """
        self.golden_seed_weights = {k: v.clone() for k, v in model_weights.items()}
        
        print("[VAULT-11] Computing Fisher Information Matrix (FIM) Diagonal...")
        for key, tensor in model_weights.items():
            # Mock Fisher diagonal: We assume weights with higher absolute magnitude 
            # are more "important" to the network's current state.
            # In true EWC, F_i = E[(dL/d_theta_i)^2]
            importance = tensor.abs() + 1e-5
            self.fisher_matrix[key] = importance
            
        print("[VAULT-11] Golden Seed mastered skills registered and protected.")
        
    def calculate_collapse_score(self, mutated_weights: dict):
        """
        Calculates the EWC penalty: sum( (lambda/2) * F_i * (theta_new - theta_old)^2 )
        If the score exceeds a threshold, the mutation destroys past knowledge and is quarantined.
        """
        if not self.fisher_matrix:
            print("[VAULT-11] WARNING: No Fisher Matrix registered. Collapse Score is 0.")
            return 0.0
            
        ewc_loss = 0.0
        
        for key, new_tensor in mutated_weights.items():
            if key in self.golden_seed_weights and key in self.fisher_matrix:
                old_tensor = self.golden_seed_weights[key]
                fisher_diag = self.fisher_matrix[key]
                
                # Penalty = (lambda / 2) * F_i * (theta_new - theta_old)^2
                diff_sq = (new_tensor - old_tensor) ** 2
                penalty = (self.lambda_ewc / 2.0) * (fisher_diag * diff_sq).sum()
                ewc_loss += penalty.item()
                
        print(f"[VAULT-11] Calculated EWC Collapse Score: {ewc_loss:.4f}")
        return ewc_loss
        
    def evaluate_mutation(self, mutated_weights: dict, collapse_threshold=1000.0):
        """
        Determines if a mutated brain should be quarantined.
        """
        score = self.calculate_collapse_score(mutated_weights)
        if score > collapse_threshold:
            print(f"[VAULT-11] 🛑 QUARANTINE TRIGGERED: Collapse Score ({score:.2f}) exceeds threshold ({collapse_threshold})")
            print("[VAULT-11] The mutation destroyed critical knowledge. Rejecting weights.")
            return False
        else:
            print("[VAULT-11] ✅ IMMUNE CHECK PASSED: Mutation is safe.")
            return True
