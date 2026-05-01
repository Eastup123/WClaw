from collections.abc import Callable

from .basic import create_todo, draft_xiaohongshu_post, extract_link_stub, summarize_text


TOOL_REGISTRY: dict[str, Callable] = {
    "summarize_text": summarize_text,
    "create_todo": create_todo,
    "extract_link_stub": extract_link_stub,
    "draft_xiaohongshu_post": draft_xiaohongshu_post,
}

