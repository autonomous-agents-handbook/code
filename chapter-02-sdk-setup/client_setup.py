import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def stream_response(prompt: str):
    """Demonstrates streaming agent thought tokens in real-time."""
    print(f"\n[QUERY]: {prompt}\n" + "-" * 40)
    
    with client.messages.stream(
        model="claude-3-5-sonnet-latest",
        max_tokens=1024,
        system="You are an expert system architect. Be direct and concise.",
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    print("\n")

if __name__ == "__main__":
    stream_response("Explain why stateless API calls require external scratchpad memory for agents.")
