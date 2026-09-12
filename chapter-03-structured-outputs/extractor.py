import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class AgentAction(BaseModel):
    action_type: str = Field(description="Type of action: 'search', 'execute', or 'respond'")
    target: str = Field(description="Target tool, URL, or code file")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")

def extract_structured_plan(prompt: str) -> AgentAction:
    tools = [
        {
            "name": "emit_action_schema",
            "description": "Output the structured agent decision.",
            "input_schema": AgentAction.model_json_schema()
        }
    ]
    
    response = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=512,
        tools=tools,
        tool_choice={"type": "tool", "name": "emit_action_schema"},
        messages=[{"role": "user", "content": prompt}]
    )
    
    tool_input = response.content[0].input
    validated_action = AgentAction(**tool_input)
    return validated_action

if __name__ == "__main__":
    action = extract_structured_plan("The user wants to inspect current server memory usage.")
    print("Validated Output:", action.model_dump_json(indent=2))
