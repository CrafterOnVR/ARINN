import time
import llm
from .crucible import Crucible # type: ignore

class RoleAgent:
    def __init__(self, name: str, role_prompt: str, temperature: float):
        self.name = name
        self.role_prompt = role_prompt
        self.temperature = temperature
        self.client = llm.LLMClient(enabled=True)

    def speak(self, context: str) -> str:
        prompt = f"{self.role_prompt}\n\nContext:\n{context}\n\nProvide your response based on your role:"
        try:
            resp = self.client._handle_api_call(
                self.client._client.chat.completions.create,
                model=self.client.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"[API Error from {self.name}]: {e}"

class LogicAgent(RoleAgent):
    def __init__(self):
        super().__init__(
            name="Logic Agent",
            role_prompt="You are the Architect. Design the overall solution with strict consistency, mathematical precision, and logical rigor. Avoid unusual connections.",
            temperature=0.1
        )

class CreativeAgent(RoleAgent):
    def __init__(self):
        super().__init__(
            name="Creative Agent",
            role_prompt="You are the Brainstormer. Explore unusual connections, highly optimized workarounds, and alternative hypotheses to solve the problem.",
            temperature=0.8
        )

class CriticAgent(RoleAgent):
    def __init__(self):
        super().__init__(
            name="Critic Agent",
            role_prompt="You are the Adversary. Actively try to break the proposed solution. Force disagreement. Find at least 3 reasons why the provided proposal fails. Be ruthless.",
            temperature=0.2
        )

class DebateCoordinator:
    def __init__(self):
        self.logic = LogicAgent()
        self.creative = CreativeAgent()
        self.critic = CriticAgent()
        self.crucible = Crucible()
        
        # Ensemble accuracy weights
        self.weights = {
            "Logic Agent": 0.5,
            "Creative Agent": 0.5,
            "Critic Agent": 0.5
        }

    def debate_cycle(self, problem: str, rounds: int = 1) -> str:
        print(f"\n[DEBATE ARENA] Initiating multi-agent deliberation on problem: {problem[:50]}...")
        
        # 1. Initial Proposals
        logic_proposal = self.logic.speak(f"Propose a solution to: {problem}")
        creative_proposal = self.creative.speak(f"Propose an outside-the-box solution to: {problem}")
        
        print("[DEBATE ARENA] Logic and Creative Agents have submitted proposals.")
        
        current_best = logic_proposal # Default starting point
        
        for r in range(rounds):
            print(f"\n--- Debate Round {r+1} ---")
            
            # 2. Forced Disagreement
            criticism = self.critic.speak(f"Attack this proposal ruthlessly:\n{current_best}")
            print(f"[Critic]: {criticism[:150]}...")
            
            # 3. Defense
            defense = self.logic.speak(f"Defend your proposal against these criticisms, and fix any real flaws in your code:\nProposal: {current_best}\nCriticism: {criticism}")
            print(f"[Logic Defender]: {defense[:150]}...")
            
            current_best = defense
            time.sleep(1) # Pace API calls
            
        # 4. Sandbox Testing (The Judge)
        print("\n[DEBATE ARENA] Deliberation complete. Pushing to Crucible Sandbox to prove it mathematically.")
        # Extract purely python code block using a quick lambda string parse
        import re
        code_blocks = re.findall(r'```python\n(.*?)```', current_best, re.DOTALL)
        code_to_test = code_blocks[0] if code_blocks else current_best
        
        passed, feedback = self.crucible.verify_code(code_to_test)
        if passed:
            print("[DEBATE ARENA] Crucible verified golden. Proposal survives reality check.")
            # Boost logic weight
            self.weights["Logic Agent"] += 0.1
            return code_to_test
        else:
            print(f"[DEBATE ARENA] Proposal FAILED in sandbox. Reality rejected the idea.\nError: {feedback[:100]}")
            self.weights["Logic Agent"] -= 0.1
            self.weights["Critic Agent"] += 0.1 # Critic was right to attack it
            return f"# SYNTHESIS FAILED\n{feedback}"
