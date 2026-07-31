"""STDIO transport — compatible with Claude Desktop, Cursor, VS Code.

CRITICAL: All logging MUST go to stderr. stdout is the MCP wire channel —
any non-JSON bytes written there will corrupt the protocol stream.
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mcp_forge.core.forge import Forge

# Force all log output to stderr — never stdout on STDIO transport
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("mcp_forge.transports.stdio")


class StdioTransport:
    """
    MCP STDIO transport.
    Reads newline-delimited JSON-RPC 2.0 messages from stdin,
    writes responses to stdout.
    Fully compatible with Claude Desktop, Cursor, and VS Code MCP clients.
    """

    def __init__(self, app: "Forge") -> None:
        self.app = app

    def start(self) -> None:
        """Block and serve MCP requests over STDIO."""
        logger.info("STDIO transport active — server='%s' v%s", self.app.name, self.app.version)
        asyncio.run(self._serve())

    async def _serve(self) -> None:
        loop = asyncio.get_running_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        # stdout writer — binary mode for reliable newline handling
        writer_transport, writer_protocol = await loop.connect_write_pipe(
            asyncio.BaseProtocol, sys.stdout.buffer
        )

        while True:
            line = await reader.readline()
            if not line:
                logger.info("STDIO: stdin closed, shutting down")
                break
            try:
                message = json.loads(line.decode("utf-8"))
                response = await self._handle(message)
                if response is not None:
                    out = json.dumps(response, ensure_ascii=False) + "\n"
                    writer_transport.write(out.encode("utf-8"))
            except json.JSONDecodeError as e:
                logger.error("Invalid JSON from stdin: %s | raw: %r", e, line[:120])

    async def _handle(self, message: dict[str, Any]) -> dict[str, Any] | None:
        method = message.get("method", "")
        msg_id = message.get("id")

        # MCP spec: client sends this after initialize — no response expected
        if method == "notifications/initialized":
            logger.info("MCP client initialized")
            return None

        if method == "initialize":
            return self._ok(msg_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": self.app.name, "version": self.app.version},
            })

        if method == "tools/list":
            return self._ok(msg_id, {"tools": self.app.list_tools()})

        if method == "tools/call":
            params = message.get("params", {})
            tool_name = params.get("name", "")
            tool_input = params.get("arguments", {})
            try:
                result = await self.app.call_tool(tool_name, tool_input)
                return self._ok(msg_id, {
                    "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}],
                    "isError": False,
                })
            except Exception as e:
                logger.error("Tool '%s' raised: %s", tool_name, e)
                return self._err(msg_id, str(e))

        # Unknown method — return JSON-RPC method not found
        return self._err(msg_id, f"Method not found: {method}", code=-32601)

    @staticmethod
    def _ok(msg_id: Any, result: dict[str, Any]) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": msg_id, "result": result}

    @staticmethod
    def _err(msg_id: Any, message: str, code: int = -32603) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}
