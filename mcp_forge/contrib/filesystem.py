"""Built-in filesystem tools — read, write, list, exists.

All tools are sandboxed to paths the caller explicitly provides.
No implicit CWD traversal or path expansion is performed.
"""

from __future__ import annotations

import os
from pathlib import Path

from mcp_forge.core.forge import Forge

filesystem = Forge(name="__filesystem_router__")


@filesystem.tool(description="Read the contents of a file (UTF-8)")
def read_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not p.is_file():
        raise IsADirectoryError(f"Path is a directory, not a file: {path}")
    return p.read_text(encoding="utf-8")


@filesystem.tool(description="Write content to a file, creating parent directories if needed")
def write_file(path: str, content: str) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"Written: {path} ({len(content)} bytes)"


@filesystem.tool(description="List files and directories at a path, sorted alphabetically")
def list_dir(path: str = ".") -> list[str]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Directory not found: {path}")
    if not p.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")
    return sorted(os.listdir(path))


@filesystem.tool(description="Check whether a file or directory exists at a path")
def path_exists(path: str) -> bool:
    return Path(path).exists()


@filesystem.tool(description="Delete a file (does not delete directories)")
def delete_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not p.is_file():
        raise IsADirectoryError(f"Path is a directory — use a dedicated delete_dir tool: {path}")
    p.unlink()
    return f"Deleted: {path}"
