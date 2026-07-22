"""
ARINN Autoresearch training script — AMD/CPU compatible version.
Stripped of NVIDIA-only dependencies (Flash Attention 3, torch.compile CUDA, etc.).
Uses standard PyTorch ops that work on any backend.

This is a simplified but functional version of train.py for the
autoresearch optimization loop.

Usage: python train_amd.py
"""

import os
import gc
import math
import time
import sys
from dataclasses import dataclass, asdict

import torch  # type: ignore
import torch.nn as nn  # type: ignore
import torch.nn.functional as F  # type: ignore

# Import from the prepare.py in same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prepare import MAX_SEQ_LEN, TIME_BUDGET, EVAL_TOKENS, Tokenizer, _document_batches, get_token_bytes  # type: ignore


# ---------------------------------------------------------------------------
# Device-agnostic dataloader (replaces CUDA-only version from prepare.py)
# ---------------------------------------------------------------------------

def make_dataloader_generic(tokenizer, B, T, split, device, buffer_size=1000):
    """CPU/AMD compatible dataloader without CUDA pinned memory."""
    assert split in ["train", "val"]
    row_capacity = T + 1
    batches = _document_batches(split)
    bos_token = tokenizer.get_bos_token_id()
    doc_buffer = []
    epoch = 1

    def refill_buffer():
        nonlocal epoch
        doc_batch, epoch = next(batches)
        token_lists = tokenizer.encode(doc_batch, prepend=bos_token)
        doc_buffer.extend(token_lists)

    row_buffer = torch.empty((B, row_capacity), dtype=torch.long)

    while True:
        for row_idx in range(B):
            pos = 0
            while pos < row_capacity:
                while len(doc_buffer) < buffer_size:
                    refill_buffer()
                remaining = row_capacity - pos
                best_idx = -1
                best_len = 0
                for i, doc in enumerate(doc_buffer):
                    doc_len = len(doc)
                    if doc_len <= remaining and doc_len > best_len:
                        best_idx = i
                        best_len = doc_len
                if best_idx >= 0:
                    doc = doc_buffer.pop(best_idx)
                    row_buffer[row_idx, pos:pos + len(doc)] = torch.tensor(doc, dtype=torch.long)
                    pos += len(doc)
                else:
                    shortest_idx = min(range(len(doc_buffer)), key=lambda i: len(doc_buffer[i]))
                    doc = doc_buffer.pop(shortest_idx)
                    row_buffer[row_idx, pos:pos + remaining] = torch.tensor(doc[:remaining], dtype=torch.long) # type: ignore
                    pos += remaining

        inputs = row_buffer[:, :-1].to(device)
        targets = row_buffer[:, 1:].to(device)
        yield inputs, targets, epoch


@torch.no_grad()
def evaluate_bpb_generic(model, tokenizer, batch_size, device):
    """Device-agnostic BPB evaluation."""
    # Load token_bytes to CPU first, then transfer (avoids DirectML torch.load bug)
    token_bytes = get_token_bytes(device="cpu").to(device)
    val_loader = make_dataloader_generic(tokenizer, batch_size, MAX_SEQ_LEN, "val", device)
    steps = EVAL_TOKENS // (batch_size * MAX_SEQ_LEN)
    total_nats = 0.0
    total_bytes = 0
    for _ in range(steps):
        x, y, _ = next(val_loader)
        loss_flat = model(x, y, reduction='none').reshape(-1)
        y_flat = y.reshape(-1)
        nbytes = token_bytes[y_flat]
        mask = nbytes > 0
        total_nats += (loss_flat * mask).sum().item()
        total_bytes += nbytes.sum().item()
    return total_nats / (math.log(2) * total_bytes)

# ---------------------------------------------------------------------------
# GPT Model (AMD-Compatible — No Flash Attention, No torch.compile)
# ---------------------------------------------------------------------------

@dataclass
class GPTConfig:
    sequence_len: int = 2048
    vocab_size: int = 32768
    n_layer: int = 8
    n_head: int = 4
    n_embd: int = 512
    dropout: float = 0.0


def norm(x):
    return F.rms_norm(x, (x.size(-1),))


class CausalSelfAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.n_head = config.n_head
        self.n_embd = config.n_embd
        self.head_dim = self.n_embd // self.n_head
        assert self.n_embd % self.n_head == 0

        self.c_attn = nn.Linear(self.n_embd, 3 * self.n_embd, bias=False)
        self.c_proj = nn.Linear(self.n_embd, self.n_embd, bias=False)
        self.dropout = config.dropout

    def forward(self, x):
        B, T, C = x.size()
        qkv = self.c_attn(x)
        q, k, v = qkv.split(self.n_embd, dim=2)
        q = q.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        k = k.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        v = v.view(B, T, self.n_head, self.head_dim).transpose(1, 2)

        # Standard PyTorch scaled_dot_product_attention (works on all backends)
        y = F.scaled_dot_product_attention(
            q, k, v,
            is_causal=True,
            dropout_p=self.dropout if self.training else 0.0
        )
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        y = self.c_proj(y)
        return y


class MLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.c_fc = nn.Linear(config.n_embd, 4 * config.n_embd, bias=False)
        self.c_proj = nn.Linear(4 * config.n_embd, config.n_embd, bias=False)

    def forward(self, x):
        x = self.c_fc(x)
        x = F.gelu(x)
        x = self.c_proj(x)
        return x


class Block(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.attn = CausalSelfAttention(config)
        self.mlp = MLP(config)

    def forward(self, x):
        x = x + self.attn(norm(x))
        x = x + self.mlp(norm(x))
        return x


class GPT(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.transformer = nn.ModuleDict({
            "wte": nn.Embedding(config.vocab_size, config.n_embd),
            "wpe": nn.Embedding(config.sequence_len, config.n_embd),
            "h": nn.ModuleList([Block(config) for _ in range(config.n_layer)]),
        })
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)

    def forward(self, idx, targets=None, reduction='mean'):
        B, T = idx.size()
        pos = torch.arange(0, T, dtype=torch.long, device=idx.device).unsqueeze(0)

        tok_emb = self.transformer.wte(idx)
        pos_emb = self.transformer.wpe(pos)
        x = tok_emb + pos_emb

        for block in self.transformer.h:
            x = block(x)
        x = norm(x)

        logits = self.lm_head(x)

        if targets is not None:
            loss = F.cross_entropy(
                logits.reshape(-1, logits.size(-1)),
                targets.reshape(-1),
                ignore_index=-1,
                reduction=reduction
            )
            return loss
        return logits

    def estimate_flops(self):
        nparams = sum(p.numel() for p in self.parameters())
        return 6 * nparams

# ---------------------------------------------------------------------------
# Hyperparameters
# ---------------------------------------------------------------------------

DEPTH = 4               # Number of transformer layers (smaller for CPU/AMD)
MODEL_DIM = 256         # Embedding dimension
NUM_HEADS = 4           # Attention heads
TOTAL_BATCH_SIZE = 2**16  # ~64K tokens per step (reduced for CPU)
DEVICE_BATCH_SIZE = 16   # Micro-batch size
LEARNING_RATE = 3e-4
WARMUP_STEPS = 10
WEIGHT_DECAY = 0.1

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

t_start = time.time()
torch.manual_seed(42)

# Device selection: prefer CUDA > DirectML > CPU
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"Using CUDA: {torch.cuda.get_device_name()}")
else:
    try:
        import torch_directml  # type: ignore
        device = torch_directml.device()
        print(f"Using DirectML (AMD GPU acceleration)")
    except ImportError:
        device = torch.device("cpu")
        print(f"Using CPU (install torch-directml for AMD GPU acceleration)")

print(f"Device: {device}")

tokenizer = Tokenizer.from_directory()
vocab_size = tokenizer.get_vocab_size()
print(f"Vocab size: {vocab_size:,}")

config = GPTConfig(
    sequence_len=MAX_SEQ_LEN,
    vocab_size=vocab_size,
    n_layer=DEPTH,
    n_head=NUM_HEADS,
    n_embd=MODEL_DIM,
)
print(f"Model config: {asdict(config)}") # type: ignore

