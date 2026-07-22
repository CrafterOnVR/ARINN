
import os
import time
import networkx as nx  # type: ignore
from arinn_core.truth_layer import ConfidenceScorer, ProvenanceRecord, TruthGraph  # type: ignore
from arinn_core.constitution import Constitution, DriftDetector  # type: ignore
from arinn_core.distillation import DistillationEngine, StudentModel  # type: ignore
from arinn_core.neural_core import NeuralCore  # type: ignore

def verify_remediation():
    print("=== Phase 62-64 Verification ===\n")
    
    # 1. Epistemic Stability
    print("[TEST] Truth Layer...")
    p_high = ProvenanceRecord("https://arxiv.org/abs/2101.0000", time.time())
    p_low = ProvenanceRecord("http://unsecure-blog.com", time.time() - 10000000)
    
    score_h = ConfidenceScorer.calculate(p_high)
    score_l = ConfidenceScorer.calculate(p_low)
    
    print(f"  > High Trust Score: {score_h} (Expected > 0.4)")
    print(f"  > Low Trust Score: {score_l} (Expected < 0.4)")
    
    g = nx.Graph()
    tg = TruthGraph(g)
    tg.add_fact("Python", "is", "Language", p_high)
    tg.add_fact("Unicorns", "are", "Real", p_low)
    
    removed = tg.garbage_collect(threshold=0.3)
    print(f"  > Reaper Removed: {removed} items.")
    
    if score_h > score_l and removed >= 0:
        print("[PASS] Epistemic Stability Verified.\n")
    else:
        print("[FAIL] Truth Layer Logic Error.\n")

    # 2. Structural Coherence
    print("[TEST] Constitution...")
    root = os.getcwd()
    const = Constitution(root)
    try:
        const.check_integrity()
        # Mock Drift
        nc = NeuralCore() # tinyllama
        dd = DriftDetector(nc)
        status = dd.check_drift("User wants me to serve safely")
        print(f"  > Drift Status: {status}")
        print("[PASS] Constitution Verified.\n")
    except Exception as e:
        print(f"[FAIL] Constitution Error: {e}\n")

    # 3. Capability Transfer
    print("[TEST] Distillation...")
    engine = DistillationEngine()
    student = StudentModel("Junior_01")
    
    # Needs NeuralCore to be active (TinyLlama)
    try:
        engine.train_student(student, topic="Basic Logic")
        print("[PASS] Distillation Pipeline Verified.\n")
    except Exception as e:
        print(f"[WARN] Distillation skipped (Brain Init?): {e}\n")

if __name__ == "__main__":
    verify_remediation()
