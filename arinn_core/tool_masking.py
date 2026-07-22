class FSMToolMasker:
    """
    Vault 10: Just-In-Time (JIT) Tool Activation (Prompt De-Bloating)
    Implements a Finite State Machine (FSM) to mask tools from the AI context.
    If the agent is in the 'RESEARCH' state, it mathematically cannot see the 
    'EXECUTE_CODE' tool, preventing hallucinatory API calls.
    """
    def __init__(self):
        self.state = "INIT"
        # Mapping of State -> Allowed Tools
        self.fsm_rules = {
            "INIT": ["ping_system", "read_goal"],
            "RESEARCH": ["web_search", "read_file", "list_dir"],
            "ARCHITECT": ["write_file", "generate_ast", "compile_tool"],
            "OPTIMIZE": ["fuzz_ast", "benchmark_speed", "run_sandbox"],
            "FINALIZE": ["commit_memory", "snapshot_state"]
        }
        
    def transition(self, new_state: str):
        if new_state in self.fsm_rules:
            print(f"[VAULT-10] FSM State Transition: {self.state} -> {new_state}")
            self.state = new_state
        else:
            print(f"[VAULT-10] Invalid FSM State Transition: {new_state}")
            
    def get_active_tools(self):
        """
        Returns only the tools legally allowed in the current FSM state.
        By de-bloating the prompt, we prevent the LLM from hallucinating 
        complex tools when it should just be searching the web.
        """
        allowed = self.fsm_rules.get(self.state, [])
        print(f"[VAULT-10] Active State: {self.state} | JIT Tools Unlocked: {len(allowed)}")
        return allowed
        
    def mask_prompt(self, base_prompt: str):
        """
        Appends the strict subset of tools to the prompt.
        """
        tools = self.get_active_tools()
        mask_text = f"\n[FSM MASK ACTIVE] You are restricted to the following tools: {', '.join(tools)}\n"
        return base_prompt + mask_text
