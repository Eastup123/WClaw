from typing import Any, Iterable

from .registry import TOOL_REGISTRY


def build_toolset(tool_names: Iterable[str] | None) -> list[Any]:
    """Resolve configured tool names into LangChain-compatible tool objects."""
    if tool_names is None:
        return []

    resolved = []
    missing = []
    for tool_name in tool_names:
        tool_obj = TOOL_REGISTRY.get(tool_name)
        if tool_obj is None:
            missing.append(tool_name)
            continue
        resolved.append(tool_obj)

    if missing:
        available = ", ".join(sorted(TOOL_REGISTRY))
        missing_text = ", ".join(missing)
        raise ValueError(f"Unknown tools: {missing_text}. Available tools: {available}")

    return resolved
