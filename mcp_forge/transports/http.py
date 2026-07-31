"""HTTP transport — FastAPI-based REST MCP server."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mcp_forge.core.forge import Forge

logger = logging.getLogger("mcp_forge.transports.http")


class HttpTransport:
    """
    HTTP transport for mcp-forge.

    Endpoints:
      GET  /health          — liveness check
      GET  /tools           — list all registered tools + schemas
      POST /tools/{name}    — call a tool with JSON body
    """

    def __init__(self, app: "Forge", host: str = "0.0.0.0", port: int = 8080) -> None:
        self.app = app
        self.host = host
        self.port = port

    def start(self, reload: bool = False) -> None:
        try:
            from fastapi import FastAPI, Body, HTTPException
            from fastapi.middleware.cors import CORSMiddleware
            import uvicorn
        except ImportError as e:
            raise ImportError(
                "HTTP transport requires 'fastapi' and 'uvicorn'. "
                "Install with: pip install mcp-forge[http]"
            ) from e

        api = FastAPI(
            title=self.app.name,
            version=self.app.version,
            description=self.app.description or f"mcp-forge MCP server: {self.app.name}",
        )
        api.add_middleware(
            CORSMiddleware,
            allow_origins=self.app.config.cors_origins,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        forge = self.app

        @api.get("/health")
        async def health() -> dict[str, str]:
            return {"status": "ok", "server": forge.name, "version": forge.version}

        @api.get("/tools")
        async def list_tools() -> dict[str, Any]:
            return {"tools": forge.list_tools()}

        @api.post("/tools/{tool_name}")
        async def call_tool(
            tool_name: str,
            body: dict[str, Any] = Body(default_factory=dict),
        ) -> dict[str, Any]:
            try:
                result = await forge.call_tool(tool_name, body)
                return {"result": result}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e)) from e

        logger.info("HTTP transport: http://%s:%d", self.host, self.port)
        uvicorn.run(api, host=self.host, port=self.port, reload=reload)
