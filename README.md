# Agentic AI Assistant

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

## Example output

```
[Planner]   Steps: 1) parse spec 2) implement parser 3) write tests
[Researcher] Notes: PTP header is 34 bytes, fields: ...
[Coder]     Produced 42 lines of Python + pytest cases.
[Critic]    APPROVED — coverage of all required fields, edge cases handled.
```

## Roadmap

- [ ] Add a real web-search tool (Tavily / DuckDuckGo)
- [ ] Add a sandboxed Python execution tool
- [ ] Persistent vector memory (FAISS)
- [ ] Streamlit UI

## License

MIT — see [LICENSE](LICENSE).
