from pathlib import Path
from typing import Any

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

from subagents import build_subagents
from utils.env_utils import apply_environment


def create_agent(settings: dict[str, Any]):
    apply_environment(settings)

    project_root = Path(settings["_meta"]["project_root"])
    skills_dir = (project_root / settings["paths"]["skills_dir"]).resolve()
    backend_root = (project_root / settings["backend"]["root_dir"]).resolve()

    return create_deep_agent(
        model=settings["llm"]["model"],
        system_prompt=settings["prompts"]["main_agent"],
        tools=[],
        skills=[str(skills_dir)],
        subagents=build_subagents(settings),
        backend=FilesystemBackend(
            root_dir=str(backend_root),
            virtual_mode=settings["backend"].get("virtual_mode", True),
        ),
    )
