"""Tests for contrib tools."""

from mcp_forge import Forge
from mcp_forge.contrib import memory
from mcp_forge.testing import ForgeTestClient


def test_memory_contrib() -> None:
    app = Forge(name="memory-test")
    app.include(memory)
    client = ForgeTestClient(app)

    client.call("remember", {"key": "foo", "value": "bar"})
    assert client.call("recall", {"key": "foo"}) == "bar"

    client.call("forget", {"key": "foo"})
    result = client.call("recall", {"key": "foo"})
    assert "not found" in result
