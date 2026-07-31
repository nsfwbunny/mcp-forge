# ⚡ mcp-forge

> The FastAPI-style framework for building MCP servers in Python.

[![PyPI version](https://img.shields.io/pypi/v/mcp-forge.svg?style=flat-square&color=0ea5e9)](https://pypi.org/project/mcp-forge/)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg?style=flat-square)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![MCP](https://img.shields.io/badge/protocol-MCP%201.0-purple.svg?style=flat-square)](https://modelcontextprotocol.io)
[![Stars](https://img.shields.io/github/stars/nsfwbunny/mcp-forge?style=flat-square)](https://github.com/nsfwbunny/mcp-forge/stargazers)

Stop writing boilerplate MCP servers. `mcp-forge` lets you declare tools with a single decorator — schema, validation, and transport are handled automatically.

```python
from mcp_forge import Forge

app = Forge(name="my-server", version="1.0.0")

@app.tool(description="Add two numbers")
def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    app.run()  # STDIO, HTTP or SSE — your choice
```

That's it. No JSON schema by hand. No transport boilerplate. No config files.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Declarative tools** | `@app.tool()` — auto-infers schema from Python type hints |
| **Auto schema** | Pydantic v2 under the hood — full JSON Schema generation |
| **Type validation** | Input/output validated at runtime, errors surfaced cleanly |
| **Multi-transport** | STDIO (Claude Desktop), HTTP (REST), SSE (streaming) |
| **Async-first** | Native `async def` support for all tools |
| **Hot reload** | `--reload` flag for development |
| **CLI** | `mcp-forge new`, `mcp-forge run`, `mcp-forge build` |
| **Zero config** | Sensible defaults, override when needed |

---

## 🚀 Quick Start

### Install

```bash
pip install mcp-forge
```

### Create a new server

```bash
mcp-forge new my-server
cd my-server
mcp-forge run --reload
```

### Add your first tool

```python
from mcp_forge import Forge
from pydantic import BaseModel

app = Forge(name="calculator", version="1.0.0")

class SearchInput(BaseModel):
    query: str
    limit: int = 10

@app.tool(description="Search the knowledge base")
async def search(params: SearchInput) -> list[dict]:
    # your logic here
    return [{"result": f"Result for {params.query}"}]
```

### Run in different transports

```bash
# STDIO (for Claude Desktop, Cursor, VS Code)
mcp-forge run --transport stdio

# HTTP (for custom integrations)
mcp-forge run --transport http --port 8080

# SSE (for streaming)
mcp-forge run --transport sse --port 8080
```

---

## 📐 Architecture

```
mcp-forge
├── core/
│   ├── forge.py          # Main Forge class — app entrypoint
│   ├── tool.py           # @tool decorator + ToolRegistry
│   ├── schema.py         # Auto JSON Schema from type hints (Pydantic v2)
│   └── validator.py      # Input/output validation engine
├── transports/
│   ├── stdio.py          # STDIO transport (Claude Desktop compatible)
│   ├── http.py           # FastAPI-based HTTP transport
│   └── sse.py            # Server-Sent Events transport
├── cli/
│   ├── main.py           # Typer CLI — new, run, build, list
│   └── templates/        # Project scaffolding templates
└── contrib/
    ├── memory.py         # Built-in memory tool
    ├── filesystem.py     # Built-in filesystem tools
    └── web.py            # Built-in web fetch tool
```

---

## 🔌 Built-in Tools (contrib)

`mcp-forge` ships with production-ready contrib tools you can include in one line:

```python
from mcp_forge import Forge
from mcp_forge.contrib import memory, filesystem, web

app = Forge(name="full-server")
app.include(memory)      # remember(), recall(), forget()
app.include(filesystem)  # read_file(), write_file(), list_dir()
app.include(web)         # fetch_url(), search_web()
```

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
    )
)
```

Or via `mcp-forge.toml`:

```toml
[server]
name = "my-server"
version = "1.0.0"
transport = "http"
port = 8080
log_level = "info"

[tools]
max_timeout = 30
auto_reload = true
```

---

## 🧪 Testing

```python
from mcp_forge.testing import ForgeTestClient

client = ForgeTestClient(app)

def test_add():
    result = client.call("add", {"a": 2, "b": 3})
    assert result == 5
```

---

## 🌍 Ecosystem Compatibility

| Client | Transport | Status |
|---|---|---|
| Claude Desktop | STDIO | ✅ Supported |
| Cursor | STDIO | ✅ Supported |
| VS Code (Copilot) | STDIO / HTTP | ✅ Supported |
| Continue.dev | HTTP / SSE | ✅ Supported |
| Custom LLM apps | HTTP / SSE | ✅ Supported |

---

## 📦 Roadmap

- [x] `@tool` decorator with auto-schema
- [x] STDIO transport
- [x] HTTP transport (FastAPI)
- [x] SSE transport
- [x] Pydantic v2 validation
- [x] CLI (`new`, `run`, `build`)
- [ ] `@resource` decorator (MCP Resources spec)
- [ ] `@prompt` decorator (MCP Prompts spec)
- [ ] Plugin registry (community contrib tools)
- [ ] Docker one-liner deploy
- [ ] mcp-forge cloud (hosted MCP servers)

---

## 🤝 Contributing

PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
git clone https://github.com/nsfwbunny/mcp-forge
cd mcp-forge
pip install -e ".[dev]"
pytest
```

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

<p align="center">
  Built with ⚡ by <a href="https://github.com/nsfwbunny">Benni Alencar</a>
</p>
