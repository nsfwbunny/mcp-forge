"""Built-in memory tools — remember, recall, forget.

Each call to `memory_router()` returns a fresh router with its own
isolated store. The module-level `memory` export is the default singleton.
"""

from __future__ import annotations

from mcp_forge.core.forge import Forge


def memory_router() -> Forge:
    """Create a new memory router with an isolated key-value store."""
    router = Forge(name="__memory_router__")
    _store: dict[str, str] = {}  # scoped to this router instance

    @router.tool(description="Store a key-value pair in memory")
    def remember(key: str, value: str) -> str:
        _store[key] = value
        return f"Stored: {key}"

    @router.tool(description="Recall a value from memory by key")
    def recall(key: str) -> str:
        return _store.get(key, f"Key '{key}' not found in memory")

    @router.tool(description="Delete a key from memory")
    def forget(key: str) -> str:
        removed = _store.pop(key, None)
        return f"Forgot: {key}" if removed is not None else f"Key '{key}' not found"

    @router.tool(description="List all keys currently in memory")
    def list_memory() -> list:  # type: ignore[return]
        return list(_store.keys())

    return router


# Default singleton — use memory_router() for isolated instances
memory = memory_router()
