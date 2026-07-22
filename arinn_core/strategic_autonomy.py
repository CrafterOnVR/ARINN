
import random
import uuid
from .instruction_mastery import InstructionDecomposer, ExecutionDAG

class DomainManager:
    """
    Manages ARINN's "Skill Tree".
    Tracks mastery levels and XP in different domains.
    """
    def __init__(self):
        self.domains = {
            "General": {"level": 1, "xp": 0},
            "Coding": {"level": 0, "xp": 0},
            "Physics": {"level": 0, "xp": 0},
            "Philosophy": {"level": 0, "xp": 0}
        }
        
    def add_xp(self, domain, xp_amount):
        if domain not in self.domains:
            self.domains[domain] = {"level": 0, "xp": 0}
            
        self.domains[domain]["xp"] += xp_amount
        
        # Simple Level Up logic: XP needed = Level * 100
        current_lvl = self.domains[domain]["level"]
        xp_needed = (current_lvl + 1) * 100
        
        if self.domains[domain]["xp"] >= xp_needed:
            self.domains[domain]["level"] += 1
            self.domains[domain]["xp"] -= xp_needed
            return True # Leveled Up
        return False
        
    def get_status(self):
        return {d: f"Lvl {v['level']} ({v['xp']}xp)" for d, v in self.domains.items()}

class MetaPlanner:
    """
    High-level strategic planning.
    Uses Phase 16's Decomposer to execute strategies.
    """
    def __init__(self):
        self.decomposer = InstructionDecomposer()
        self.active_strategies = []
        
    def create_strategy(self, goal_domain, target_level):
        """
        Generates a learning plan to reach a target level in a domain.
        """
        strategy_id = str(uuid.uuid4())[:8]
        
        # Heuristic Strategy Generation
        # "Master Physics" -> "Search fundamentals", "Study Axioms", "Compute problems"
        instruction = f"Study {goal_domain} fundamentals and Solve problems"
        
        tasks = self.decomposer.decompose(instruction)
        dag = ExecutionDAG(tasks)
        
        strategy = {
            "id": strategy_id,
            "goal": f"Reach {goal_domain} Lvl {target_level}",
            "dag": dag,
            "status": "IP" # In Progress
        }
        self.active_strategies.append(strategy)
        return strategy

class IdeaSynthesizer:
    """
    Cross-Pollination Engine.
    Combines concepts from random active domains to suggest new research.
    """
    def __init__(self, domain_mgr):
        self.domain_mgr = domain_mgr
        
    def synthesize(self):
        """
        Picks two domains with >0 level and attempts to merge them.
        """
        active_domains = [d for d, v in self.domain_mgr.domains.items() if v['level'] > 0]
        
        if len(active_domains) < 2:
            return None # Not enough knowledge to synthesize
            
        d1, d2 = random.sample(active_domains, 2)
        
        # In a real system, this would use embeddings to find intersections.
        # Here we generate a prompt/hypothesis.
        hypothesis = f"Does {d1} offer optimization heuristics for {d2}?"
        confidence = (self.domain_mgr.domains[d1]['level'] + self.domain_mgr.domains[d2]['level']) / 20.0
        
        return {
            "source_a": d1,
            "source_b": d2,
            "hypothesis": hypothesis,
            "estimated_value": min(1.0, confidence)
        }
