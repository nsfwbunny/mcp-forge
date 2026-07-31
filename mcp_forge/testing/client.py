"""ForgeTestClient — synchronous test client for mcp-forge apps."""

from __future__ import annotations

import asyncio
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from mcp_forge.core.forge import Forge


class ForgeTestClient:
    """
    Synchronous test client for mcp-forge applications.
    Works correctly in both standard scripts and running event loops
    (pytest-asyncio, Jupyter).

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
        coro = self.app.call_tool(tool_name, params or {})
        try:
            loop = asyncio.get_running_loop()
            # Running inside an existing event loop (pytest-asyncio, Jupyter)
            # Use nest_asyncio if available, otherwise raise a clear error
            try:
                import nest_asyncio
                nest_asyncio.apply(loop)
                return loop.run_until_complete(coro)
            except ImportError:
                raise RuntimeError(
                    "ForgeTestClient.call() was called from inside a running event loop. "
                    "Either use 'await client.acall()' or install nest_asyncio: "
                    "pip install nest_asyncio"
                ) from None
        except RuntimeError:
            # No running loop — safe to use asyncio.run()
            return asyncio.run(coro)

    async def acall(self, tool_name: str, params: dict[str, Any] | None = None) -> Any:
        """Async variant — use inside async tests or coroutines."""
        return await self.app.call_tool(tool_name, params or {})

    def list_tools(self) -> list[dict[str, Any]]:
        """Return the list of registered tools."""
        return self.app.list_tools()
