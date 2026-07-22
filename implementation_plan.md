# ARINN "Core Identity" Implementation Plan

## Goal Description
Transform the existing Research Agent into "ARINN" (Autonomous Researching and Improving Neural Network).
This involves implementing a simulated "Bootloader" learning curriculum where the agent must "grow" through phases (Meta-Learning, Logic Gates, etc.) before becoming fully operational.
We will also introduce a local Neural Network "Brain" and encrypted memory.

## User Review Required
> [!IMPORTANT]
> This change introduces `torch` (PyTorch) as a dependency. The user's environment must support it.
> The "Dual-Executable" requirement will be implemented using `multiprocessing` to keep the codebase unified but functionally separated.

## Proposed Changes

### Dependencies
#### [MODIFY] [requirements.txt](file:///c:/Users/dmdra/Development/research_agent/requirements.txt)
- Add `torch`
- Add `cryptography`

### New Core Package (`arinn_core/`)
We will create a new package to house the "Soul" of the machine.

#### [NEW] [arinn_core/__init__.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/__init__.py)

#### [NEW] [arinn_core/brain.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/brain.py)
- Defines `ArinnBrain` class.
- Uses PyTorch.
- Implements methods for `train(data)` and `infer(data)`.
- Capable of learning simple logic gates (XOR) for Phase 2.

#### [NEW] [arinn_core/bootloader.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/bootloader.py)
- Defines `Bootloader` class.
- Manages the 6 Phases of growth:
    1.  `META_LEARNING`: Optimizing hyperparameters.
    2.  `LOGIC_GATES`: Training the Brain on logical operations.
    3.  `EFFICIENCY`: optimizing model size/speed (simulated).
    4.  `INTERNAL_VOICE`: establishing internal reasoning loop.
    5.  `ROSETTA_STONE`: translating internal tokens to English.
    6.  `AUTONOMOUS_SCHOLAR`: The final "Working" state.
- Persists state to `bootloader_state.json`.

#### [NEW] [arinn_core/memory.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/memory.py)
- Defines `SecureMemory` class.
- Uses `cryptography.fernet` for encryption at rest.
- Wraps basic file I/O for "Core Memories".

#### [NEW] [arinn_core/identity.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/identity.py)
- The main entry point for the ARINN personality.
- Orchestrates the "Architect" vs "Worker" processes.

### Integration

#### [MODIFY] [super_enhanced_agent.py](file:///c:/Users/dmdra/Development/research_agent/super_enhanced_agent.py)
- Integrate `ArinnBrain` and `Bootloader`.
- If `Bootloader` is not complete, the Agent should refuse standard tasks and focus on "Self-Growth" tasks.
- Add `autonomous_choice()` method implementing the 80/90 rule.

## Phase 5: Verified Autonomous Learning & Integrity (Current)
This phase implements the "Real World" learning with strict safety rails.

### Core Safety Systems
#### [MODIFY] [safety_controller.py](file:///c:/Users/dmdra/Development/research_agent/safety_controller.py)
*   [NEW] Implement `VerificationManager` for integrity checks (checksums).
*   [NEW] Add `SelfImprovementPermission` class (state file: `permission.json`) requiring explicit "CONFIRMED" status.
*   [NEW] Implement `rollback_to_stable()` method.

### Self-Improvement Logic
#### [MODIFY] [self_improvement_manager.py](file:///c:/Users/dmdra/Development/research_agent/self_improvement_manager.py)
*   [UPDATE] `initiate_self_improvement`:
    1. Check `permission.json`. If not "CONFIRMED", abort.
    2. Create full snapshot (zip).
    3. Apply changes.
    4. **Run Verification Suite** (import valid modules, run test script).
    5. If fail: `safety_controller.rollback_to_stable()`.
    6. If pass: Request new permission (revoke current) or log success.

### Real-World Learning
#### [MODIFY] [continuous_learning.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/continuous_learning.py)
*   [NEW] `loop_real_world_learning()`:
    *   Uses `ResearchAgent` to fetch *real* news headlines or technical docs.
    *   Uses `ArinnBrain` to classify/analyze them.
    *   **TrustScore**: Verify source against a whitelist (e.g., reputable tech blogs, official docs).

## Verification Plan

### Automated Tests
- Test `ArinnBrain` can learn XOR (validate Phase 2).
- Test `Bootloader` state transitions.
- Test `SecureMemory` encrypts/decrypts correctly.
- [NEW] Test `rollback()` restores deleted/corrupted files.
- [NEW] Test `SelfImprovementPermission` blocks actions without confirmation.

