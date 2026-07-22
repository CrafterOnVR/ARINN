import os
import sys

project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from arinn_core.continuous_learning import ContinuousLearner
from super_enhanced_agent import SuperEnhancedResearchAgent
from run_initialize import CURRICULUM, EXAM_HOURS

def retry_exam():
    print("Initializing Agent and Learner for Final Exam Retake...")
    agent = SuperEnhancedResearchAgent(
        data_dir="data",
        use_llm=True,
        enable_super_intelligence=True
    )
    learner = ContinuousLearner(identity=agent.identity) if hasattr(agent, 'identity') else ContinuousLearner(identity=lambda: None)
    
    print("\nTriggering the True Offline Final Exam...")
    learner.loop_final_exam(topics=CURRICULUM, exam_seconds=EXAM_HOURS * 3600)

if __name__ == "__main__":
    retry_exam()
