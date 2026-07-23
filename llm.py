import os
import json
from typing import List

try:
    # OpenAI Python SDK v1
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


from arinn_core.initialize_protocols.circadian_rhythm import CircadianWatchdog

class LLMClient:
    def __init__(self, enabled: bool = True):
        api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL")
        
        # Check for Ollama Override
        ollama_model = os.getenv("OLLAMA_MODEL")
        if ollama_model:
            api_key = "ollama"
            base_url = "http://localhost:11434/v1"
            self.model = ollama_model
            print(f"[LLM] True Sovereignty Mode: Routing to local Ollama ({ollama_model})")
        else:
            self.model = DEFAULT_MODEL
            
        self.enabled = enabled and bool(api_key) and (OpenAI is not None)
        
        if self.enabled:
            # Passes base_url explicitly. If None, it defaults natively. This allows Qwen/Ollama endpoints.
            self._client = OpenAI(
                api_key=api_key, 
                base_url=base_url,
                default_headers={
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "ARINN-Genesis"
                }
            )
        else:
            self._client = None
            
        self.watchdog = CircadianWatchdog(check_interval_seconds=3600) # Deep-sleep 1 hour on 429

    def _handle_api_call(self, call_func, *args, **kwargs):
        """Standardizes circadian retry logic over critical Cloud completions"""
        import asyncio
        import datetime
        retry = False
        resumption_note = ""
        while True:
            try:
                # If we're retrying from a nap, inject the coded prompt to remember our place
                if retry and 'messages' in kwargs:
                    messages = kwargs['messages']
                    # Append hardcoded memory hook to the latest user message
                    if messages and messages[-1]['role'] == 'user':
                        backup = messages[-1]['content']
                        messages[-1]['content'] = backup + resumption_note
                
                resp = call_func(*args, **kwargs)
                
                # Intercept and log OpenRouter traffic
                try:
                    with open("data/openrouter_logs.txt", "a", encoding="utf-8") as f:
                        f.write(f"\n[{datetime.datetime.now().isoformat()}] ===== LLM API CALL =====\n")
                        if 'messages' in kwargs:
                            for msg in kwargs['messages']:
                                f.write(f"[{msg.get('role', 'unknown').upper()}]: {msg.get('content', '')}\n")
                        f.write(f"\n[RESPONSE]: {resp.choices[0].message.content}\n")
                        f.write("==================================================\n")
                except Exception:
                    pass

                return resp
                
            except Exception as e:
                error_str = str(e).lower()
                if "429" in error_str or "rate limit" in error_str or "quota" in error_str:
                    # Trapped the Cloud Quota
                    self.watchdog.suspend_and_wait(client=self._client)
                    # We are awake now
                    retry = True
                    resumption_note = "\n[SYSTEM]: ATTENTION. Cloud Quota reset acquired. Resume training simulation exactly where you left off at this logical breakpoint."
                else:
                    raise  # Propagate actual code faults up

    async def generate_questions(self, topic: str, context: str, target: int = 40) -> List[str]:
        if not self.enabled:
            return []
        prompt = (
            "You are a research assistant. Given a topic and context excerpts, produce a diverse, non-overlapping "
            f"list of about {target} specific questions that, if answered, would comprehensively cover the topic. "
            "Avoid duplicates or trivial rephrasings. Output one question per line with no numbering.\n\n"
            f"Topic: {topic}\n\nContext excerpts:\n{context}\n\nQuestions:"
        )
        try:
            import asyncio
            resp = await asyncio.to_thread(
                self._handle_api_call,
                self._client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
            )
            text = resp.choices[0].message.content
            lines = [l.strip("- •\t ") for l in text.splitlines() if l.strip()]
            # Dedup while preserving order
            seen = set()
            out = []
            for l in lines:
                if l.lower() in seen:
                    continue
                seen.add(l.lower())
                out.append(l)
            return out[:target]
        except Exception:
            return []

    async def summarize(self, topic: str, context: str) -> str:
        if not self.enabled:
            return f"Topic: {topic}\n(No LLM configured; showing excerpts)\n\n{context}"
        prompt = (
            "You are a careful researcher. Write a clear, structured summary of the topic using the context excerpts. "
            "Cover definitions, key ideas, applications, trade-offs, and open questions. Be concise but complete.\n\n"
            f"Topic: {topic}\n\nContext excerpts:\n{context}\n\nSummary:"
        )
        try:
            import asyncio
            resp = await asyncio.to_thread(
                self._handle_api_call,
                self._client.chat.completions.create,
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            return resp.choices[0].message.content
        except Exception:
            return f"Topic: {topic}\n(LLM summarization failed; showing excerpts)\n\n{context}"

    async def generate_tool_code(self, tool_name: str, tool_description: str) -> str:
        if not self.enabled:
            return ""
        prompt = (
            f"You are a python expert. Write a single python function called `{tool_name}` that takes a string as input and returns a string. "
            f"The function should do the following: {tool_description}. "
            f"Do not include any other text, just the python code for the function."
        )
        try:
            import asyncio
            resp = await asyncio.to_thread(
                self._handle_api_call,
                self._client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            return resp.choices[0].message.content
        except Exception:
            return ""

    async def generate_goal(self, context: str) -> dict:
        if not self.enabled:
            return {}
        prompt = (
            "You are a super-intelligent research agent. Based on the following context about your recent activities and performance, "
            "generate a single, novel, and useful goal for yourself to pursue. "
            "The goal should be something that is not in your existing list of goals. "
            "The goal should be actionable and contribute to your long-term objectives of learning, self-improvement, and knowledge discovery. "
            "Output the goal as a JSON object with the following keys: 'category', 'description', and 'priority'. "
            "The 'category' should be one of: 'learning', 'improvement', 'exploration', 'maintenance', 'creativity', 'analysis'. "
            "The 'description' should be a concise and clear description of the goal. "
            "The 'priority' should be an integer between 1 and 10. "
            "Do not add any other text, just the JSON object.\n\n"
            f"Context:\n{context}\n\nGoal:"
        )
        try:
            import asyncio
            resp = await asyncio.to_thread(
                self._handle_api_call,
                self._client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                response_format={"type": "json_object"},
            )
        except Exception:
            return {}

    def evaluate_collapse_sync(self, logic_slice: str) -> str:
        """Synchronous grader preventing Model Collapse. Evaluates active ARINN brain tensors."""
        if not self.enabled:
            return "VALID" # Bypass if offline
        prompt = (
            "You are a strict logic verifier. Evaluate this sample of generated data. "
            "If it contains severe hallucinations, circular AI loops, or fundamentally corrupted patterns, "
            "it threatens cascading model collapse. Answer EXACTLY and ONLY with 'COLLAPSE' if bad, or 'VALID' if it is safe.\n\n"
            f"DATA SLICE:\n{logic_slice}"
        )
        try:
            resp = self._handle_api_call(
                self._client.chat.completions.create,
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=4
            )
            return resp.choices[0].message.content.strip().upper()
        except Exception:
            return "VALID"