### Manual Verification
- Run the agent.
- Observe the "Bootloader" phases in the logs/console.
- Verify it reaches "Phase 6" and becomes operational.
- Trigger `autonomous_choice` and ensure it respects the 80/90 rule.
- Attempt to maximize self-improvement and verify the "Permission Denied" prompt appears.

## Phase 6: Advanced Autonomy & Explainability (Current)
This phase enhances the agent with forecasting, explainability, and safe experiments.

### New Modules
#### [NEW] [arinn_core/cross_verifier.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/cross_verifier.py)
*   Implements `CrossVerifier` to check facts against multiple sources.
#### [NEW] [arinn_core/sandbox.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/sandbox.py)
*   Implements `SandboxExecutor` to run code in isolated subprocesses.

### Enhancements
#### [MODIFY] [arinn_core/identity.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/identity.py)
*   Add `explain_decision(context)`: Generates a human-readable trace of the 80/90 decision.
#### [MODIFY] [automation_engine.py](file:///c:/Users/dmdra/Development/research_agent/automation_engine.py)
*   Add `TaskForecaster`: Predicts next likely tasks based on history.


## Phase 7: Autonomous Meta-Efficiency
Focus: Optimizing *how* the agent learns (parameters/strategy) without modifying code.

### New Modules
#### [NEW] [arinn_core/meta_optimizer.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/meta_optimizer.py)
*   `MetaOptimizer`: Tracks `KnowledgeGainRate` and adjusts:
    *   `LearningRate` of the Brain.
    *   `SearchDepth` of the Researcher.
    *   `AutonomousThresholds` (80/90 rule).

#### [NEW] [safety_guard.py](file:///c:/Users/dmdra/Development/research_agent/safety_guard.py)
*   `FailsafeGuard`: A standalone validator that runs before/after key cycles to check integrity. "Hardened" means it has minimal dependencies and protects `backup_pre_upgrade`.

### Enhancements
#### [MODIFY] [arinn_core/continuous_learning.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/continuous_learning.py)
*   Integrate `MetaOptimizer`.
*   Replace static loops with dynamic curriculum ordering.

## Phase 8: Hivemind Architecture (Current)
Focus: Escalate intelligence by upgrading the single `SimpleNet` to a collaborative "Hivemind" of 20 interwoven Neural Networks.

### New Modules
#### [NEW] [arinn_core/hivemind.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/hivemind.py)
*   `SubBrain`: Individual expert network with architecture `[64, 256, 256, 256, 64]`.
*   `ArinnHivemind`: The container class managing 20 `SubBrain` instances.
    *   **Gating Network**: A "Chief" network that learns which Expert (SubBrain) to trust for a given input (Mixture of Experts).
    *   **Interconnection**: Outputs of one expert can optionally feed others (recurrence) or be aggregated.
    *   **Dynamic Expansion**: `expand_capacity()` method that adds 16 neurons to the hidden layers of ALL 20 SubBrains at runtime, preserving existing weights.

### Enhancements
#### [MODIFY] [arinn_core/meta_optimizer.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/meta_optimizer.py)
*   **Plateau Detection**: Monitor `KnowledgeVelocity`. If metric stagnates (e.g. error > 0.2 for 50 steps), trigger `hivemind.expand_all()`.
*   **Random Mutation**: Low probability chance to trigger expansion during exploration phases.

#### [MODIFY] [arinn_core/brain.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/brain.py)
*   Replace `SimpleNet` instantiation with `ArinnHivemind`.
*   Update `save()`/`load()` to handle the complex state of 20+ models.
*   Expose `expand_brain()` method to user CLI.

## Phase 9: Dynamic Architecture Persistence (Current)
Focus: Robust loading of evolved neural architectures and proper inference modes.

### Enhancements
#### [MODIFY] [arinn_core/hivemind.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/hivemind.py)
*   Update `SubBrain.__init__` to accept `hidden_sizes` (list or int) to reconstruct grown networks.
*   Update `ArinnHivemind.__init__` to accept `expert_configs` list.

#### [MODIFY] [arinn_core/brain.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/brain.py)
*   `save()`: Serialize expert architectures to `expert_configs.json`.
*   `load()`: Read JSON first, reconstruct `ArinnHivemind` with exact shapes, then load weights.
*   `infer()`: Ensure `model.eval()` is called (and toggled back to `train()` if needed).

## Phase 10: The Apprentice (Proposed)
Focus: Teaching ARINN to comprehend and write Python code through real-world analysis and sandboxed trial-and-error.

