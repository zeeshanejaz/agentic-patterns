from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


def workspace_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").exists() and (parent / "packages").is_dir():
            return parent
    raise RuntimeError("Could not find the uv workspace root")


def load_env() -> None:
    load_dotenv(workspace_root() / ".env")


def openai_model() -> str:
    return os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
