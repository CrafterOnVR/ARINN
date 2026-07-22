import os
import json
import time

class DatasetSynthesizer:
    """
    Phase 10: The STaR Reasoner.
    Formats successful Swarm operations into instruction-tuning datasets.
    """
    def __init__(self, output_dir=None):
        if output_dir is None:
            # Default to project root / data / synthetic_datasets
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            self.output_dir = os.path.join(project_root, "data", "synthetic_datasets")
        else:
            self.output_dir = output_dir
            
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        # Create a new dataset file based on the date
        date_str = time.strftime("%Y-%m-%d")
        self.dataset_file = os.path.join(self.output_dir, f"arinn_training_data_{date_str}.jsonl")

    def synthesize_success(self, goal: str, reasoning_trace: str, optimized_code: str):
        """
        Formats a successful AST mutation / Swarm cycle into a ChatML / Instruct format
        suitable for fine-tuning LLMs (like Qwen or Llama).
        """
        # Using a standard system/user/assistant format
        data_point = {
            "messages": [
                {"role": "system", "content": "You are ARINN, a highly advanced autonomous AI specializing in highly optimized Python code."},
                {"role": "user", "content": f"Task: {goal}\nWrite an optimized Python script for this task. Before writing the code, explain your mathematical or logical reasoning."},
                {"role": "assistant", "content": f"<reasoning>\n{reasoning_trace}\n</reasoning>\n\n```python\n{optimized_code}\n```"}
            ]
        }
        
        with open(self.dataset_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(data_point) + "\n")
            
        print(f"[Synthesizer] Successfully recorded 1 new STaR training sample to {self.dataset_file}")
        return self.dataset_file

    def get_latest_dataset(self):
        """Returns the path to today's dataset file, if it exists."""
        if os.path.exists(self.dataset_file):
            return self.dataset_file
        return None
