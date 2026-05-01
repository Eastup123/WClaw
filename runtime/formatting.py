import json
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
