import os
from typing import Any


def apply_environment(settings: dict[str, Any]) -> None:
    llm = settings.get("llm", {})
    observability = settings.get("observability", {})

    if llm.get("openai_base_url"):
        os.environ["OPENAI_BASE_URL"] = llm["openai_base_url"]
    if llm.get("openai_api_key"):
        os.environ["OPENAI_API_KEY"] = llm["openai_api_key"]

    os.environ["DEEPAGENT_MODEL"] = llm.get("model", os.getenv("DEEPAGENT_MODEL", ""))

    if observability.get("langsmith_tracing") is not None:
        os.environ["LANGSMITH_TRACING"] = str(observability["langsmith_tracing"]).lower()
    if observability.get("langsmith_api_key"):
        os.environ["LANGSMITH_API_KEY"] = observability["langsmith_api_key"]
    if observability.get("langsmith_project"):
        os.environ["LANGSMITH_PROJECT"] = observability["langsmith_project"]
