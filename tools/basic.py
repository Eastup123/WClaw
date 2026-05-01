from langchain_core.tools import tool


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
