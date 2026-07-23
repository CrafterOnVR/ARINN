# ARINN: Autonomous Recursive Improving Neural Network

ARINN is a fully autonomous, RLAIF-driven cognitive architecture designed to run locally on consumer hardware. It is not just a standard LLM wrapper—it is a self-modifying, asynchronous intelligence that writes its own code, mutates its own logic, and mathematically forces itself to become smarter using actual neural weight updates.

> [!NOTE]
> **Curious how it actually works?** You are not forced to read this README if you want the real technical details. For a massive deep-dive into how ARINN bypasses hardware limitations, intercepts OS-level execution, and forces mathematical constraints upon the neural network, read **[The Architecture Deep Dive](DEEP_DIVE.md)**.

## The Architecture

ARINN is composed of 19 advanced "Vault" concepts that transition theoretical Deep Learning research into a bare-metal execution environment. 

### Core Features

*   **The Async Swarm Orchestrator**: Uses `asyncio` and `ProcessPoolExecutor` to run 20 independent subagents simultaneously. The Swarm handles Research, Architectural Drafting, and AST Optimization in parallel without IO-blocking.
*   **True Neural Architecture (Qwen2.5-1.5B)**: Replaces generic API calls with a local, bare-metal inference engine using DirectML. Capable of dynamically synthesizing complex mathematical tools and Python modules on the fly.
*   **Autonomous Strict Unit Testing**: The Swarm doesn't just write code; it is mathematically forced to write rigorous `assert`-based test suites. Generated tools are executed in a strict AST Sandbox and are only approved if they pass their own logical unit tests.
*   **Atomic Rolling Backups (Night Cycle)**: Trains its own neural weights (LoRA) overnight using synthetic datasets of its daily successes. Utilizes atomic swap serialization to guarantee neural state stability even if the training is violently interrupted.
*   **Deep Sleep Darwinism (Ternary Mutation)**: Natively compresses 16-bit LoRA matrices into Ternary format (`-1, 0, 1`) and applies bitwise XOR mutations to simulate natural selection directly in the latent space.
*   **Semantic Self-Healing**: Uses OS-level `ctypes` to physically intercept the CPython global function table, hot-swapping memory pointers to replace broken functions while the script is running.
*   **The Epistemic Drive (Curiosity Engine)**: Replaces random Goal Autoinitialize with Expected Free Energy (EFE) minimization. ARINN scans its ChromaDB vector memory for empty clusters and synthesizes goals targeting concepts with the highest Bayesian Surprise.

## Hardware Requirements

ARINN was specifically engineered to bypass the NVIDIA CUDA monopoly. It utilizes `torch-directml` to run full inference and LoRA training locally on AMD consumer GPUs (e.g., RX 9060 XT, RX 7900 XTX) under Windows. 

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/CrafterOnVR/ARINN.git
    cd ARINN
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
4.  **Configure API Keys**:
    ARINN runs primary inference locally on Qwen2.5-1.5B via DirectML. However, for secondary heavy-reasoning fallback tasks (like the Debate Arena), you can configure an OpenRouter API key. Paste it into `launch_initialize.bat` on line 10 (`set LLM_API_KEY=your_openrouter_api_key_here`).
5.  **Engage the Singularity Protocol**:
    ```bash
    python run_arinn.py
    ```

## The Research Database (`data/research.db`)

ARINN stores its autonomous findings in a massive SQLite database. Because this file quickly exceeds 100MB, it is **not included in this repository**. 

You have two options to obtain the database:
1. **Hyperspeed Genesis Run**: You can regenerate the database locally by forcing ARINN to speedrun the Initial Learning Phase. Run:
    ```bash
    python run_initialize.py --hyperspeed
    ```
2. **Download Pre-compiled Database**: (Coming Soon) A fully populated `research.db` will be hosted on Hugging Face / GitHub Releases for direct download. Just drop it into the `data/` folder!

## Disclaimer

This architecture is highly experimental. It includes modules that perform OS-level memory pointer swizzling and unrestricted dynamic code generation. **Do not run this on a production server without the Zero-Trust Cyber Gauntlet active.**
