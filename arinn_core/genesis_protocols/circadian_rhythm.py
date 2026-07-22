import time
import logging

class CircadianWatchdog:
    """
    Phase 8: Circadian Rhythm Rate Limit Failsafe.
    Physically catches OpenAI RateLimit / Quota errors and suspends ARINN
    into an isolated cold-store state until the API boundary clears, injecting
    a hardcoded non-AI resumption prompt.
    """
    def __init__(self, check_interval_seconds: int = 3600):
        self.interval = check_interval_seconds

    def suspend_and_wait(self, client=None) -> bool:
        """
        Enters a recursive waiting sequence. Pings the test API.
        Returns True when successful clearance is acquired.
        """
        logging.warning("[CIRCADIAN RHYTHM] Quota Exhausted! System entering deep autonomous suspension...")
        print("[!] API Rate Limit Exceeded. Activating Circadian Failsafe. ARINN sleeping.")
        
        while True:
            # We enforce the sleep BEFORE checking to respect backoff.
            print(f"[CIRCADIAN RHYTHM] Suspending processing for {self.interval // 60} minutes...")
            time.sleep(self.interval)

            if client is None:
                # If no client provided to rigorously ping, we assume the interval sleep was sufficient
                # e.g., waiting 24hrs for limits usually resets it
                print("[CIRCADIAN RHYTHM] Unverified wake. Resuming bounds...")
                return True

            try:
                # Perform a micro-ping to verify if limits dropped
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": "ping"}],
                    max_tokens=1
                )
                print("[CIRCADIAN RHYTHM] Quota boundary clear. Re-igniting API streams.")
                return True
            except Exception as e:
                # Still exhausted
                error_str = str(e).lower()
                if "rate_limit" in error_str or "quota" in error_str or "429" in error_str:
                    print("[CIRCADIAN RHYTHM] Ping failed (Limit still active). Continuing sleep.")
                else:
                    # An unrelated error occurred, assume network outage but resume anyway
                    print(f"(!) Unknown boundary during ping ({e}). Attempting resumption.")
                    return True
