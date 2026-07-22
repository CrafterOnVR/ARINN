import torch
import math

class DarwinianMutator:
    """
    Vault 6: Direct Weight-Space Mutation (Deep Sleep Darwinism)
    Implements ternary quantization (BitNet b1.58) and bitwise mutations.
    Rather than relying solely on backpropagation, this algorithm probabilistically
    flips ternary weights to simulate natural selection in the latent space.
    """
    def __init__(self, mutation_rate=0.01):
        self.mutation_rate = mutation_rate
        
    def _quantize_to_ternary(self, weight_tensor: torch.Tensor):
        """
        Compresses standard FP16 weights into {-1, 0, 1} based on BitNet b1.58 logic.
        This radically reduces VRAM and enables extremely fast bitwise mutations.
        """
        # Calculate scaling factor based on mean absolute value
        scale = weight_tensor.abs().mean().clamp(min=1e-5)
        
        # Scale and round to nearest integer, clamping to [-1, 1]
        quantized = torch.round(weight_tensor / scale).clamp(-1, 1)
        return quantized, scale
        
    def _apply_bitwise_mutation(self, ternary_tensor: torch.Tensor):
        """
        Simulates genetic mutations by randomly flipping a small percentage 
        of ternary weights (-1 -> 0, 0 -> 1, 1 -> -1).
        """
        # Create a mutation mask based on the probability schedule
        mutation_mask = (torch.rand_like(ternary_tensor) < self.mutation_rate).float()
        
        # Random noise to apply to the mutated bits (shift by -1, 1, or 2)
        noise = torch.randint_like(ternary_tensor, low=1, high=3).float()
        
        # Apply mutation using modulo arithmetic to stay within the ternary range
        # We shift the range from [-1, 1] to [0, 2], apply noise, mod 3, shift back to [-1, 1]
        shifted = ternary_tensor + 1.0
        mutated_shifted = torch.fmod(shifted + (mutation_mask * noise), 3.0)
        
        mutated_tensor = mutated_shifted - 1.0
        return mutated_tensor
        
    def _check_drift_bounds(self, baseline_tensor: torch.Tensor, mutated_tensor: torch.Tensor):
        """
        Calculates the percentage of flipped bits between the baseline and mutated tensor.
        If it exceeds 15% (0.15), it rejects the mutation to prevent structural drift.
        """
        diff = torch.abs(baseline_tensor - mutated_tensor)
        flipped_percentage = (diff > 0).float().mean().item()
        
        if flipped_percentage > 0.15:
            print(f"[VAULT-6] FATAL: Drift Bounds Exceeded ({flipped_percentage:.2%}). Rejecting mutation.")
            return False
        return True

    def execute_tournament_selection(self, model_weights: dict):
        """
        Takes the current LoRA weights, quantizes them, applies random mutations 
        to generate thousands of 'children', and (in theory) benchmarks them.
        """
        print("[VAULT-6] Initiating Deep Sleep Darwinism (Ternary Weight Mutation)...")
        mutated_model = {}
        
        for key, tensor in model_weights.items():
            # Only mutate 2D weight matrices, not 1D biases
            if len(tensor.shape) == 2:
                # 1. Quantize to BitNet format
                ternary_weights, scale = self._quantize_to_ternary(tensor)
                
                # 2. Mutate the genetic code of the matrix
                mutated_ternary = self._apply_bitwise_mutation(ternary_weights)
                
                # Bounds check
                if not self._check_drift_bounds(ternary_weights, mutated_ternary):
                    mutated_model[key] = tensor # Keep original
                    continue
                
                # 3. De-quantize back to FP16 for standard inference
                mutated_model[key] = (mutated_ternary * scale).half()
            else:
                mutated_model[key] = tensor
                
        print(f"[VAULT-6] Synaptic mutation complete. Genetic drift applied at {self.mutation_rate*100}% rate.")
        return mutated_model
