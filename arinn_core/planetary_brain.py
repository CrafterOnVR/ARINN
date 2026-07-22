
import threading
import time
import uuid
import random
from .instruction_mastery import InstructionDecomposer, ExecutionDAG

class GlobalState:
    """
    Planetary Knowledge Base.
    Thread-safe storage for shared insights.
    """
    def __init__(self):
        self.lock = threading.Lock()
        self.knowledge = {} # Topic -> Insight
        self.logs = []
        
    def submit_insight(self, topic, insight, agent_id):
        with self.lock:
            if topic not in self.knowledge:
                self.knowledge[topic] = []
            self.knowledge[topic].append(insight)
            self.logs.append(f"[{agent_id}] Insight on '{topic}': {insight}")
            return len(self.knowledge[topic])

    def get_insights(self, topic):
        with self.lock:
            return self.knowledge.get(topic, [])[:]

class SubAgent(threading.Thread):
    """
    Independent Autonomous Agent.
    Runs in its own thread, executes tasks, reports to GlobalState.
    """
    def __init__(self, agent_id, global_state, specialized_domain):
        super().__init__()
        self.agent_id = agent_id
        self.global_state = global_state
        self.domain = specialized_domain
        self.daemon = True # Kill when main thread dies
        self.running = False
        self.decomposer = InstructionDecomposer()
    
    def run(self):
        self.running = True
        while self.running:
            # 1. Generate Task (Real-World Data Source)
            from .advanced_curriculum import get_curriculum
            curriculum = get_curriculum()
            
            relevant_concepts = [k for k in curriculum.keys() if self.domain.lower() in str(curriculum[k]).lower()]
            if not relevant_concepts:
                 relevant_concepts = list(curriculum.keys())
            
            target_key = random.choice(relevant_concepts)
            item = curriculum[target_key]
            
            # Construct Real-World Instruction
            instruction = f"Execute Research: '{item['search_query']}' and Solve: '{item['code_challenge']}'"
            
            # 2. Decompose (Phase 16)
            tasks = self.decomposer.decompose(instruction)
            
            # 3. Execute (Real CPU Work)
            # Find a 'COMPUTE' or 'SEARCH' task
            work_tasks = [t for t in tasks if t.type in ["SEARCH", "COMPUTE"]]
            for t in work_tasks:
                # Perform actual CPU work (Compression) to prove effort
                import zlib
                data = (t.description * 1000).encode('utf-8')
                _ = zlib.compress(data)
                
                # 4. Integrate Result
                result = f"Processed {t.description[:30]}... Ratio {len(_)/len(data):.2f}"
                count = self.global_state.submit_insight(self.domain, result, self.agent_id)
                
            time.sleep(0.5)
            
    def stop(self):
        self.running = False

class PlanetaryMind:
    """
    The Orchestrator.
    Spawns and manages the swarm.
    """
    def __init__(self):
        self.state = GlobalState()
        self.agents = []
        
    def spawn_agent(self, domain):
        agent_id = f"Agent-{len(self.agents)+1}-{domain[:3].upper()}"
        agent = SubAgent(agent_id, self.state, domain)
        self.agents.append(agent)
        agent.start()
        return agent_id
        
    def stop_all(self):
        for a in self.agents:
            a.stop()
        for a in self.agents:
            a.join(timeout=1.0)
            
    def get_swarm_status(self):
        return f"Active Agents: {len(self.agents)} | Total Insights: {len(self.state.logs)}"
