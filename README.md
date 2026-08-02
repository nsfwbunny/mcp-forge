# ⚡ mcp-forge

> The FastAPI-style framework for building MCP servers in Python.

[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg?style=flat-square)](https://www.python.org)
[![PyPI](https://img.shields.io/pypi/v/mcp-forge.svg?style=flat-square)](https://pypi.org/project/mcp-forge/)
[![Downloads](https://img.shields.io/pypi/dm/mcp-forge?style=flat-square&color=blue)](https://pypi.org/project/mcp-forge/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![MCP](https://img.shields.io/badge/protocol-MCP%202024--11--05-purple.svg?style=flat-square)](https://modelcontextprotocol.io)
[![CI](https://img.shields.io/github/actions/workflow/status/benni-os/mcp-forge/ci.yml?branch=main&style=flat-square&label=CI)](https://github.com/benni-os/mcp-forge/actions)
[![Coverage](https://img.shields.io/codecov/c/github/benni-os/mcp-forge?style=flat-square)](https://codecov.io/gh/benni-os/mcp-forge)
[![mypy](https://img.shields.io/badge/type--checked-mypy%20strict-informational?style=flat-square)](https://mypy.readthedocs.io)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square)](https://github.com/astral-sh/ruff)

Stop writing boilerplate MCP servers.

`mcp-forge` is a production-grade framework for the [Model Context Protocol](https://modelcontextprotocol.io) — inspired by FastAPI's declarative style. You define tools as typed Python functions. Schema generation, input validation, and transport wiring are automatic.

```python
from mcp_forge import Forge

app = Forge(name="my-server", version="1.0.0")

@app.tool(description="Search the knowledge base")
async def search(query: str, limit: int = 10) -> list[dict]:
    return [{"title": f"Result for {query}"}]  # your logic here

if __name__ == "__main__":
    app.run()  # STDIO by default — Claude Desktop / Cursor / VS Code ready
```

No JSON schema by hand. No transport boilerplate. No config files.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Declarative tools** | `@app.tool()` — auto-infers JSON Schema from Python type hints |
| **Auto schema** | Pydantic v2 under the hood — full draft-07 JSON Schema generation |
| **Runtime validation** | Input validated before execution, errors surfaced as MCP-spec errors |
| **Multi-transport** | STDIO · HTTP (FastAPI) · SSE — switch with one flag |
| **Async-first** | `async def` and `def` tools work side by side |
| **Contrib tools** | `memory`, `filesystem`, `web` — production-ready, one-line include |
| **Testing client** | `ForgeTestClient` — sync and async, no running server needed |
| **CLI** | `mcp-forge new` · `mcp-forge run --reload` · `mcp-forge list` |
| **PEP 561 typed** | Ships `py.typed` — full mypy strict / pyright support |
| **Zero dependencies*** | Core needs only `pydantic>=2.0` — transports are optional extras |

> *Transport extras: `pip install mcp-forge[http]`, `mcp-forge[sse]`, `mcp-forge[all]`*

---

## 🚀 Quick Start

```bash
pip install mcp-forge
mcp-forge new my-server
cd my-server
mcp-forge run --reload
```

That's a running MCP server. Connect it to Claude Desktop:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my_server"]
    }
  }
}
```

---

## 📐 Architecture

```
mcp-forge
├── core/
│   ├── forge.py          # Forge class — declarative app entrypoint
│   ├── schema.py         # Auto JSON Schema from Pydantic v2 type hints
│   ├── validator.py      # Input/output validation engine
│   ├── config.py         # ForgeConfig dataclass
│   └── exceptions.py     # MCP-aligned exception hierarchy
├── transports/
│   ├── stdio.py          # STDIO — MCP spec 2024-11-05 compliant
│   ├── http.py           # HTTP — FastAPI-based REST transport
│   └── sse.py            # SSE — Server-Sent Events streaming transport
├── cli/
│   └── main.py           # Typer CLI — new, run, list, build
└── contrib/
    ├── memory.py         # In-process memory store (scoped per Forge instance)
    ├── filesystem.py     # Safe filesystem tools with path sandboxing
    └── web.py            # HTTP fetch with timeout and error handling
```

**Design principles:**
- Transport is a runtime concern — your tool code never changes between STDIO, HTTP, and SSE
- Schema is derived, never written — if your types are correct, your schema is correct
- Contrib tools are opt-in — `app.include(memory)` adds 4 tools; you stay in control

---

## 🔌 Contrib Tools

```python
from mcp_forge import Forge
from mcp_forge.contrib import memory, filesystem, web

app = Forge(name="full-server")
app.include(memory)      # remember(), recall(), forget(), list_memory()
app.include(filesystem)  # read_file(), write_file(), list_dir(), delete_file()
app.include(web)         # fetch_url()
```

Each contrib router carries its own isolated state. Safe to include in multiple `Forge` instances within the same process.

---

## ⚙️ Configuration

```python
from mcp_forge import Forge, ForgeConfig

app = Forge(
    name="my-server",
    version="1.0.0",
    config=ForgeConfig(
        transport="http",
        port=8080,
        log_level="info",
        cors_origins=["*"],
        max_tool_timeout=30,
    ),
)
```

Or via `mcp-forge.toml` at the project root:

```toml
[server]
name = "my-server"
version = "1.0.0"
transport = "http"
port = 8080

[tools]
max_timeout = 30
auto_reload = true
```

---

## 🧪 Testing

`ForgeTestClient` calls tools directly — no server, no sockets, no mocking required.

```python
from mcp_forge.testing import ForgeTestClient

client = ForgeTestClient(app)

def test_add():
    assert client.call("add", {"a": 2, "b": 3}) == 5

async def test_search_async():
    results = await client.acall("search", {"query": "mcp"})
    assert isinstance(results, list)
```

Works with `pytest` and `pytest-asyncio` out of the box.

---

## 🌍 Ecosystem Compatibility

| Client | Transport | Status |
|---|---|---|
| Claude Desktop | STDIO | ✅ Tested |
| Cursor | STDIO | ✅ Tested |
| VS Code (GitHub Copilot) | STDIO · HTTP | ✅ Tested |
| Continue.dev | HTTP · SSE | ✅ Tested |
| Custom LLM agents | HTTP · SSE | ✅ Tested |
| JARVAS-2 (Benni OS) | HTTP · STDIO | ✅ Tested |

---

## 🤝 Contributing

PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
git clone https://github.com/benni-os/mcp-forge
cd mcp-forge
pip install -e ".[dev]"
pytest
```

Found a bug? [Open an issue](https://github.com/benni-os/mcp-forge/issues/new/choose).  
Have an idea? [Start a discussion](https://github.com/benni-os/mcp-forge/discussions).

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

<p align="center">
  Part of the <strong>Benni OS</strong> open source ecosystem &mdash;
  built and maintained by <a href="https://github.com/benni-os">@benni-os</a>
</p>
