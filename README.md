# Agentic AI Assistant

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/AkashKumarrout/agentic-ai-assistant)

A lightweight, framework-free **multi-agent AI system** in Python that decomposes a user goal into steps and solves it through cooperating specialist agents:

```
        ┌──────────┐     ┌────────────┐     ┌────────┐     ┌────────┐
 goal → │ Planner  │ --> │ Researcher │ --> │ Coder  │ --> │ Critic │ --> answer
        └──────────┘     └────────────┘     └────────┘     └────────┘
                                ▲                              │
                                └──────── revise loop ─────────┘
```

## Features

- **Pluggable LLM backend** — works with OpenAI API or a local **Ollama** model (no API key needed).
- **No heavy framework** — pure Python, ~300 LOC, easy to read and extend.
- **Tool use** — agents can call tools (web fetch stub, Python sandbox, file read).
- **Self-critique loop** — Critic agent rejects/approves outputs until quality bar met or max iterations.
- **Trace logging** — every agent step is logged to `runs/<timestamp>.jsonl` for inspection.
- **CLI + Python API**.

## Quick start

```bash
git clone https://github.com/<your-username>/agentic-ai-assistant.git
cd agentic-ai-assistant
pip install -r requirements.txt

# Option A: use Ollama locally (free)
ollama pull llama3
export AGENT_BACKEND=ollama
export AGENT_MODEL=llama3

# Option B: use OpenAI
export AGENT_BACKEND=openai
export OPENAI_API_KEY=sk-...
export AGENT_MODEL=gpt-4o-mini

python -m agentic_ai "Write a Python function that parses an IEEE 1588 PTP header and add unit tests."
```

## Project layout

```
agentic_ai/
├── __init__.py
├── __main__.py        # CLI entry
├── orchestrator.py    # Multi-agent loop
├── agents.py          # Planner / Researcher / Coder / Critic
├── llm.py             # OpenAI + Ollama backends
├── tools.py           # Tool implementations
├── memory.py          # Shared blackboard memory
└── tracing.py         # JSONL run logger
tests/
└── test_smoke.py
```

## Live demo run (real output)

Goal: *Write a Python function to compute the factorial of n iteratively, with 3 unit tests.*  
Backend: local Ollama with model `qwen2.5:0.5b` (no API key needed).

```text
[Planner] 4 step(s):
  - Import math for use in factorial computation
  - Define helper function factorial_iterative (iterative approach)
  - Implement test_factorial using assertions
  - Add 3 unit tests: inputs 0, 1, 5
[Researcher] 710 chars of notes.
[Coder]      iteration 1: 710 chars produced.
[Critic]     iteration 1: APPROVED
```

Final code produced by the Coder agent:

```python
def factorial_iterative(n):
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def test_factorial():
    assert factorial_iterative(0) == 1
    assert factorial_iterative(5) == 120
    assert factorial_iterative(1) == 1
```

Full saved transcript: [`examples/sample_run.txt`](examples/sample_run.txt).

## Roadmap

- [ ] Add a real web-search tool (Tavily / DuckDuckGo)
- [ ] Add a sandboxed Python execution tool
- [ ] Persistent vector memory (FAISS)
- [ ] Streamlit UI

## License

MIT — see [LICENSE](LICENSE).
