"""HTTP transport — FastAPI-based REST server."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mcp_forge.core.forge import Forge

logger = logging.getLogger("mcp_forge.transports.http")


class HttpTransport:
    """
    HTTP transport for mcp-forge.
    Exposes MCP endpoints via FastAPI:
      GET  /tools        — list all tools
      POST /tools/{name} — call a tool
      GET  /health       — health check
    """

    def __init__(self, app: "Forge", host: str = "0.0.0.0", port: int = 8080) -> None:
        self.app = app
        self.host = host
        self.port = port

    def start(self, reload: bool = False) -> None:
        try:
            from fastapi import FastAPI
            from fastapi.middleware.cors import CORSMiddleware
            import uvicorn
        except ImportError as e:
            raise ImportError(
                "HTTP transport requires 'fastapi' and 'uvicorn'. "
                "Install with: pip install mcp-forge[http]"
            ) from e

        api = FastAPI(title=self.app.name, version=self.app.version)
        api.add_middleware(
            CORSMiddleware,
            allow_origins=self.app.config.cors_origins,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        forge = self.app

        @api.get("/tools")
        async def list_tools() -> dict:
            return {"tools": forge.list_tools()}

        @api.post("/tools/{tool_name}")
        async def call_tool(tool_name: str, body: dict[str, Any]) -> dict:
            result = await forge.call_tool(tool_name, body)
            return {"result": result}

        @api.get("/health")
        async def health() -> dict:
            return {"status": "ok", "server": forge.name, "version": forge.version}

        logger.info("HTTP transport listening on http://%s:%d", self.host, self.port)
        uvicorn.run(api, host=self.host, port=self.port, reload=reload)
