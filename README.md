# Building Autonomous AI Agents with Claude — Companion Code

This repository contains the complete, runnable Python code examples, architecture blueprints, and production guardrails from the book **Building Autonomous AI Agents with Claude**.

## 📁 Chapter Directory

- **`chapter-01-react-loop/`**: Minimal ReAct control loop with scratchpad iteration.
- **`chapter-02-sdk-setup/`**: Modern client setup, streaming responses, and system prompt engineering.
- **`chapter-03-structured-outputs/`**: Pydantic schema validation and JSON extraction.
- **`chapter-04-tool-calling/`**: Native tool calling, dynamic dispatching, and error handling.
- **`chapter-05-mcp-protocol/`**: Model Context Protocol (FastMCP) server and client implementations.
- **`chapter-06-memory-caching/`**: Prompt Caching integration and sliding-window context buffers.
- **`chapter-07-research-agent/`**: Complete multi-step web search and synthesis agent.
- **`chapter-08-code-healing-agent/`**: Autonomous code execution and self-debugging sandbox.
- **`chapter-09-multi-agent/`**: Supervisor-Worker orchestration pattern.
- **`chapter-10-production-guardrails/`**: Loop circuit-breakers, token limits, and human-in-the-loop gates.

---

## 🚀 Quickstart

### 1. Clone the repository
```bash
git clone [https://github.com/autonomous-agents-handbook/code.git](https://github.com/autonomous-agents-handbook/code.git)
cd code
```
**2. Set up environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
**3. Configure API Key**
```bash
cp .env.example .env
```
Open .env and add your Anthropic API key:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
```
**4. Run your first agent**
```bash
python chapter-01-react-loop/agent.py
```
**📜 Disclaimer**
This repository contains code examples for educational purposes accompanying the book Building Autonomous AI Agents with Claude. It is an independent publication and is not affiliated with, sponsored by, or endorsed by Anthropic, PBC.
