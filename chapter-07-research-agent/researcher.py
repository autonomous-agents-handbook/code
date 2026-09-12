import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

KNOWLEDGE_BASE = {
    "rag architecture": "Modern RAG architectures use hybrid sparse-dense retrieval with cross-encoder re-ranking.",
    "context window": "Claude 3.5 Sonnet supports a 200k token context window with prompt caching."
}

def lookup(term: str) -> str:
    for key, val in KNOWLEDGE_BASE.items():
        if key in term.lower():
            return val
    return "No records matching query."

def research(topic: str):
    print(f"[AGENT ACTIVATED] Researching: {topic}")
    result = lookup(topic)
    
    response = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=512,
        messages=[
            {"role": "user", "content": f"Topic: {topic}\nRetrieved Knowledge: {result}\nProvide a concise 2-sentence synthesis."}
        ]
    )
    print("\n[SYNTHESIS]:", response.content[0].text)

if __name__ == "__main__":
    research("RAG architecture best practices")
