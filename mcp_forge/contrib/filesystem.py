"""Built-in filesystem tools — read, write, list."""

from __future__ import annotations

import os
from pathlib import Path

from mcp_forge.core.forge import Forge

filesystem = Forge(name="__filesystem_router__")


@filesystem.tool(description="Read the contents of a file")
def read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


@filesystem.tool(description="Write content to a file (creates if not exists)")
def write_file(path: str, content: str) -> str:
    Path(path).write_text(content, encoding="utf-8")
    return f"Written: {path}"


@filesystem.tool(description="List files in a directory")
def list_dir(path: str = ".") -> list:
    return os.listdir(path)


@filesystem.tool(description="Check if a file or directory exists")
def path_exists(path: str) -> bool:
    return Path(path).exists()
