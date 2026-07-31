# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 2026-07-31

### Added
- `Forge` class with `@app.tool()` declarative decorator
- Auto JSON Schema generation from Python type hints (Pydantic v2)
- STDIO transport — MCP spec `2024-11-05`, Claude Desktop / Cursor / VS Code compatible
- HTTP transport — FastAPI REST (`GET /tools`, `POST /tools/{name}`, `GET /health`)
- SSE transport — Server-Sent Events for streaming
- `ForgeConfig` dataclass with full server configuration
- CLI: `mcp-forge new`, `mcp-forge run`, `mcp-forge list`
- Contrib routers: `memory`, `filesystem`, `web`
- `ForgeTestClient` with sync `.call()` and async `.acall()`
- Full test suite with pytest + pytest-asyncio
- GitHub Actions CI — Python 3.11 + 3.12, ruff, mypy, auto-publish

### Fixed
- STDIO transport: all logging redirected to stderr (stdout is MCP wire channel)
- STDIO transport: `notifications/initialized` handler added (MCP spec required)
- STDIO transport: replaced deprecated `get_event_loop()` with `get_running_loop()`
- `Forge.include()`: deep-copy prevents shared mutable state between instances
- `memory` contrib: scoped `_store` per router instance, not global module
- `schema.py`: guarded `get_type_hints()` with try/except for untyped params
- HTTP transport: `Body()` for proper FastAPI request validation
- Contrib `__init__`: lazy imports prevent `ImportError` without optional extras
- `ForgeTestClient`: `nest_asyncio` fallback for running event loops