model = GPT(config).to(device)

num_params = sum(p.numel() for p in model.parameters())
print(f"Parameters: {num_params:,} ({num_params/1e6:.1f}M)")

tokens_per_fwdbwd = DEVICE_BATCH_SIZE * MAX_SEQ_LEN
grad_accum_steps = max(1, TOTAL_BATCH_SIZE // tokens_per_fwdbwd)

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=LEARNING_RATE,
    betas=(0.9, 0.95),
    weight_decay=WEIGHT_DECAY,
    fused=False,
)

train_loader = make_dataloader_generic(tokenizer, DEVICE_BATCH_SIZE, MAX_SEQ_LEN, "train", device)

print(f"Time budget: {TIME_BUDGET}s")
print(f"Gradient accumulation steps: {grad_accum_steps}")

# ---------------------------------------------------------------------------
# LR Schedule
# ---------------------------------------------------------------------------

def get_lr(step, warmup_steps, max_steps):
    if step < warmup_steps:
        return LEARNING_RATE * step / max(warmup_steps, 1)
    progress = (step - warmup_steps) / max(max_steps - warmup_steps, 1)
    return LEARNING_RATE * 0.5 * (1.0 + math.cos(math.pi * progress))

# ---------------------------------------------------------------------------
# Training Loop
# ---------------------------------------------------------------------------

print("\n--- Training Start ---")
t_train_start = time.time()
total_training_time = 0
step = 0
smooth_loss = 0

try:
    while True:
        t0 = time.time()
        model.train()

        for micro_step in range(grad_accum_steps):
            x, y, epoch = next(train_loader)

            loss = model(x, y)
            loss_item = loss.detach().item()
            loss = loss / grad_accum_steps
            loss.backward()

        # Update LR
        lr = get_lr(step, WARMUP_STEPS, int(TIME_BUDGET / 0.5))  # rough estimate
        for pg in optimizer.param_groups:
            pg['lr'] = lr

        # Clip gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

        optimizer.step()
        optimizer.zero_grad(set_to_none=True)

        t1 = time.time()
        dt = t1 - t0

        if step > 5:
            total_training_time += dt # type: ignore

        # Logging
        ema = 0.9
        smooth_loss = ema * smooth_loss + (1 - ema) * loss_item
        debiased = smooth_loss / (1 - ema ** (step + 1))
        pct = 100 * min(total_training_time / TIME_BUDGET, 1.0) # type: ignore
        tok_sec = int(TOTAL_BATCH_SIZE / max(dt, 0.001))
        remaining = max(0, TIME_BUDGET - total_training_time) # type: ignore

        print(f"\rstep {step:04d} ({pct:.1f}%) | loss: {debiased:.4f} | lr: {lr:.2e} | dt: {dt*1000:.0f}ms | tok/s: {tok_sec:,} | epoch: {epoch} | rem: {remaining:.0f}s    ", end="", flush=True)

        # GC
        if step == 0:
            gc.collect()

        step += 1

        if step > 5 and total_training_time >= TIME_BUDGET:
            break

except KeyboardInterrupt:
    print("\n\n[!] Training interrupted by user.")

print("\n\n--- Training Complete ---")

total_tokens = step * TOTAL_BATCH_SIZE

# Final eval
model.eval()
with torch.no_grad():
    val_bpb = evaluate_bpb_generic(model, tokenizer, DEVICE_BATCH_SIZE, device)

# Summary
t_end = time.time()
print("---")
print(f"val_bpb:          {val_bpb:.6f}")
print(f"training_seconds: {total_training_time:.1f}")
print(f"total_seconds:    {t_end - t_start:.1f}")
print(f"total_tokens_M:   {total_tokens / 1e6:.1f}")
print(f"num_steps:        {step}")
print(f"num_params_M:     {num_params / 1e6:.1f}")
print(f"depth:            {DEPTH}")

if device.type == "cuda":
    peak_vram_mb = torch.cuda.max_memory_allocated() / 1024 / 1024
    print(f"peak_vram_mb:     {peak_vram_mb:.1f}")
else:
    print(f"peak_vram_mb:     0.0")