### New Modules
#### [NEW] [arinn_core/apprentice.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/apprentice.py)
*   `CodeScraper`: Fetches raw Python code from trusted sources (Standard Lib, Verified Repos) for training data.
*   `SyntaxLearner`: Uses Python's `ast` module to break code into learnable structural patterns (not just text).
*   `CodingDojo`: A Reinforcement Learning loop:
    1.  Agent is given a specific task (e.g., "Sort this list").
    2.  Agent generates code (string).
    3.  `SandboxExecutor` runs it.
    4.  Feedback (Error Trace or Success) is fed back to the Hivemind.

### Enhancements
#### [MODIFY] [arinn_core/continuous_learning.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/continuous_learning.py)
*   Add `loop_coding_practice()`: The dedicated training cycle for The Apprentice.
*   Connects `MetaOptimizer` to tune "Exploration" vs "Exploitation" in code generation.

## Phase 11: Asymmetric Hivemind & Cognitive Depth (Proposed)
Focus: Breaking the symmetry of experts to create specialized thinking styles, "Self-Debate" logic, and evolutionary memory.

### New Modules
#### [NEW] [arinn_core/referee.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/referee.py)
*   `DebateArena`: Manages the internal "debate" between conflicting experts.
*   `RefereeNet`: A specialized meta-network that judges the logical consistency of outputs.

### Enhancements
#### [MODIFY] [arinn_core/hivemind.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/hivemind.py)
*   **Asymmetric Divergence**: Differentiate experts into 5 types (Symbolic, Probabilistic, Critical, Compression, Creative).
*   **Specialized Initialization**: Varies dropout, activation functions, and layer depth per expert type.

#### [MODIFY] [arinn_core/memory.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/memory.py)
*   **Memory Darwinism**: Add `utility_score` and `last_access` to memory records.
*   **Pruning**: Automatically remove low-utility memories when capacity is reached.

#### [MODIFY] [arinn_core/brain.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/brain.py)
*   **Entropy Pressure**: Add a loss term rewarding smaller representations (Compression Expert).

## Phase 12: Acceleration Curriculum (Current)
Focus: Implementing High-Leverage Meta-Cognitive Skills to accelerate future learning.

### New Modules
#### [NEW] [arinn_core/advanced_curriculum.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/advanced_curriculum.py)
* Defines the 10 Acceleration Axioms (Error Analysis, Causal Reasoning, etc.).
* Includes `signals_of_mastery` and `accelerates` impact descriptions.

### Enhancements
#### [MODIFY] [arinn_core/continuous_learning.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/continuous_learning.py)
* Add `loop_acceleration_study()`: Dedicated loop to internalize high-leverage concepts.

#### [NEW] [run_acceleration.py](file:///c:/Users/dmdra/Development/research_agent/run_acceleration.py)
* Launcher script to bypass menus and start studying immediately.

## Phase 13: Autonomous Cognitive Expansion (Planned)
Focus: Self-directing cognitive system (Goal Proposal, Tool Creation, Synthesis).

### New Modules
#### [NEW] [arinn_core/cognitive_expansion.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/cognitive_expansion.py)
* `GoalProposer`: Generates internal learning goals (no external side effects).
* `CognitiveToolCreator`: Invents/evaluates internal operators (e.g. `PatternExtractor`).

#### [NEW] [arinn_core/cross_domain.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/cross_domain.py)
* `SynthesisEngine`: Maps concepts between unrelated domains (Source -> Target).

### Enhancements
#### [MODIFY] [arinn_core/memory.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/memory.py)
* Change `prune_memories` to `deprioritize_memories` (Non-destructive).

#### [MODIFY] [arinn_core/continuous_learning.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/continuous_learning.py)
* Add `loop_autonomous_expansion()`: The main driver for Phase 13.

## Phase 14: Hyper-Efficiency & Cognitive Compression (Planned)
Focus: Metric-driven efficiency, ROI optimization, and knowledge compression.

### New Modules
#### [NEW] [arinn_core/efficiency_engine.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/efficiency_engine.py)
* `CostAccountant`: Tracks ROI (Gain/Cost).
* `CompressionEngine`: Merges concepts and reduces representation size.
* `StrategyOptimizer`: Evolution for learning strategies.

#### [NEW] [arinn_core/representation_manager.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/representation_manager.py)
* `RepresentationController`: Picks cheapest format (Symbolic/Numeric) per problem.

### Enhancements
#### [MODIFY] [arinn_core/memory.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/memory.py)
* Add `heat_map` (temperature) logic (Hot/Cold memories).

