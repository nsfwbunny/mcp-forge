"""SSE (Server-Sent Events) transport."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import TYPE_CHECKING, AsyncGenerator

if TYPE_CHECKING:
    from mcp_forge.core.forge import Forge

logger = logging.getLogger("mcp_forge.transports.sse")


class SseTransport:
    """
    SSE transport — streaming MCP responses via Server-Sent Events.
    Compatible with LLM clients that support SSE-based MCP.
    """

    def __init__(self, app: "Forge", host: str = "0.0.0.0", port: int = 8080) -> None:
        self.app = app
        self.host = host
        self.port = port

    def start(self, reload: bool = False) -> None:
        try:
            from fastapi import FastAPI
            from fastapi.responses import StreamingResponse
            import uvicorn
        except ImportError as e:
            raise ImportError(
                "SSE transport requires 'fastapi' and 'uvicorn'. "
                "Install with: pip install mcp-forge[sse]"
            ) from e

        api = FastAPI(title=f"{self.app.name} (SSE)", version=self.app.version)
        forge = self.app

        @api.post("/tools/{tool_name}/stream")
        async def stream_tool(tool_name: str, body: dict) -> StreamingResponse:
            async def event_generator() -> AsyncGenerator[str, None]:
                try:
                    result = await forge.call_tool(tool_name, body)
                    payload = json.dumps({"type": "result", "data": result})
                    yield f"data: {payload}\n\n"
                except Exception as e:
                    error = json.dumps({"type": "error", "message": str(e)})
                    yield f"data: {error}\n\n"
                yield "data: {\"type\": \"done\"}\n\n"

            return StreamingResponse(event_generator(), media_type="text/event-stream")

        logger.info("SSE transport listening on http://%s:%d", self.host, self.port)
        uvicorn.run(api, host=self.host, port=self.port, reload=reload)
