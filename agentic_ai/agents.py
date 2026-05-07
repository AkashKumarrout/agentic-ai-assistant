"""Specialist agents. Each agent is a thin wrapper around an LLM call."""
from __future__ import annotations

from .llm import LLM
from .memory import Blackboard


PLANNER_SYS = (
    "You are a senior planning agent. Given a user goal, produce a concise, "
    "ordered list of 3-6 concrete steps to accomplish it. Output ONLY the steps, "
    "one per line, prefixed with '- '. No preamble, no closing remarks."
)

RESEARCHER_SYS = (
    "You are a research agent. Given the goal and plan, produce a compact set of "
    "facts, assumptions, and references the Coder will need. Be specific and "
    "technical. Limit to ~200 words."
)

CODER_SYS = (
    "You are a senior software engineer agent. Using the goal, plan, and research "
    "notes, produce the final deliverable (code, document, or analysis) in full. "
    "Include code in fenced blocks. If tests are appropriate, include them. "
    "Address every step of the plan."
)

CRITIC_SYS = (
    "You are a strict reviewer agent. Evaluate the draft against the goal and plan. "
    "Reply on the FIRST line with exactly 'APPROVE' or 'REVISE'. "
    "On subsequent lines list concrete issues (if REVISE) or 'LGTM' (if APPROVE). "
    "Be brief."
)


def _fmt_plan(plan: list[str]) -> str:
    return "\n".join(f"- {step}" for step in plan)


class Planner:
    def __init__(self, llm: LLM) -> None:
        self.llm = llm

    def run(self, bb: Blackboard) -> list[str]:
        out = self.llm.complete(PLANNER_SYS, f"Goal: {bb.goal}", temperature=0.1)
        steps = [
            line.lstrip("-* ").strip()
            for line in out.splitlines()
            if line.strip() and not line.strip().lower().startswith(("here", "plan:"))
        ]
        return [s for s in steps if s][:6] or [bb.goal]


class Researcher:
    def __init__(self, llm: LLM) -> None:
        self.llm = llm

    def run(self, bb: Blackboard) -> str:
        prompt = f"Goal: {bb.goal}\n\nPlan:\n{_fmt_plan(bb.plan)}"
        return self.llm.complete(RESEARCHER_SYS, prompt, temperature=0.2)


class Coder:
    def __init__(self, llm: LLM) -> None:
        self.llm = llm

    def run(self, bb: Blackboard) -> str:
        prompt = (
            f"Goal: {bb.goal}\n\nPlan:\n{_fmt_plan(bb.plan)}\n\n"
            f"Research notes:\n{bb.research}\n\n"
            f"Previous critique (address if any):\n{bb.critique or '(none)'}"
        )
        return self.llm.complete(CODER_SYS, prompt, temperature=0.3)


class Critic:
    def __init__(self, llm: LLM) -> None:
        self.llm = llm

    def run(self, bb: Blackboard) -> tuple[bool, str]:
        prompt = (
            f"Goal: {bb.goal}\n\nPlan:\n{_fmt_plan(bb.plan)}\n\nDraft:\n{bb.draft}"
        )
        out = self.llm.complete(CRITIC_SYS, prompt, temperature=0.0)
        first = out.splitlines()[0].strip().upper() if out else "REVISE"
        approved = first.startswith("APPROVE")
        return approved, out
