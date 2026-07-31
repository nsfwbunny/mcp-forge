"""Core Forge application class."""

from __future__ import annotations

import asyncio
import copy
import logging
from typing import Any, Callable

from mcp_forge.core.config import ForgeConfig
from mcp_forge.core.schema import build_schema
from mcp_forge.core.validator import validate_input, validate_output
from mcp_forge.core.exceptions import ToolNotFoundError

logger = logging.getLogger("mcp_forge")


class Forge:
    """
    Main application class for mcp-forge.

    Usage::

        app = Forge(name="my-server", version="1.0.0")

        @app.tool(description="Add two numbers")
        def add(a: int, b: int) -> int:
            return a + b

        app.run()  # STDIO by default
    """

    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
        description: str = "",
        config: ForgeConfig | None = None,
    ) -> None:
        self.name = name
        self.version = version
        self.description = description
        self.config = config or ForgeConfig()
        self._tools: dict[str, dict[str, Any]] = {}
        self._routers: list[Any] = []
        self._setup_logging()

    def _setup_logging(self) -> None:
        logging.basicConfig(
            level=getattr(logging, self.config.log_level.upper(), logging.INFO),
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        )

    def tool(
        self,
        name: str | None = None,
        description: str = "",
        tags: list[str] | None = None,
    ) -> Callable:
        """
        Decorator to register a function as an MCP tool.

        Args:
            name: Tool name (defaults to function name)
            description: Human-readable description surfaced to the LLM
            tags: Optional metadata tags for grouping tools

        Returns:
            The original function, unmodified.
        """

        def decorator(fn: Callable) -> Callable:
            tool_name = name or fn.__name__
            schema = build_schema(fn)
            self._tools[tool_name] = {
                "fn": fn,
                "name": tool_name,
                "description": description or (fn.__doc__ or "").strip(),
                "schema": schema,
                "tags": tags or [],
                "is_async": asyncio.iscoroutinefunction(fn),
            }
            logger.debug("Registered tool: %s", tool_name)
            return fn

        return decorator

    def include(self, router: Any) -> None:
        """
        Include a contrib router (memory, filesystem, web, etc.).

        Tools are deep-copied so each Forge instance gets its own
        independent tool registry — no shared mutable state between apps.
        """
        for tool_name, tool_def in router._tools.items():
            # Deep copy the metadata dict; keep the function reference intact
            entry = copy.copy(tool_def)
            self._tools[tool_name] = entry
            logger.debug("Included contrib tool: %s from %s", tool_name, router.name)
        self._routers.append(router)

    async def call_tool(self, name: str, params: dict[str, Any]) -> Any:
        """Execute a registered tool by name with validated params."""
        if name not in self._tools:
            raise ToolNotFoundError(
                f"Tool '{name}' not found. Available: {list(self._tools.keys())}"
            )

        tool_def = self._tools[name]
        validated = validate_input(params, tool_def["schema"])

        fn = tool_def["fn"]
        if tool_def["is_async"]:
            result = await fn(**validated)
        else:
            result = fn(**validated)

        return validate_output(result, tool_def["schema"])

    def list_tools(self) -> list[dict[str, Any]]:
        """Return all registered tools with their MCP-compatible schemas."""
        return [
            {
                "name": t["name"],
                "description": t["description"],
                "inputSchema": t["schema"]["input"],
                "tags": t["tags"],
            }
            for t in self._tools.values()
        ]

    def run(
        self,
        transport: str | None = None,
        host: str | None = None,
        port: int | None = None,
        reload: bool = False,
    ) -> None:
        """Start the MCP server with the configured transport."""
        transport = transport or self.config.transport
        logger.info(
            "Starting mcp-forge '%s' v%s [transport=%s]",
            self.name, self.version, transport,
        )

        if transport == "stdio":
            from mcp_forge.transports.stdio import StdioTransport
            StdioTransport(self).start()
        elif transport == "http":
            from mcp_forge.transports.http import HttpTransport
            HttpTransport(self, host=host or self.config.host, port=port or self.config.port).start(reload=reload)
        elif transport == "sse":
            from mcp_forge.transports.sse import SseTransport
            SseTransport(self, host=host or self.config.host, port=port or self.config.port).start(reload=reload)
        else:
            raise ValueError(f"Unknown transport: '{transport}'. Choose: stdio, http, sse")
