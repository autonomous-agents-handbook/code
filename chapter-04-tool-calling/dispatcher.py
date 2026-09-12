import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# 1. Define executable Python tools
def calculate(expression: str) -> str:
    """Safely evaluates a basic mathematical expression."""
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        return "Error: Invalid characters in arithmetic expression."
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Execution error: {e}"

TOOL_REGISTRY = {
    "calculate": calculate
}

# 2. Declare Anthropic tool schema
TOOLS = [
    {
        "name": "calculate",
        "description": "Perform mathematical calculations. Accepts arithmetic strings like '150 * 0.85'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate."
                }
            },
            "required": ["expression"]
        }
    }
]

# 3. Agent Execution Loop
def run_tool_agent(prompt: str):
    messages = [{"role": "user", "content": prompt}]
    
    while True:
        response = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages
        )
        
        # Capture assistant response
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_args = block.input
                    tool_id = block.id
                    
                    print(f"[TOOL CALLED]: {tool_name} with args: {tool_args}")
                    
                    # Execute tool locally
                    func = TOOL_REGISTRY.get(tool_name)
                    output = func(**tool_args) if func else "Error: Tool not found."
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": str(output)
                    })
            
            # Feed tool results back to Claude
            messages.append({"role": "user", "content": tool_results})
        else:
            # Final output reached
            for block in response.content:
                if hasattr(block, "text"):
                    print("\n[FINAL RESPONSE]:\n" + block.text)
            break

if __name__ == "__main__":
    run_tool_agent("What is (450 * 12) divided by 1.15?")
