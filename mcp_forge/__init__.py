"""
mcp-forge — The FastAPI-style framework for building MCP servers in Python.
"""

__version__ = "0.1.1"
__author__ = "Benni Alencar"
__license__ = "MIT"

from mcp_forge.core.forge import Forge
from mcp_forge.core.config import ForgeConfig
from mcp_forge.core.tool import tool
from mcp_forge.core.exceptions import ForgeError, ToolNotFoundError, ValidationError

__all__ = [
    "Forge",
    "ForgeConfig",
    "tool",
    "ForgeError",
    "ToolNotFoundError",
    "ValidationError",
]
