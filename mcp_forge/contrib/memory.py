"""Built-in memory tools — remember, recall, forget."""

from __future__ import annotations

from mcp_forge.core.forge import Forge

memory = Forge(name="__memory_router__")

_store: dict[str, str] = {}


@memory.tool(description="Store a key-value pair in memory")
def remember(key: str, value: str) -> str:
    _store[key] = value
    return f"Stored: {key}"


@memory.tool(description="Recall a value from memory by key")
def recall(key: str) -> str:
    return _store.get(key, f"Key '{key}' not found in memory")


@memory.tool(description="Delete a key from memory")
def forget(key: str) -> str:
    removed = _store.pop(key, None)
    return f"Forgot: {key}" if removed is not None else f"Key '{key}' not found"


@memory.tool(description="List all keys currently in memory")
def list_memory() -> list:
    return list(_store.keys())
