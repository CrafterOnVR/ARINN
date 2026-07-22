"""
ARINN Autoresearch Launcher.
Runs the agent orchestration loop with system Python,
while train_amd.py runs in .venv312 for DirectML GPU support.
"""
import os
import sys

# Ensure arinn_core is importable
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from arinn_core.autoresearch_agent import AutoresearchAgent  # type: ignore

repo_dir = os.path.join(project_root, "autoresearch-master", "autoresearch-master")

print(f"[LAUNCHER] Repo: {repo_dir}")
print(f"[LAUNCHER] Starting Autoresearch Overnight Optimization Loop...")
print(f"[LAUNCHER] Press Ctrl+C to abort.\n")

try:
    agent = AutoresearchAgent(repo_dir=repo_dir)
    agent.execution_loop(max_iterations=20)
except KeyboardInterrupt:
    print("\n[LAUNCHER] Shutdown.")
