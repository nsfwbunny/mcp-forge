"""Core tests for mcp-forge."""

import pytest
from mcp_forge import Forge
from mcp_forge.testing import ForgeTestClient
from mcp_forge.core.exceptions import ToolNotFoundError, ValidationError


@pytest.fixture
def app() -> Forge:
    forge = Forge(name="test-server", version="0.1.0")

    @forge.tool(description="Add two integers")
    def add(a: int, b: int) -> int:
        return a + b

    @forge.tool(description="Greet someone")
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    @forge.tool(description="Async echo")
    async def echo(message: str) -> str:
        return message

    return forge


@pytest.fixture
def client(app: Forge) -> ForgeTestClient:
    return ForgeTestClient(app)


class TestToolRegistration:
    def test_registers_sync_tool(self, app: Forge) -> None:
        tools = {t["name"] for t in app.list_tools()}
        assert "add" in tools

    def test_registers_async_tool(self, app: Forge) -> None:
        tools = {t["name"] for t in app.list_tools()}
        assert "echo" in tools

    def test_tool_has_description(self, app: Forge) -> None:
        tool = next(t for t in app.list_tools() if t["name"] == "add")
        assert tool["description"] == "Add two integers"

    def test_tool_has_schema(self, app: Forge) -> None:
        tool = next(t for t in app.list_tools() if t["name"] == "add")
        assert "properties" in tool["inputSchema"]
        assert "a" in tool["inputSchema"]["properties"]
        assert "b" in tool["inputSchema"]["properties"]


class TestToolExecution:
    def test_sync_tool_executes(self, client: ForgeTestClient) -> None:
        assert client.call("add", {"a": 2, "b": 3}) == 5

    def test_async_tool_executes(self, client: ForgeTestClient) -> None:
        assert client.call("echo", {"message": "hello"}) == "hello"

    def test_string_tool_executes(self, client: ForgeTestClient) -> None:
        assert client.call("greet", {"name": "World"}) == "Hello, World!"

    def test_type_coercion(self, client: ForgeTestClient) -> None:
        # String inputs should be coerced to int
        assert client.call("add", {"a": "10", "b": "20"}) == 30


class TestErrors:
    def test_tool_not_found(self, client: ForgeTestClient) -> None:
        with pytest.raises(ToolNotFoundError):
            client.call("nonexistent_tool", {})

    def test_missing_required_param(self, client: ForgeTestClient) -> None:
        with pytest.raises(ValidationError):
            client.call("add", {"a": 1})  # missing 'b'
