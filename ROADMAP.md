# Roadmap

> mcp-forge follows [Semantic Versioning](https://semver.org). This roadmap reflects current intent, not hard commitments.

## v0.1.x — Stability (current)

- [x] Core `Forge` class with `@tool` decorator
- [x] STDIO, HTTP, SSE transports
- [x] Pydantic v2 auto-schema generation
- [x] CLI: `new`, `run`, `list`
- [x] Contrib routers: `memory`, `filesystem`, `web`
- [x] `ForgeTestClient` for unit testing
- [x] CI matrix: Python 3.11 / 3.12 / 3.13, ruff, mypy strict, codecov
- [x] PyPI package: `pip install mcp-forge`
- [ ] 100% type coverage (mypy strict, zero ignores)
- [ ] Docstring coverage on all public APIs
- [ ] `mcp-forge validate` CLI command — validates a server against MCP spec

## v0.2.0 — Transport Completeness

- [ ] WebSocket transport (bidirectional streaming)
- [ ] OAuth 2.0 authentication middleware
- [ ] Rate limiting middleware (per-tool, per-client)
- [ ] `@resource` decorator — expose MCP resources alongside tools
- [ ] `@prompt` decorator — expose MCP prompt templates
- [ ] Hot reload in dev mode (`mcp-forge run --reload`)
- [ ] Structured logging with `structlog`

## v0.3.0 — Ecosystem

- [ ] Plugin system — third-party contrib routers via entry points
- [ ] `mcp-forge deploy` — one-command deploy to Railway / Fly.io / Docker
- [ ] OpenTelemetry tracing integration
- [ ] Async-first contrib: `database` (SQLAlchemy async), `redis`, `http_client`
- [ ] MCP client — consume remote MCP servers from Python
- [ ] Documentation site (mkdocs-material)

## v1.0.0 — Production Grade

- [ ] Stable public API with deprecation policy
- [ ] Full MCP spec 2025 compliance
- [ ] Benchmark suite vs raw FastAPI overhead
- [ ] Battle-tested in production by 3+ independent projects

---

**Want to influence the roadmap?** Open a [Discussion](https://github.com/nsfwbunny/mcp-forge/discussions) or upvote existing [issues](https://github.com/nsfwbunny/mcp-forge/issues).
