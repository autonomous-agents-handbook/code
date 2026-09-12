import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

LARGE_DOCUMENT_CONTEXT = """
SYSTEM SPECIFICATION V4.2
1. All network payloads must be signed using Ed25519 keys.
2. The agent loop timeout limit is 30 seconds per dispatch turn.
3. Fallback retry policy follows exponential backoff: base 2s, factor 1.5, max 4 retries.
""" + ("\n[EXTENDED REFERENCE MANUAL DATA PAD]" * 250)

def query_with_cache():
    response = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=256,
        system=[
            {
                "type": "text",
                "text": LARGE_DOCUMENT_CONTEXT,
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=[{"role": "user", "content": "What is the fallback retry policy?"}]
    )
    
    usage = response.usage
    print(f"Input tokens: {usage.input_tokens}")
    print(f"Cache created: {getattr(usage, 'cache_creation_input_tokens', 0)}")
    print(f"Cache read: {getattr(usage, 'cache_read_input_tokens', 0)}")
    print("\nAnswer:", response.content[0].text)

if __name__ == "__main__":
    query_with_cache()
