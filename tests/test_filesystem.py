"""Tests for filesystem contrib tools."""

from __future__ import annotations

import pytest
from mcp_forge import Forge
from mcp_forge.contrib.filesystem import filesystem
from mcp_forge.testing import ForgeTestClient


@pytest.fixture
def client(tmp_path, monkeypatch) -> ForgeTestClient:  # type: ignore[no-untyped-def]
    monkeypatch.chdir(tmp_path)
    app = Forge(name="fs-test")
    app.include(filesystem)
    return ForgeTestClient(app)


class TestFilesystem:
    def test_write_and_read(self, client: ForgeTestClient, tmp_path) -> None:  # type: ignore[no-untyped-def]
        path = str(tmp_path / "hello.txt")
        client.call("write_file", {"path": path, "content": "hello world"})
        assert client.call("read_file", {"path": path}) == "hello world"

    def test_write_creates_parent_dirs(self, client: ForgeTestClient, tmp_path) -> None:  # type: ignore[no-untyped-def]
        path = str(tmp_path / "a" / "b" / "c.txt")
        client.call("write_file", {"path": path, "content": "nested"})
        assert client.call("read_file", {"path": path}) == "nested"

    def test_list_dir_sorted(self, client: ForgeTestClient, tmp_path) -> None:  # type: ignore[no-untyped-def]
        (tmp_path / "z.txt").write_text("z")
        (tmp_path / "a.txt").write_text("a")
        result = client.call("list_dir", {"path": str(tmp_path)})
        assert result == sorted(result)

    def test_path_exists_true(self, client: ForgeTestClient, tmp_path) -> None:  # type: ignore[no-untyped-def]
        f = tmp_path / "exists.txt"
        f.write_text("x")
        assert client.call("path_exists", {"path": str(f)}) is True

    def test_path_exists_false(self, client: ForgeTestClient, tmp_path) -> None:  # type: ignore[no-untyped-def]
        assert client.call("path_exists", {"path": str(tmp_path / "nope.txt")}) is False

    def test_read_missing_file_raises(self, client: ForgeTestClient, tmp_path) -> None:  # type: ignore[no-untyped-def]
        with pytest.raises(FileNotFoundError):
            client.call("read_file", {"path": str(tmp_path / "ghost.txt")})

    def test_delete_file(self, client: ForgeTestClient, tmp_path) -> None:  # type: ignore[no-untyped-def]
        f = tmp_path / "del.txt"
        f.write_text("bye")
        client.call("delete_file", {"path": str(f)})
        assert not f.exists()

    def test_delete_missing_file_raises(self, client: ForgeTestClient, tmp_path) -> None:  # type: ignore[no-untyped-def]
        with pytest.raises(FileNotFoundError):
            client.call("delete_file", {"path": str(tmp_path / "nope.txt")})
