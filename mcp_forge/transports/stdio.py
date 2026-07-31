"""STDIO transport — compatible with Claude Desktop, Cursor, VS Code."""

from __future__ import annotations

import asyncio
import json
import logging
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp_forge.core.forge import Forge

logger = logging.getLogger("mcp_forge.transports.stdio")


class StdioTransport:
    """
    MCP STDIO transport.
    Reads JSON-RPC messages from stdin, writes responses to stdout.
    Fully compatible with Claude Desktop's MCP client.
    """

    def __init__(self, app: "Forge") -> None:
        self.app = app

    def start(self) -> None:
        """Block and serve MCP requests over STDIO."""
        logger.info("STDIO transport active — waiting for MCP messages")
        asyncio.run(self._serve())

    async def _serve(self) -> None:
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        loop = asyncio.get_event_loop()
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        while True:
            line = await reader.readline()
            if not line:
                break
            try:
                message = json.loads(line.decode())
                response = await self._handle(message)
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            except json.JSONDecodeError as e:
                logger.error("Invalid JSON from stdin: %s", e)

    async def _handle(self, message: dict) -> dict:
        method = message.get("method", "")
        msg_id = message.get("id")

        if method == "tools/list":
            return self._ok(msg_id, {"tools": self.app.list_tools()})

        if method == "tools/call":
            params = message.get("params", {})
            tool_name = params.get("name")
            tool_input = params.get("arguments", {})
            try:
                result = await self.app.call_tool(tool_name, tool_input)
                return self._ok(msg_id, {"content": [{"type": "text", "text": json.dumps(result)}]})
            except Exception as e:
                return self._err(msg_id, str(e))

        if method == "initialize":
            return self._ok(msg_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": self.app.name, "version": self.app.version},
            })

        return self._err(msg_id, f"Unknown method: {method}")

    @staticmethod
    def _ok(msg_id: Any, result: dict) -> dict:
        return {"jsonrpc": "2.0", "id": msg_id, "result": result}

    @staticmethod
    def _err(msg_id: Any, message: str) -> dict:
        return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32603, "message": message}}
