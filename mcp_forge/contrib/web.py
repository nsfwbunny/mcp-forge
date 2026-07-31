"""Built-in web tools — fetch URL content."""

from __future__ import annotations

from mcp_forge.core.forge import Forge

web = Forge(name="__web_router__")


@web.tool(description="Fetch the text content of a URL")
async def fetch_url(url: str, timeout: int = 10) -> str:
    try:
        import httpx
    except ImportError:
        raise ImportError("fetch_url requires httpx. Install with: pip install httpx")

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text
