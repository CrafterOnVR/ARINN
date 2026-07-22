# ARINN: Autonomous Researching and Improving Neural Network
*Comprehensive Feature Specification*

ARINN is a next-generation autonomous agent designed for continuous self-improvement, deep research, and secure operation.

## 1. Core Architecture & Identity
*   **Dual-Process Identity**: `ArinnIdentity` orchestrates operation ("Worker") and evolution ("Architect").
*   **Neural Brain**: Custom PyTorch `SimpleNet` (16 hidden neurons) with Adam Optimizer and `ArinnBrain` wrapper.
*   **Secure Memory**: `Fernet`-encrypted storage (`arinn_secure_memory.enc`) for core memories.
*   **Bootloader Curriculum**: 6-phase growth path ensuring unique instance development.

## 2. Intelligence & Meta-Learning
*   **Hivemind Architecture (Phase 8)**: 
    *   **Structure**: 20 Interconnected Expert Networks (`SubBrain`) managed by a Mixture-of-Experts Gating system.
    *   **Neurogenesis**: Autonomous capability to expand hidden layers (+16 neurons) when learning plateaus are detected.
    *   **Deep Topology**: Experts use `[64, 256, 256, 256, 64]` architecture.
*   **Continuous Learning**: Cycles for `Reasoning`, `Efficiency`, `Simple Topics`, and `Real-World Learning`.
*   **Autonomous Meta-Efficiency (Phase 7)**: 
    *   **MetaOptimizer**: Dynamically tunes Learning Rate and Search Depth based on real-time `KnowledgeVelocity`.
*   **The Apprentice (Phase 10)**:
    *   **Self-Taught Programmer**: Autonomous "Coding Dojo" where the agent reads real Python source code and trains a specialized LSTM network (`CodeBrain`) to comprehend and generate syntax.
    *   **Curriculum Prioritization**: Sorts learning tasks by ROI (Value/Cost ratio).
*   **Asymmetric Meta-Cognition (Phase 11)**:
    *   **Divergent Thinking**: 5 Specialized Expert Types (Symbolic, Probabilistic, Creative, Critical, Compression).
    *   **Self-Debate**: A `RefereeNet` that judges conflicting expert outputs to determine the most stable answer.
    *   **Memory Darwinism**: Memories compete for survival; low-utility knowledge is autonomously pruned.
*   **Acceleration Curriculum (Phase 12)**:
    *   **The Compounding Order**: 10 Embedded "Axioms" for high-leverage cognitive growth (Error Analysis, Causal Reasoning, etc.).
    *   **Closed-Loop Mastery**: Each skill has defined `signals_of_mastery` to prevent premature progression.
    *   **Tool Inventing**: Capability to invent "Search-Space Pruners" and other mental operators (Module 10).
    *   **Autonomous Study**: Agent actively researches these concepts to upgrade its own reasoning.
*   **Explainable Reasoning (Phase 6)**: Generates human-readable traces for 80/90 rule decisions (`explain_decision`).
*   **Semantic Pattern Recognition**: `AdvancedPatternIntelligence` extracts knowledge graphs.

## 3. Advanced Research Engine
*   **Hybrid Fetcher**: Async `httpx` + Selenium (Headless Chrome/Firefox) for dynamic content.
*   **Multi-Engine Search**: `duckduckgo_search` with rate-limiting and anonymity.
*   **Cross-Verification (Phase 6)**: `CrossVerifier` checks facts against a trusted whitelist (Wikipedia, Arxiv, Python.org).
*   **Real-World Learning (Phase 5)**: Replaced simulations with genuine scraping of technical docs and news.

## 4. Automation & Task Management
*   **Advanced Automation Engine**: Async task queue with dependency management.
*   **Task Forecasting (Phase 6)**: Probabilistic prediction of next-step tasks based on history.
*   **GitHub Orchestration**: Full control (Issues, PRs, Workflow triggers) via `GitPython` and REST API.
*   **Isolated Sandboxes (Phase 6)**: `SandboxExecutor` runs experimental code in secure subprocesses with timeouts.

## 5. Safety, Integrity & Self-Improvement
*   **Hardened Failsafe (Phase 7)**: `FailsafeGuard` (standalone) creates cryptographic snapshots and auto-rolls back on corruption.
*   **Strict Permissions (Phase 5)**: Self-improvement requires explicit `permission.json` confirmation and auto-revokes after use.
*   **Verification Manager (Phase 5)**: Validates SHA-256 checksums and syntax before allowing any code change.
*   **Self-Modification**: `SelfImprovementManager` capable of analyzing and editing own source (when permitted).

## 6. User Interfaces
*   **PyQt6 Desktop GUI**: Real-time dashboard with health checks, visualization tabs, and control toggles.
*   **Interactive CLI**: Terminal-based continuous learning loop interaction.
