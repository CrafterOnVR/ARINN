import os
from arinn_core.autoresearch_agent import AutoresearchAgent  # type: ignore

def test_autoresearch():
    print("[VERIFY] Initializing Autoresearch Agent...")
    repo_path = os.path.join(os.path.dirname(__file__), "autoresearch-master", "autoresearch-master")
    
    # Check if the repo exists
    if not os.path.exists(repo_path):
        print(f"[VERIFY] ERROR: Autoresearch repo not found at {repo_path}")
        return False
        
    agent = AutoresearchAgent(repo_dir=repo_path)
    
    # We will test the initialization and a mock "propose_changes" safely 
    # without actually running a 5 minute training budget for verification purposes.
    
    success = agent.initialize_experiment(tag="test_verify")
    if not success:
        return False
        
    print(f"[VERIFY] Branch created: {agent.current_branch}")
    
    mock_code = "def train():\n    pass\n"
    new_code, desc = agent.propose_changes(mock_code, "No previous history.")
    
    if new_code:
        print("[VERIFY] NeuralCore successfully proposed a code modification.")
        print(f"[VERIFY] Description: {desc}")
        print("[VERIFY] Code snippet snippet length: ", len(new_code))
        
        # Cleanup test branch
        import subprocess
        subprocess.run(["git", "checkout", "master"], cwd=repo_path, capture_output=True)
        subprocess.run(["git", "branch", "-D", "autoresearch/test_verify"], cwd=repo_path, capture_output=True)
        print("[VERIFY] Test branch cleaned up.")
        print("[VERIFY] SUCCESS: Phase 84 (Autoresearch) integration verified.")
        return True
    else:
        print("[VERIFY] FAIL: Failed to extract code from NeuralCore output.")
        return False

if __name__ == "__main__":
    test_autoresearch()
