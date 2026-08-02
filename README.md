<div align="center">

<br />

<img src="https://raw.githubusercontent.com/nsfwbunny/mcp-forge/main/.github/assets/logo.svg" alt="mcp-forge" width="72" />

# mcp-forge

**The FastAPI-style framework for building MCP servers in Python.**

Declarative tools. Auto-schema. Type-safe. Production-ready.

<br />

[![PyPI version](https://img.shields.io/pypi/v/mcp-forge?style=for-the-badge&logo=pypi&logoColor=white&color=0066FF)](https://pypi.org/project/mcp-forge/)
[![Python](https://img.shields.io/badge/python-3.11_%7C_3.12_%7C_3.13-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![CI](https://img.shields.io/github/actions/workflow/status/nsfwbunny/mcp-forge/ci.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white&label=CI)](https://github.com/nsfwbunny/mcp-forge/actions)
[![Coverage](https://img.shields.io/codecov/c/github/nsfwbunny/mcp-forge?style=for-the-badge&logo=codecov&logoColor=white)](https://codecov.io/gh/nsfwbunny/mcp-forge)
[![License: MIT](https://img.shields.io/badge/license-MIT-22c55e?style=for-the-badge)](LICENSE)
[![mypy](https://img.shields.io/badge/mypy-strict-6366f1?style=for-the-badge&logo=python&logoColor=white)](https://mypy.readthedocs.io)

<br />

[**Quick Start**](#-quick-start) &nbsp;&bull;&nbsp;
[**Documentation**](#-features) &nbsp;&bull;&nbsp;
[**Examples**](#-examples) &nbsp;&bull;&nbsp;
[**Roadmap**](ROADMAP.md) &nbsp;&bull;&nbsp;
[**Contributing**](CONTRIBUTING.md)

<br />

<!-- demo gif: replace the src below with your actual recording -->
<img src="https://raw.githubusercontent.com/nsfwbunny/mcp-forge/main/.github/assets/demo.gif" alt="mcp-forge demo" width="720" />

<br />

</div>

---

## Why mcp-forge?

Every MCP server you write starts the same way: hand-craft JSON Schema, wire a transport loop, handle `notifications/initialized`, redirect stderr, copy-paste validation logic. It's the same boilerplate every time.

**mcp-forge eliminates all of it.** You write a typed Python function. The framework derives the schema from your type hints, validates inputs at runtime, and exposes the tool over any transport — STDIO, HTTP, or SSE — without changing a single line of your logic.

Think of it as the **FastAPI moment for MCP servers**.

```python
from mcp_forge import Forge

app = Forge(name="my-server", version="1.0.0")

@app.tool(description="Search the knowledge base")
async def search(query: str, limit: int = 10) -> list[dict]:
    """Returns ranked results for the given query."""
    ...  # your logic here

if __name__ == "__main__":
    app.run()  # STDIO — Claude Desktop / Cursor / VS Code ready
```

No JSON Schema by hand. No transport boilerplate. No config files.

---

## ⚡ Quick Start

```bash
pip install mcp-forge
mcp-forge new my-server && cd my-server
mcp-forge run --reload
```

Connect to **Claude Desktop** in 30 seconds:

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

Switch to **HTTP** transport with one flag:

```bash
mcp-forge run --transport http --port 8080
```

---

## ✨ Features

<table>
<tr>
<td width="50%">

**🏗️ Declarative Tools**
Define tools as typed Python functions with `@app.tool()`. No schema files, no registration calls.

**🧠 Auto JSON Schema**
Pydantic v2 under the hood. Full draft-07 JSON Schema generated from your type hints — automatically.

**✅ Runtime Validation**
Inputs validated before execution. Errors surface as proper MCP-spec error responses.

**🚀 Multi-Transport**
STDIO · HTTP · SSE. Switch transports at runtime — your tool code never changes.

</td>
<td width="50%">

**⏳ Async-First**
`async def` and `def` tools work side by side. No event loop management needed.

**🔌 Contrib Routers**
`memory` · `filesystem` · `web` — production-ready tools, one-line include.

**🧪 Testing Client**
`ForgeTestClient` calls tools directly — no running server, no mocking, no sockets.

**📦 PEP 561 Typed**
Ships `py.typed`. Full `mypy --strict` and Pyright support out of the box.

</td>
</tr>
</table>

---

## 📚 Examples

### Minimal server — 3 lines of logic

```python
from mcp_forge import Forge

app = Forge(name="calculator")

@app.tool()
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@app.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

app.run()
```

### With contrib tools

```python
from mcp_forge import Forge
from mcp_forge.contrib import memory, filesystem, web

app = Forge(name="agent-tools")
app.include(memory)      # remember(), recall(), forget(), list_memory()
app.include(filesystem)  # read_file(), write_file(), list_dir(), delete_file()
app.include(web)         # fetch_url()

app.run()
```

### HTTP transport with custom config

```python
from mcp_forge import Forge, ForgeConfig

app = Forge(
    name="api-server",
    config=ForgeConfig(
        transport="http",
        port=8080,
        cors_origins=["*"],
        max_tool_timeout=30,
    ),
)

@app.tool()
async def summarize(text: str, max_words: int = 100) -> str:
    """Summarize text to a given word count."""
    ...

app.run()
```

### Unit testing — no server needed

```python
from mcp_forge.testing import ForgeTestClient

client = ForgeTestClient(app)

def test_add():
    result = client.call("add", {"a": 2, "b": 3})
    assert result == 5

async def test_summarize_async():
    result = await client.acall("summarize", {"text": "Hello world"})
    assert isinstance(result, str)
```

---

## 📐 Architecture

```
mcp-forge
├── core/
│   ├── forge.py        ← Forge class — declarative app entrypoint
│   ├── schema.py       ← Auto JSON Schema from Pydantic v2 type hints
│   ├── validator.py    ← Input/output validation engine
│   ├── config.py       ← ForgeConfig dataclass
│   └── exceptions.py   ← MCP-aligned exception hierarchy
├── transports/
│   ├── stdio.py        ← STDIO — MCP spec 2024-11-05 compliant
│   ├── http.py         ← HTTP — FastAPI-based REST transport
│   └── sse.py          ← SSE — Server-Sent Events streaming
├── cli/
│   └── main.py         ← Typer CLI — new, run, list, build
└── contrib/
    ├── memory.py       ← Scoped in-process memory store
    ├── filesystem.py   ← Safe filesystem tools with path sandboxing
    └── web.py          ← HTTP fetch with timeout and error handling
```

**Design principles:**

- **Transport is a runtime concern** — your tool code never changes between STDIO, HTTP, and SSE
- **Schema is derived, never written** — if your types are correct, your schema is correct
- **Contrib is opt-in** — `app.include(memory)` adds tools; you stay in control
- **Strict by default** — mypy strict, ruff format + lint, 100% typed public API

---

## 🌍 Ecosystem Compatibility

| Client | Transport | Status |
|:--|:--|:--|
| Claude Desktop | STDIO | ✅ Tested |
| Cursor | STDIO | ✅ Tested |
| VS Code (GitHub Copilot) | STDIO · HTTP | ✅ Tested |
| Continue.dev | HTTP · SSE | ✅ Tested |
| Custom LLM agents | HTTP · SSE | ✅ Tested |

---

## 📦 Installation

```bash
# Core only (STDIO transport)
pip install mcp-forge

# With HTTP + SSE transports
pip install "mcp-forge[http]"

# Everything
pip install "mcp-forge[all]"
```

**Requires:** Python 3.11+ &nbsp;·&nbsp; pydantic>=2.0

---

## 🤝 Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

```bash
git clone https://github.com/nsfwbunny/mcp-forge
cd mcp-forge
pip install -e ".[dev]"
pytest
```

- 🐛 **Found a bug?** → [Open an issue](https://github.com/nsfwbunny/mcp-forge/issues/new?template=bug_report.md)
- 💡 **Have an idea?** → [Start a discussion](https://github.com/nsfwbunny/mcp-forge/discussions)
- 📜 **See what's planned** → [ROADMAP.md](ROADMAP.md)

---

<div align="center">

<br />

Built by [**Benni Alencar**](https://github.com/nsfwbunny) &nbsp;&middot;&nbsp;
Part of the **Benni OS** open-source ecosystem

<br />

<sub>If mcp-forge saves you time, consider giving it a ⭐</sub>

</div>
