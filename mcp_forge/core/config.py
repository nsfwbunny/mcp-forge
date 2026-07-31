"""ForgeConfig — server configuration dataclass."""

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class ForgeConfig:
    transport: Literal["stdio", "http", "sse"] = "stdio"
    host: str = "0.0.0.0"
    port: int = 8080
    log_level: Literal["debug", "info", "warning", "error"] = "info"
    cors_origins: list[str] = field(default_factory=lambda: ["*"])
    max_tool_timeout: int = 30
    auto_reload: bool = False
