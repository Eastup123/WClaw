import json
import os
from typing import Literal
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from langchain_core.tools import tool
from tavily import TavilyClient


def _build_tavily_client() -> TavilyClient:
    api_key = os.getenv("TAVILY_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY is not set. Please export the Tavily API key before using internet_search."
        )
    return TavilyClient(api_key=api_key)


@tool
def summarize_text(text: str) -> str:
    """Return a short summary stub for the provided text."""
    normalized = " ".join(text.split())
    if not normalized:
        return "No content provided."
    if len(normalized) <= 120:
        return normalized
    return f"{normalized[:117]}..."


@tool
def create_todo(task: str) -> str:
    """Create a simple todo item description."""
    normalized = task.strip()
    if not normalized:
        return "TODO: clarify the next action."
    return f"TODO: {normalized}"


@tool
def extract_link_stub(link: str) -> str:
    """Return a lightweight placeholder for a link-processing step."""
    normalized = link.strip()
    if not normalized:
        return "No link provided."
    return f"Link captured for follow-up: {normalized}"


@tool
def draft_xiaohongshu_post(topic: str) -> str:
    """Generate a compact Xiaohongshu-style draft for a topic."""
    normalized = topic.strip() or "未命名主题"
    return (
        f"标题：{normalized}\n"
        f"正文：围绕“{normalized}”整理亮点、体验和行动建议，补充真实细节后即可发布。\n"
        "标签：#经验分享 #内容草稿"
    )


@tool
def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
) -> str:
    """Search the internet for up-to-date information with Tavily."""
    normalized_query = query.strip()
    if not normalized_query:
        return "Search query is empty."

    if max_results < 1:
        return "max_results must be at least 1."

    try:
        response = _build_tavily_client().search(
            query=normalized_query,
            max_results=max_results,
            topic=topic,
            include_raw_content=include_raw_content,
        )
    except Exception as exc:
        return f"internet_search failed: {exc}"

    return json.dumps(response, ensure_ascii=False, indent=2)


@tool
def fetch_url(url: str) -> str:
    """Fetch a URL and return the page content as UTF-8 text when possible."""
    normalized_url = url.strip()
    if not normalized_url:
        return "URL is empty."

    request = Request(
        normalized_url,
        headers={
            "User-Agent": "WClaw/1.0 (+https://local-agent)",
        },
    )

    try:
        with urlopen(request, timeout=20) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            content_type = response.headers.get("Content-Type", "")
            body = response.read().decode(charset, errors="replace")
    except HTTPError as exc:
        return f"fetch_url failed with HTTP {exc.code}: {exc.reason}"
    except URLError as exc:
        return f"fetch_url failed: {exc.reason}"
    except Exception as exc:
        return f"fetch_url failed: {exc}"

    preview = body if len(body) <= 12000 else f"{body[:12000]}\n...[truncated]"
    return f"URL: {normalized_url}\nContent-Type: {content_type}\n\n{preview}"
