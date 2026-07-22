# ARINN Linux Migration State

Welcome to the new environment. If you are reading this, the user has migrated ARINN from Windows to Linux.

## Current State of the Project (Phase 83 - The Toolmaker)

We just finished implementing **Phase 84: The Autoresearch Protocol**. This successfully integrated Karpathy's `autoresearch` repo (`train.py`) with our `NeuralCore`. We created `arinn_core/autoresearch_agent.py` and `verify_autoresearch.py` which successfully reads `train.py`, allows Mistral-Nemo to propose edits (like modifying the learning rate), and commits the change.

However, before we start the *actual* overnight PyTorch training loop, we paused to finish **Phase 83: The Toolmaker**.

## Phase 83: The Toolmaker (In Progress)

### What is Phase 83?
Phase 83 is about giving ARINN the ability to dynamically write, test, and hot-load new Python tools into its own memory space without restarting. This is the "Self-Extending Codebase" phase.

### Current Status of Phase 83:
1.  **Written**: `arinn_core/toolmaker.py` (Contains `ToolGenerator`, `ToolSandbox`, and `DynamicToolRegistry`).
2.  **Written**: `verify_toolmaker.py`.
3.  **Issue (Before Migration)**: We were getting Out-Of-Memory (OOM) errors on the Windows machine when trying to run the Toolmaker because loading Mistral-Nemo-12B inside the verifier competed with the OS. We tweaked `config_optimized.yaml` (`n_ctx` down to 2048, `n_threads` to 4) and managed to get it to pass!
4.  **Pending Goal**: The user has just migrated to Linux. We need to run `verify_toolmaker.py` in the new Linux environment to ensure the dynamic generation, execution, and hot-importing of the "fibonacci" test tool still works on this new OS.

## Immediate Next Steps (For the New AI Instance)

1.  **Verify Environment**: Ensure `llama-cpp-python` is compiled with CUDA support on this Linux machine so Mistral-Nemo doesn't run on the CPU.
    - If Step 2 runs incredibly slowly, the culprit is likely a missing CUDA build. You may need to run: `CMAKE_ARGS="-DLLAMA_CUDA=on" pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir`
2.  **Verify Toolmaker**: Run `python verify_toolmaker.py`.
    - If it OOMs or fails, troubleshoot the context size in `config_optimized.yaml` or the code extraction logic block in `toolmaker.py`.
    - If it succeeds, Phase 83 is complete!
3.  **Complete the Orchestrator loop**: Hook up the Toolmaker to `genesis.py` so ARINN automatically writes a tool when it hits a missing dependency.
4.  **Prepare Autoresearch Data**: Run `uv run prepare.py` inside `autoresearch-master/autoresearch-master` to download the Shakespeare dataset.
5.  **Kick off Autoresearch (Phase 84)**: Run the execution loop!

## Key Files to Check
- `task.md`, `implementation_plan.md`, `features.md`, `walkthrough.md` (These contain the full truth of all 84 phases. I have copied them into the root `research_agent/` directory for easy access on Linux).
- `arinn_core/toolmaker.py`
- `verify_toolmaker.py`
- `config_optimized.yaml`
