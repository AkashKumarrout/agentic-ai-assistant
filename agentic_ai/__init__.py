"""Agentic AI Assistant - multi-agent orchestration toolkit."""
from .orchestrator import run
from .memory import Blackboard

__all__ = ["run", "Blackboard"]
__version__ = "0.1.0"
