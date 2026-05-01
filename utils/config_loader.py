import os
import re
from pathlib import Path
from typing import Any

import yaml


ENV_VAR_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)\}")


def _resolve_env_placeholders(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _resolve_env_placeholders(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_resolve_env_placeholders(item) for item in value]
    if isinstance(value, str):
        return ENV_VAR_PATTERN.sub(lambda match: os.getenv(match.group(1), match.group(0)), value)
    return value


def load_settings(config_path: str | Path) -> dict[str, Any]:
    path = Path(config_path).resolve()
    with path.open("r", encoding="utf-8") as file:
        raw = yaml.safe_load(file) or {}

    settings = _resolve_env_placeholders(raw)
    settings["_meta"] = {
        "config_path": str(path),
        "project_root": str(path.parent.parent.resolve()),
    }
    return settings
