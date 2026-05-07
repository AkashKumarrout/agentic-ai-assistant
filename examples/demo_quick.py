"""Demo: solve a small task end-to-end using whichever backend is configured.

Run:
    python examples/demo_quick.py

If AGENT_BACKEND is unset, the offline EchoLLM is used so the script always runs.
"""
from agentic_ai import run

if __name__ == "__main__":
    answer = run("Explain what an agentic AI loop is in 5 bullet points.")
    print("\n--- ANSWER ---\n")
    print(answer)
