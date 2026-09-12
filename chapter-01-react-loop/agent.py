import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

SYSTEM_PROMPT = """
You are an autonomous ReAct agent. You solve tasks by iterating through three distinct phases:
1. THOUGHT: Reason carefully about the problem, current state, and what information is missing.
2. ACTION: Decide on a concrete next step or calculation to execute.
3. OBSERVATION: Analyze the result and determine if the final answer is reached.

When you reach the solution, output:
FINAL ANSWER: [Your definitive answer]
"""

def run_react_agent(user_query: str, max_turns: int = 5):
    messages = [{"role": "user", "content": user_query}]
    
    print(f"\n[USER QUERY]: {user_query}\n" + "-" * 50)

    for turn in range(1, max_turns + 1):
        print(f"\n--- Turn {turn} ---")
        
        response = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages
        )
        
        assistant_reply = response.content[0].text
        print(assistant_reply)

        if "FINAL ANSWER:" in assistant_reply:
            print("\n[SUCCESS] Goal achieved.")
            return assistant_reply

        # Append turn to message history for continuous scratchpad memory
        messages.append({"role": "assistant", "content": assistant_reply})
        messages.append({"role": "user", "content": "Proceed to the next Thought or provide FINAL ANSWER."})

    print("\n[STOP] Reached maximum iteration limit.")
    return None

if __name__ == "__main__":
    task = "A store sells laptops for $850 each. A customer buys 4 laptops with a 15% discount and 8% sales tax applied after the discount. Calculate the exact final amount paid."
    run_react_agent(task)
