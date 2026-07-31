"""mcp-forge exception hierarchy."""


class ForgeError(Exception):
    """Base exception for all mcp-forge errors."""


class ToolNotFoundError(ForgeError):
    """Raised when a tool is called by name but not registered."""


class ValidationError(ForgeError):
    """Raised when tool input or output fails schema validation."""


class TransportError(ForgeError):
    """Raised when a transport fails to start or encounters a fatal error."""


class ConfigurationError(ForgeError):
    """Raised for invalid ForgeConfig values."""
