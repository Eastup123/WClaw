from pathlib import Path
from typing import Any

from tools import build_toolset


def _resolve_skill_paths(skill_entries: list[str], skills_dir: Path) -> list[str]:
    resolved = []
    for skill in skill_entries:
        skill_path = Path(skill)
        if not skill_path.is_absolute():
            skill_path = skills_dir / skill_path
        resolved.append(str(skill_path.resolve()))
    return resolved


def build_subagents(settings: dict[str, Any]) -> list[dict[str, Any]]:
    project_root = Path(settings["_meta"]["project_root"])
    skills_dir = (project_root / settings["paths"]["skills_dir"]).resolve()

    subagents: list[dict[str, Any]] = []
    configured = settings.get("subagents", {})
    for config in configured.values():
        if not config.get("enabled", True):
            continue

        subagents.append(
            {
                "name": config["name"],
                "description": config["description"],
                "system_prompt": config["system_prompt"],
                "tools": build_toolset(config.get("tools")),
                "skills": _resolve_skill_paths(config.get("skills", []), skills_dir),
            }
        )

    return subagents
