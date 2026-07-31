"""ForgeTestClient — synchronous test client for mcp-forge apps."""

from __future__ import annotations

import asyncio
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from mcp_forge.core.forge import Forge


class ForgeTestClient:
    """
    Synchronous test client for mcp-forge applications.

    Usage::

        from mcp_forge.testing import ForgeTestClient

        client = ForgeTestClient(app)
        result = client.call("add", {"a": 2, "b": 3})
        assert result == 5
    """

    def __init__(self, app: "Forge") -> None:
        self.app = app

    def call(self, tool_name: str, params: dict[str, Any] | None = None) -> Any:
        """Call a tool synchronously and return the result."""
        return asyncio.run(self.app.call_tool(tool_name, params or {}))

    def list_tools(self) -> list[dict[str, Any]]:
        """Return the list of registered tools."""
        return self.app.list_tools()
