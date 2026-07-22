
from .brain import ArinnBrain
from .memory import SecureMemory
from .bootloader import Bootloader, Phase

class ArinnIdentity:
    def __init__(self):
        self.brain = ArinnBrain()
        self.memory = SecureMemory()
        self.bootloader = Bootloader(self.brain, self.memory)
        self.name = "ARINN"

    def wake_up(self):
        """The main entry point for the growing identity."""
        if self.bootloader.current_phase != Phase.AUTONOMOUS_SCHOLAR:
            print("[ARINN] System in growth mode.")
            self.bootloader.process_growth()
            return False # Not ready for full work
        
        print(f"[ARINN] Identity Active: {self.name}. Fully Operational.")
        return True

    def explain_decision(self, decision, mastery, context=None):
        """Generates a human-readable explanation for a decision."""
        explanation = f"[Reasoning Trace]\n"
        explanation += f"  - Current Mastery: {mastery:.1%}\n"
        
        if decision == "MOVE_TO_NEW_TOPIC":
            if mastery >= 0.90:
                explanation += "  - Logic: Mastery > 90% (Diminishing Returns Threshold).\n"
                explanation += "  - Conclusion: Topic exhausted. Efficient usage of time dictates moving to new territory."
            else: # 80-90 range
                explanation += "  - Logic: Mastery > 80% (Competency Threshold).\n"
                explanation += "  - Random Factor: Rolled > 0.5 (Exploration Bias).\n"
                explanation += "  - Conclusion: Sufficient competency achieved. Opting to explore breadth over depth."
        elif decision == "DEEP_DIVE":
            if mastery < 0.80:
                explanation += "  - Logic: Mastery < 80% (Learning Gap).\n"
                explanation += "  - Conclusion: Knowledge insufficient. Continued study required to reach competency."
            else:
                explanation += "  - Logic: Mastery > 80% (Competency Threshold).\n"
                explanation += "  - Random Factor: Rolled <= 0.5 (Perfection Bias).\n"
                explanation += "  - Conclusion: Competent, but choosing to refine knowledge towards expertise."
        
        return explanation

    def autonomous_choice(self, current_topic_mastery: float):
        """Decides next action based on 80/90 rule with explanation."""
        decision = "DEEP_DIVE"
        
        if current_topic_mastery >= 0.90:
            decision = "MOVE_TO_NEW_TOPIC"
        elif current_topic_mastery >= 0.80:
             # Random chance to perfect it or move on
             import random
             if random.random() > 0.5:
                 decision = "MOVE_TO_NEW_TOPIC"
             else:
                 decision = "DEEP_DIVE"
        else:
            decision = "DEEP_DIVE"
            
        print(self.explain_decision(decision, current_topic_mastery))
        return decision
