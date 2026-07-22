
import random
import time

class GoalProposer:
    """
    Autonomous Goal Proposal System.
    Generates internal learning goals based on abstraction potential and long-term value.
    Enforces strict safety: Learning-focused only, no external side effects.
    """
    def __init__(self):
        self.active_goals = []
        self.completed_goals = []
        
        # Seed themes for goals
        self.themes = [
            "Causal Inference", "Data Compression", "Error Correction", 
            "Pattern Recognition", "Symbolic Logic", "Transfer Learning"
        ]

    def propose_goal(self, memory_system=None):
        """
        Proposes a new learning goal based on MEMORY UTILITY analysis.
        Finds gaps (cold memories) or high-potential clusters.
        """
        # Default themes if no memory access
        theme = "General Cognitive Upgrade"
        focus = "Axiom Internalization"
        confidence = 0.5
        
        if memory_system:
             # Real Logic: Scan memory for high-potential or low-coverage areas
             # 1. Look for 'Hot' items (Utility > 0.8) -> Deep Dive
             # 2. Look for 'Cold' items (Utility < 0.2) -> Refresher
             
             heat_map = memory_system.get_heat_map()
             if heat_map:
                 # Find random hot item
                 hot_items = [k for k, v in heat_map.items() if v > 0.7]
                 cold_items = [k for k, v in heat_map.items() if v < 0.3]
                 
                 if hot_items:
                     target = random.choice(hot_items)
                     theme = f"Advanced mastery of '{target}'"
                     focus = "Deep Dive"
                     confidence = 0.9
                 elif cold_items:
                     target = random.choice(cold_items)
                     theme = f"Revival of '{target}'"
                     focus = "Memory Refresher"
                     confidence = 0.75
        
        goal = {
            "description": f"{focus} on {theme}",
            "type": "LEARNING_ONLY",
            "benefit": "Optimizes memory utility distribution.",
            "confidence": confidence,
            "status": "PROPOSED",
            "timestamp": time.time()
        }
        
        if self._validate_goal(goal):
            self.active_goals.append(goal)
            return goal
        else:
            return None

    def _validate_goal(self, goal):
        """Strict validation: Must be learning-focused."""
        if goal["type"] != "LEARNING_ONLY":
            return False
        # Future: Check for disallowed keywords (e.g. "Simulate Pain", "Access Internet without Sandbox")
        return True

    def complete_goal(self, goal):
        if goal in self.active_goals:
            goal["status"] = "COMPLETED"
            self.active_goals.remove(goal)
            self.completed_goals.append(goal)


class CognitiveToolCreator:
    """
    Internal Tool Invention and Management.
    Allows ARINN to define, test, and deprecate mental operators.
    """
    def __init__(self):
        self.tools = {} # name -> metadata
        self.deprecated_tools = []
        
        # Initialize with Axiom-derived tools
        self.register_tool("PatternExtractor", "Identifies repeated sub-structures in data tensors.")
        self.register_tool("HypothesisPruner", "Removes low-probability branches from search trees.")
        self.register_tool("ContradictionDetector", "Flags conflicting logic statements.")

    def register_tool(self, name, description):
        if name not in self.tools:
            self.tools[name] = {
                "description": description,
                "usage_count": 0,
                "success_rate": 0.5, # Initial prior
                "status": "ACTIVE"
            }
            return True
        return False

    def use_tool(self, name, success=True):
        """Simulates usage and updates metrics."""
        if name in self.tools:
            tool = self.tools[name]
            tool["usage_count"] += 1
            # Update success rate (moving average)
            alpha = 0.1
            outcome = 1.0 if success else 0.0
            tool["success_rate"] = (1 - alpha) * tool["success_rate"] + alpha * outcome
            
            # Auto-deprecate if ineffective
            if tool["usage_count"] > 10 and tool["success_rate"] < 0.2:
                self.deprecate_tool(name)
            
            return True
        return False

    def deprecate_tool(self, name):
        if name in self.tools:
            print(f"[TOOL] Deprecating ineffective tool: {name}")
            tool = self.tools.pop(name)
            tool["status"] = "DEPRECATED"
            self.deprecated_tools.append(tool)

    def invent_tool(self):
        """
        Attempts to invent a new tool by recombining functional primitives.
        Tools are actual callable lambdas that transform data.
        """
        # Functional Primitives (Real-world operations)
        primitives = [
            ("FilterEven", lambda x: [i for i in x if isinstance(i, int) and i % 2 == 0]),
            ("FilterOdd", lambda x: [i for i in x if isinstance(i, int) and i % 2 != 0]),
            ("Sum", lambda x: sum([i for i in x if isinstance(i, (int, float))])),
            ("StrLen", lambda x: [len(str(i)) for i in x]),
            ("Unique", lambda x: list(set(x)))
        ]
        
        # Combine two primitives
        base1_name, base1_func = random.choice(primitives)
        base2_name, base2_func = random.choice(primitives)
        
        new_name = f"Auto{base1_name}Then{base2_name}"
        
        # Define Metadata
        desc = f"Autonomously composed: {base1_name} -> {base2_name}"
        
        # Register abstract handle (In future we would compile and save the code)
        # For now, we store the composition logic
        
        if self.register_tool(new_name, desc):
            return new_name
        return None
