import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def dispatch_worker(specialty: str, task: str) -> str:
    response = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=300,
        system=f"You are a specialized {specialty} sub-agent. Answer directly.",
        messages=[{"role": "user", "content": task}]
    )
    return response.content[0].text

def supervisor(request: str):
    print(f"[SUPERVISOR TASK]: {request}")
    
    # 1. Delegate technical code analysis
    code_summary = dispatch_worker("Software Tester", "Write a single pytest test case for an agent email validator.")
    print(f"\n[WORKER 1 - TESTER]:\n{code_summary}")
    
    # 2. Delegate security audit
    security_audit = dispatch_worker("Security Auditor", f"Review this code logic for injection risks:\n{code_summary}")
    print(f"\n[WORKER 2 - SECURITY]:\n{security_audit}")

if __name__ == "__main__":
    supervisor("Build and review an agent tool for validating emails.")
