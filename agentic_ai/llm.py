"""Pluggable LLM backends: OpenAI and Ollama."""
from __future__ import annotations

import json
import os
from typing import Protocol
from urllib import request as _urlreq
from urllib.error import URLError


class LLM(Protocol):
    def complete(self, system: str, user: str, temperature: float = 0.2) -> str: ...


class OllamaLLM:
    """Local Ollama backend. Requires `ollama serve` running."""

    def __init__(self, model: str = "llama3", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host.rstrip("/")

    def complete(self, system: str, user: str, temperature: float = 0.2) -> str:
        body = json.dumps(
            {
                "model": self.model,
                "stream": False,
                "options": {"temperature": temperature},
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            }
        ).encode("utf-8")
        req = _urlreq.Request(
            f"{self.host}/api/chat",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        try:
            with _urlreq.urlopen(req, timeout=120) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except URLError as exc:
            raise RuntimeError(f"Ollama request failed: {exc}") from exc
        return payload.get("message", {}).get("content", "").strip()


class OpenAILLM:
    """OpenAI Chat Completions backend (HTTP, no SDK dependency)."""

    def __init__(self, model: str = "gpt-4o-mini", api_key: str | None = None):
        self.model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set.")

    def complete(self, system: str, user: str, temperature: float = 0.2) -> str:
        body = json.dumps(
            {
                "model": self.model,
                "temperature": temperature,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            }
        ).encode("utf-8")
        req = _urlreq.Request(
            "https://api.openai.com/v1/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )
        with _urlreq.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        return payload["choices"][0]["message"]["content"].strip()


class EchoLLM:
    """Offline stub used by tests when no backend is configured."""

    def complete(self, system: str, user: str, temperature: float = 0.2) -> str:
        return f"[echo] {user[:200]}"


def get_llm() -> LLM:
    backend = os.environ.get("AGENT_BACKEND", "echo").lower()
    model = os.environ.get("AGENT_MODEL")
    if backend == "openai":
        return OpenAILLM(model=model or "gpt-4o-mini")
    if backend == "ollama":
        return OllamaLLM(model=model or "llama3")
    return EchoLLM()
