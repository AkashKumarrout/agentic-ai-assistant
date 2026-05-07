"""Tools that agents may invoke. Kept minimal & dependency-free."""
from __future__ import annotations

import ast
import io
import contextlib
from urllib import request as _urlreq
from urllib.error import URLError


def fetch_url(url: str, max_bytes: int = 20_000) -> str:
    """Fetch a URL and return up to `max_bytes` of decoded text."""
    if not url.startswith(("http://", "https://")):
        return f"[fetch_url] Refused: only http(s) allowed, got {url!r}"
    try:
        with _urlreq.urlopen(url, timeout=15) as resp:
            data = resp.read(max_bytes)
        return data.decode("utf-8", errors="replace")
    except URLError as exc:
        return f"[fetch_url] error: {exc}"


def safe_eval_python(source: str) -> str:
    """Execute a *small* snippet of pure Python and return stdout.

    Restricted: rejects imports, attribute access on dunders, and exec/eval.
    Use only with trusted input — this is a demo sandbox, not a security boundary.
    """
    try:
        tree = ast.parse(source, mode="exec")
    except SyntaxError as exc:
        return f"[safe_eval_python] SyntaxError: {exc}"

    banned_nodes = (ast.Import, ast.ImportFrom)
    for node in ast.walk(tree):
        if isinstance(node, banned_nodes):
            return "[safe_eval_python] imports are not allowed"
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            return "[safe_eval_python] dunder access not allowed"
        if isinstance(node, ast.Name) and node.id in {"exec", "eval", "open", "compile"}:
            return f"[safe_eval_python] use of {node.id} not allowed"

    buf = io.StringIO()
    safe_globals: dict = {"__builtins__": {"print": print, "range": range, "len": len, "sum": sum}}
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(tree, "<sandbox>", "exec"), safe_globals, {})
    except Exception as exc:  # noqa: BLE001
        return f"[safe_eval_python] runtime error: {exc}"
    return buf.getvalue() or "[safe_eval_python] (no output)"


TOOLS = {
    "fetch_url": fetch_url,
    "python": safe_eval_python,
}
