"""CLI entry point: `python -m agentic_ai "<your goal>"`."""
import sys
from .orchestrator import run


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: python -m agentic_ai "<your goal>"', file=sys.stderr)
        return 2
    goal = " ".join(sys.argv[1:])
    result = run(goal)
    print("\n=== FINAL ANSWER ===\n")
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
