"""Built-in contrib tool routers — lazy imports to avoid dependency errors.

Import the router you need directly:

    from mcp_forge.contrib import memory
    from mcp_forge.contrib import filesystem
    from mcp_forge.contrib import web  # requires: pip install httpx
"""

from __future__ import annotations


def __getattr__(name: str) -> object:
    """
    Lazy-load contrib routers on first access.
    Prevents ImportError when optional extras (httpx) are not installed.
    """
    if name == "memory":
        from mcp_forge.contrib.memory import memory
        return memory
    if name == "filesystem":
        from mcp_forge.contrib.filesystem import filesystem
        return filesystem
    if name == "web":
        from mcp_forge.contrib.web import web
        return web
    raise AttributeError(f"module 'mcp_forge.contrib' has no attribute '{name}'")


__all__ = ["memory", "filesystem", "web"]
