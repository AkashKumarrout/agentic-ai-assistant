"""Shared blackboard memory for inter-agent communication."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Blackboard:
    goal: str = ""
    plan: list[str] = field(default_factory=list)
    research: str = ""
    draft: str = ""
    critique: str = ""
    approved: bool = False
    iterations: int = 0
    extra: dict[str, Any] = field(default_factory=dict)

    def snapshot(self) -> dict[str, Any]:
        return {
            "goal": self.goal,
            "plan": list(self.plan),
            "research": self.research,
            "draft": self.draft,
            "critique": self.critique,
            "approved": self.approved,
            "iterations": self.iterations,
        }
