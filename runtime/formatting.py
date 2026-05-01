import json
from pathlib import Path
from typing import Any


def _extract_text_from_content(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(part.strip() for part in parts if part and part.strip())
    return ""


def extract_stream_text(message: Any) -> str:
    return _extract_text_from_content(getattr(message, "content", None))


def _extract_path_from_args(args: Any) -> str | None:
    if not isinstance(args, dict):
        return None

    for key in ("path", "file_path", "filepath", "filename"):
        value = args.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _extract_skill_name_from_path(path_value: str | None) -> str | None:
    if not path_value:
        return None

    normalized = path_value.replace("\\", "/")
    if not normalized.endswith("/SKILL.md"):
        return None

    return Path(normalized).parent.name or None


def extract_runtime_activities(message: Any) -> list[dict[str, str]]:
    activities: list[dict[str, str]] = []

    for tool_call in getattr(message, "tool_calls", None) or []:
        if not isinstance(tool_call, dict):
            continue

        call_id = str(tool_call.get("id") or "")
        tool_name = str(tool_call.get("name") or "").strip()
        args = tool_call.get("args") or {}

        if not tool_name:
            continue

        if tool_name == "task":
            subagent_name = ""
            if isinstance(args, dict):
                subagent_name = str(args.get("subagent_type") or "").strip()
            label = subagent_name or "task"
            activities.append(
                {
                    "kind": "subagent",
                    "label": label,
                    "call_id": call_id or f"subagent:{label}",
                }
            )
            continue

        path_value = _extract_path_from_args(args)
        skill_name = _extract_skill_name_from_path(path_value)
        if skill_name:
            activities.append(
                {
                    "kind": "skill",
                    "label": skill_name,
                    "call_id": f"skill:{skill_name}",
                }
            )

        activities.append(
            {
                "kind": "tool",
                "label": tool_name,
                "call_id": call_id or f"tool:{tool_name}",
            }
        )

    return activities


def format_agent_result(result: Any) -> str:
    if isinstance(result, dict):
        messages = result.get("messages")
        if isinstance(messages, list):
            for message in reversed(messages):
                if isinstance(message, dict):
                    text = _extract_text_from_content(message.get("content"))
                    if text:
                        return text
                else:
                    content = getattr(message, "content", None)
                    text = _extract_text_from_content(content)
                    if text:
                        return text

        for key in ("output", "final_output", "response", "content"):
            text = _extract_text_from_content(result.get(key))
            if text:
                return text

        return json.dumps(result, ensure_ascii=False, indent=2, default=str)

    content = getattr(result, "content", None)
    text = _extract_text_from_content(content)
    if text:
        return text

    messages = getattr(result, "messages", None)
    if isinstance(messages, list):
        for message in reversed(messages):
            content = getattr(message, "content", None)
            text = _extract_text_from_content(content)
            if text:
                return text

    return str(result)