#### [MODIFY] [arinn_core/continuous_learning.py](file:///c:/Users/dmdra/Development/research_agent/arinn_core/continuous_learning.py)
* Add `loop_hyper_efficiency()`: Loop focusing on compression and strategy pruning.

## Phase 16: Self-Correcting Instruction Mastery
**Goal**: Enable ARINN to autonomously decompose, verify, and execute complex instructions with self-correction.

### Components
1.  **`arinn_core/instruction_mastery.py`**:
    *   `InstructionDecomposer`: Breaks text into `SubTask` DAG.
    *   `ExecutionDAG`: Manages dependency graph and state.
    *   `FeedbackLoop`: Detects errors (procedural/conceptual) and triggers `re-plan`.
2.  **`arinn_core/consensus.py`**:
    *   `ConsensusManager`: Queries Hivemind Experts for plan validation.
    *   `RefereeArbitration`: Resolves expert conflicts.
3.  **`arinn_core/continuous_learning.py`**:
    *   `loop_instruction_mastery()`: Main loop for receiving and processing instructions.

### Verification Plan
*   **Automated Tests**: `verify_instruction_mastery.py`
    *   Test DAG creation from simple string.
    *   Test Dependency resolution (Task B waits for Task A).
    *   Test Error Correction (Inject failure -> System adapts).
    *   Test Dependency resolution (Task B waits for Task A).
    *   Test Error Correction (Inject failure -> System adapts).
    *   Test Consensus (Simulate expert disagreement -> Referee decides).

## Phase 17: Hyper-Efficient Recursive Learning
**Goal**: Enable exponential self-improvement with user-controlled manual override.

### Components
1.  **`arinn_core/hyper_learning.py`**:
    *   `KnowledgeTracker`: Monitors learning velocity (Concepts/Sec, Error Drop Rate).
    *   `RecursiveOptimizer`: Adjusts learning parameters (LR, Batch Size, Strategy) dynamically.
    *   `ExponentialGrower`: Triggers recursive "Growth Cycles" if velocity is high.
2.  **`arinn_core/continuous_learning.py`**:
    *   `loop_hyper_recursive_learning()`: The main loop.
    *   **Manual Override**: Checks for `manual_override.lock`. If present, pauses recursion.

### Verification Plan
*   **Automated Tests**: `verify_hyper_learning.py`
    *   Test Velocity Tracking.
    *   Test Recursive Parameter Adjustment.
    *   Test Recursive Parameter Adjustment.
    *   Test Manual Lock functionality (Create lock -> System pauses).

## Phase 18: Strategic Multi-Domain Autonomy
**Goal**: Enable ARINN to self-manage multiple domains, innovate cross-connections, and plan strategically.

### Components
1.  **`arinn_core/strategic_autonomy.py`**:
    *   `DomainManager`: Tracks progress in different fields (e.g., "Physics": LVL 5, "Code": LVL 10).
    *   `MetaPlanner`: Uses `InstructionDecomposer` to execute high-level goals like "Master Domain X".
    *   `IdeaSynthesizer`: Combines concepts from different active domains to generate "Novelties".
2.  **`arinn_core/continuous_learning.py`**:
    *   `loop_strategic_autonomy()`: The master loop that acts as the "CEO" of the Hivemind, directing experts to domains.

### Verification Plan
*   **Automated Tests**: `verify_strategic_autonomy.py`
    *   Test Domain Registration & Mastery Tracking.
    *   Test Meta-Plan generation (High-level goal -> Sub-tasks).
    *   Test Meta-Plan generation (High-level goal -> Sub-tasks).
    *   Test Idea Synthesis (Domain A + Domain B -> New Concept).

## Phase 19: Planetary-Scale Autonomous Cognition
**Goal**: Enable massive parallel cognition via multi-agent orchestration and global state sharing.

### Components
1.  **`arinn_core/planetary_brain.py`**:
    *   `PlanetaryMind`: The central authority. Spawns and manages Sub-Agents.
    *   `SubAgent`: Independent worker capable of executing Instruction DAGs (from Phase 16) in parallel threads.
    *   `GlobalState`: Thread-safe shared memory for agents to sync findings.
2.  **`arinn_core/continuous_learning.py`**:
    *   `loop_planetary_cognition()`: Orchestrates the swarm of agents.

### Verification Plan
*   **Automated Tests**: `verify_planetary.py`
    *   Test Sub-Agent spawning.
    *   Test Parallel Task Execution (Agent A does Task 1, Agent B does Task 2).
    *   Test Global State Convergence (Agents share results).
