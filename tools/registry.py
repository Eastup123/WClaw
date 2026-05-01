from collections.abc import Callable

from .basic import (
    create_todo,
    draft_xiaohongshu_post,
    extract_link_stub,
    fetch_url,
    internet_search,
    summarize_text,
)


TOOL_REGISTRY: dict[str, Callable] = {
    "summarize_text": summarize_text,
    "create_todo": create_todo,
    "extract_link_stub": extract_link_stub,
    "draft_xiaohongshu_post": draft_xiaohongshu_post,
    "internet_search": internet_search,
    "fetch_url": fetch_url,
}

