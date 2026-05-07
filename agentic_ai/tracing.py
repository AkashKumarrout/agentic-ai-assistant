"""JSONL run tracer."""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any


class Tracer:
    def __init__(self, root: str | os.PathLike[str] = "runs") -> None:
        Path(root).mkdir(parents=True, exist_ok=True)
        self.path = Path(root) / f"{int(time.time())}.jsonl"
        self._fh = self.path.open("a", encoding="utf-8")

    def log(self, agent: str, event: str, data: Any) -> None:
        rec = {"ts": time.time(), "agent": agent, "event": event, "data": data}
        self._fh.write(json.dumps(rec, default=str) + "\n")
        self._fh.flush()

    def close(self) -> None:
        self._fh.close()
