"""Tests for the validation engine."""

from __future__ import annotations

import pytest
from mcp_forge import Forge
from mcp_forge.testing import ForgeTestClient
from mcp_forge.core.exceptions import ValidationError


def test_validate_output_null_guard() -> None:
    """Tools that declare a non-nullable return type must not return None."""
    app = Forge(name="validator-test")

    @app.tool(description="Should not return None")
    def bad_tool(x: int) -> str:  # declares str, returns None
        return None  # type: ignore[return-value]

    client = ForgeTestClient(app)
    with pytest.raises(ValidationError, match="returned None"):
        client.call("bad_tool", {"x": 1})


def test_validate_output_allows_none_on_nullable() -> None:
    """Optional[str] return type must allow None without raising."""
    app = Forge(name="nullable-test")

    @app.tool(description="Nullable return")
    def maybe_tool(x: int) -> str | None:
        return None

    client = ForgeTestClient(app)
    assert client.call("maybe_tool", {"x": 1}) is None
