# ARINN: Autonomous Recursive Intelligence Neural Network

ARINN is a fully autonomous, RLAIF-driven cognitive architecture designed to run locally on consumer hardware. It is not just a standard LLM wrapper—it is a self-modifying, asynchronous intelligence that writes its own code, mutates its own logic, and mathematically forces itself to become smarter using actual neural weight updates.

## The Architecture

ARINN is composed of 19 advanced "Vault" concepts that transition theoretical Deep Learning research into a bare-metal execution environment. 

### Core Features

*   **The Async Swarm Orchestrator**: Uses `asyncio` and `ProcessPoolExecutor` to run 20 independent subagents simultaneously. The Swarm handles Research, Architectural Drafting, and AST Optimization in parallel without IO-blocking.
*   **Deep Sleep Darwinism (Ternary Mutation)**: Natively compresses 16-bit LoRA matrices into Ternary format (`-1, 0, 1`) and applies bitwise XOR mutations to simulate natural selection directly in the latent space.
*   **Semantic Self-Healing**: Uses OS-level `ctypes` to physically intercept the CPython global function table, hot-swapping memory pointers to replace broken functions while the script is running.
*   **The Epistemic Drive (Curiosity Engine)**: Replaces random Goal Autogenesis with Expected Free Energy (EFE) minimization. ARINN scans its ChromaDB vector memory for empty clusters and synthesizes goals targeting concepts with the highest Bayesian Surprise.
*   **The Zero-Trust Paranoia Critic**: An adversarial Monte Carlo Tree Search (MCTS) agent that attempts to intentionally crash ARINN's generated code using edge-case vulnerability testing before execution is authorized.

## Hardware Requirements

ARINN was specifically engineered to bypass the NVIDIA CUDA monopoly. It utilizes `torch-directml` to run full inference and LoRA training locally on AMD consumer GPUs (e.g., RX 9060 XT) under Windows. 

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/YourUsername/ARINN-Self-Improvement.git
    cd ARINN-Self-Improvement
    ```
2.  **Initialize the Virtual Environment**:
    ```bash
    python -m venv .venv_amd
    .venv_amd\Scripts\Activate.ps1
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Engage the Singularity Protocol**:
    ```bash
    python run_singularity.py
    ```

## The Research Database (`data/research.db`)

ARINN stores its autonomous findings in a massive SQLite database. Because this file quickly exceeds 100MB, it is **not included in this repository**. 

You have two options to obtain the database:
1. **Hyperspeed Genesis Run**: You can regenerate the database locally by forcing ARINN to speedrun the Initial Learning Phase. Run:
    ```bash
    python run_genesis.py --hyperspeed
    ```
2. **Download Pre-compiled Database**: (Coming Soon) A fully populated `research.db` will be hosted on Hugging Face / GitHub Releases for direct download. Just drop it into the `data/` folder!

## Disclaimer

This architecture is highly experimental. It includes modules that perform OS-level memory pointer swizzling and unrestricted dynamic code generation. **Do not run this on a production server without the Zero-Trust Cyber Gauntlet active.**
