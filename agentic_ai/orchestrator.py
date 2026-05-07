"""Multi-agent orchestrator with critique loop."""
from __future__ import annotations

from .agents import Coder, Critic, Planner, Researcher
from .llm import LLM, get_llm
from .memory import Blackboard
from .tracing import Tracer


def run(goal: str, max_iterations: int = 3, llm: LLM | None = None) -> str:
    """Execute the agent loop and return the final draft."""
    llm = llm or get_llm()
    bb = Blackboard(goal=goal)
    tracer = Tracer()

    try:
        planner = Planner(llm)
        researcher = Researcher(llm)
        coder = Coder(llm)
        critic = Critic(llm)

        bb.plan = planner.run(bb)
        tracer.log("planner", "plan", bb.plan)
        print(f"[Planner] {len(bb.plan)} step(s):")
        for step in bb.plan:
            print(f"  - {step}")

        bb.research = researcher.run(bb)
        tracer.log("researcher", "notes", bb.research)
        print(f"[Researcher] {len(bb.research)} chars of notes.")

        for i in range(1, max_iterations + 1):
            bb.iterations = i
            bb.draft = coder.run(bb)
            tracer.log("coder", f"draft#{i}", bb.draft)
            print(f"[Coder] iteration {i}: {len(bb.draft)} chars produced.")

            approved, critique = critic.run(bb)
            bb.critique = critique
            bb.approved = approved
            tracer.log("critic", f"review#{i}", {"approved": approved, "text": critique})
            verdict = "APPROVED" if approved else "REVISE"
            print(f"[Critic] iteration {i}: {verdict}")
            if approved:
                break

        return bb.draft
    finally:
        tracer.close()
