import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class CircuitBreakerException(Exception):
    pass

class AgentGuardrail:
    def __init__(self, max_budget_usd: float = 0.05, max_turns: int = 5):
        self.max_budget = max_budget_usd
        self.max_turns = max_turns
        self.turns_count = 0

    def inspect_turn(self):
        self.turns_count += 1
        if self.turns_count > self.max_turns:
            raise CircuitBreakerException("Loop Circuit Breaker: Max allowable agent steps reached.")

    def sanitize_input(self, user_input: str) -> str:
        prohibited = ["rm -rf", "DROP TABLE", "ignore previous instructions"]
        for phrase in prohibited:
            if phrase.lower() in user_input.lower():
                raise ValueError(f"Security Alert: Blocked phrase detected: '{phrase}'")
        return user_input

if __name__ == "__main__":
    guard = AgentGuardrail(max_turns=3)
    
    try:
        clean_prompt = guard.sanitize_input("Please summarize the documentation.")
        for step in range(5):
            guard.inspect_turn()
            print(f"Step {step + 1} passed circuit verification.")
    except (CircuitBreakerException, ValueError) as err:
        print(f"[BLOCKED BY GUARDRAIL]: {err}")
