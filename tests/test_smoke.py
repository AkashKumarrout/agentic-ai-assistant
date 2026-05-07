"""Smoke tests using the offline EchoLLM backend."""
from agentic_ai.llm import EchoLLM
from agentic_ai.orchestrator import run
from agentic_ai.tools import safe_eval_python


def test_run_with_echo_backend(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    out = run("write hello world in python", llm=EchoLLM(), max_iterations=1)
    assert isinstance(out, str)
    assert out  # non-empty


def test_safe_eval_blocks_imports():
    result = safe_eval_python("import os")
    assert "not allowed" in result


def test_safe_eval_runs_simple_code():
    result = safe_eval_python("print(2 + 2)")
    assert result.strip() == "4"
