# Contributing to mcp-forge

Thank you for your interest in contributing! Here's how to get started.

## Development Setup

```bash
git clone https://github.com/nsfwbunny/mcp-forge
cd mcp-forge
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest -v
```

## Code Style

We use `ruff` for linting and formatting:

```bash
ruff check .
ruff format .
```

## Pull Request Guidelines

1. Fork the repo and create a branch from `main`
2. Add tests for any new functionality
3. Ensure `pytest` and `ruff` pass
4. Submit a PR with a clear description of the change

## Areas of Interest

- New transport implementations
- Additional contrib tools
- Performance improvements
- Documentation and examples
- Type stub improvements
