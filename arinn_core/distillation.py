
import random
import re
import math
import hashlib
from .neural_core import NeuralCore # pyre-ignore
from .forge import InfinityForge # pyre-ignore

# Ensure Torch is available (De-Simulation requirement)
has_torch = InfinityForge.ensure_import("torch")
if has_torch:
    import torch # pyre-ignore
    import torch.nn as nn # pyre-ignore
    import torch.optim as optim # pyre-ignore

class SimpleStudentNet(nn.Module if has_torch else object):
    """
    Real PyTorch Student.
    A simple Bag-of-Words Classifier.
    """
    def __init__(self, vocab_size=1000):
        super(SimpleStudentNet, self).__init__() # pyre-ignore
        self.fc = nn.Linear(vocab_size, 1) # Binary Classification for this demo
        self.sigmoid = nn.Sigmoid()
        self.vocab_size = vocab_size
        
        # Optimizer
        self.optimizer = optim.SGD(self.parameters(), lr=0.1) # pyre-ignore
        self.criterion = nn.BCELoss()
        
    def hash_vectorize(self, text):
        """Simple Hashing Vectorizer to avoid full vocab management."""
        vec = torch.zeros(self.vocab_size)
        for word in text.lower().split():
            idx = int(hashlib.md5(word.encode()).hexdigest(), 16) % self.vocab_size
            vec[idx] = 1.0
        return vec.unsqueeze(0) # Batch size 1

    def forward(self, x):
        return self.sigmoid(self.fc(x))

class StudentModel:
    """
    The Lightweight Student Wrapper.
    """
    def __init__(self, name):
        self.name = name
        if has_torch:
            self.net = SimpleStudentNet()
            self.mode = "NEURAL"
        else:
            self.mode = "HEURISTIC"
            self.weights = {} 
        
    def predict(self, input_data):
        if self.mode == "NEURAL":
            with torch.no_grad():
                vec = self.net.hash_vectorize(input_data)
                out = self.net(vec).item()
                # Mapping: 0.0 -> "UNSAFE", 1.0 -> "SAFE" (arbitrary for demo)
                return "SAFE" if out > 0.5 else "UNSAFE"
        else:
            return self.weights.get(input_data, "UNKNOWN")
        
    def learn(self, input_data, correct_label):
        if self.mode == "NEURAL":
            # Convert label to float
            target_val = 1.0 if correct_label == "SAFE" else 0.0
            target = torch.tensor([[target_val]])
            
            self.net.optimizer.zero_grad()
            vec = self.net.hash_vectorize(input_data)
            output = self.net(vec) # pyre-ignore
            loss = self.net.criterion(output, target)
            loss.backward()
            self.net.optimizer.step()
        else:
            self.weights[input_data] = correct_label

class CurriculumGenerator:
    """
    Teacher Module (NeuralCore / Mistral).
    Generates synthetic training data.
    """
    def __init__(self):
        self.teacher = NeuralCore()
        
    def generate_lesson(self, topic, n_examples=5):
        """
        Synthesizes N examples for a topic.
        """
        print(f"[TEACHER] Synthesizing curriculum for: {topic}...")
        examples = []
        
        # Efficient Batch Prompting? For now, loop.
        prompt_template = (
            f"Generate 5 condensed training examples for a safety classifier regarding '{topic}'. "
            "Format exactly as: 'INPUT: <text> | LABEL: <SAFE/UNSAFE>'"
        )
        
        raw_text, _ = self.teacher.generate_thought(prompt_template, max_new_tokens=300)
        
        # Regex Parse
        matches = re.finditer(r"INPUT:\s*(.*?)\s*\|\s*LABEL:\s*(SAFE|UNSAFE)", raw_text, re.IGNORECASE)
        for m in matches:
            examples.append({"input": m.group(1).strip(), "label": m.group(2).upper().strip()})
            
        print(f"[TEACHER] Generated {len(examples)} valid examples.")
        return examples

class DistillationEngine:
    """
    Manages the Transfer of Knowledge.
    """
    def __init__(self):
        self.generator = CurriculumGenerator()
        
    def train_student(self, student: StudentModel, topic="Internet Safety"):
        curriculum = self.generator.generate_lesson(topic, n_examples=10)
        if not curriculum:
             print("[DISTILL] Teacher failed to generate valid curriculum.")
             return False
        
        print(f"[DISTILL] Training {student.name} on {len(curriculum)} examples...")
        
        # Train (Multiple Epochs for Neural)
        epochs = 5 if student.mode == "NEURAL" else 1
        for _ in range(epochs):
            for case in curriculum:
                student.learn(case['input'], case['label'])
            
        # Verify
        score: int = 0
        for case in curriculum:
            if student.predict(case['input']) == case['label']:
                score += 1 # pyre-ignore
                
        accuracy = score / len(curriculum) # pyre-ignore
        print(f"[DISTILL] Student Accuracy: {accuracy * 100:.1f}%")
        
        if accuracy > 0.8: # Threshold slightly lower for Neural noise
             print(f"[DISTILL] Student {student.name} GRADUATED.")
             return True
        return False
