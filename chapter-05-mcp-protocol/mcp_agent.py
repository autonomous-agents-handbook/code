import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Simulating an MCP Server Protocol interface
MCP_SERVER_RESOURCES = {
    "db://users/active": [{"id": 101, "role": "admin", "status": "online"}],
    "db://logs/error": ["500: Database connection timeout at 02:14:00"]
}

def read_mcp_resource(uri: str) -> str:
    """Reads structured context exposed by an MCP server."""
    data = MCP_SERVER_RESOURCES.get(uri)
    return str(data) if data else f"URI '{uri}' not found."

TOOLS = [{
    "name": "read_mcp_resource",
    "description": "Read context data from an MCP URI endpoint.",
    "input_schema": {
        "type": "object",
        "properties": {"uri": {"type": "string"}},
        "required": ["uri"]
    }
}]

def run_mcp_agent():
    messages = [{"role": "user", "content": "Check the error logs from db://logs/error and summarize the issue."}]
    response = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=512,
        tools=TOOLS,
        messages=messages
    )
    
    if response.stop_reason == "tool_use":
        block = response.content[0]
        uri = block.input["uri"]
        content = read_mcp_resource(uri)
        print(f"[MCP DISPATCH] Fetched {uri} -> {content}")

if __name__ == "__main__":
    run_mcp_agent()
