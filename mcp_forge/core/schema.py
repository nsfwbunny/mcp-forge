"""Auto JSON Schema generation from Python type hints."""

from __future__ import annotations

import inspect
import typing
from typing import Any, get_type_hints


_PYTHON_TO_JSON_TYPE: dict[Any, str] = {
    int: "integer",
    float: "number",
    str: "string",
    bool: "boolean",
    list: "array",
    dict: "object",
    type(None): "null",
}


def build_schema(fn: Any) -> dict[str, Any]:
    """
    Build a JSON Schema dict from a Python function's type hints.
    Supports primitives, list[T], dict[str, T], Optional[T],
    and Pydantic BaseModel parameters.

    Falls back gracefully for parameters without type annotations.
    """
    try:
        hints = get_type_hints(fn)
    except Exception:
        hints = {}

    sig = inspect.signature(fn)
    properties: dict[str, Any] = {}
    required: list[str] = []

    for param_name, param in sig.parameters.items():
        if param_name in ("self", "cls"):
            continue

        annotation = hints.get(param_name, Any)
        json_type = _resolve_type(annotation)
        properties[param_name] = json_type

        if param.default is inspect.Parameter.empty:
            required.append(param_name)

    return_annotation = hints.get("return", Any)

    return {
        "input": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
        "output": _resolve_type(return_annotation),
    }


def _resolve_type(annotation: Any) -> dict[str, Any]:
    """Recursively resolve a Python type annotation to a JSON Schema fragment."""
    origin = getattr(annotation, "__origin__", None)

    # list[T]
    if origin is list:
        args = getattr(annotation, "__args__", (Any,))
        return {"type": "array", "items": _resolve_type(args[0])}

    # dict[str, T]
    if origin is dict:
        args = getattr(annotation, "__args__", (Any, Any))
        return {"type": "object", "additionalProperties": _resolve_type(args[1])}

    # Optional[T] / Union[T, None]
    if origin is typing.Union:
        args = getattr(annotation, "__args__", ())
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            resolved = _resolve_type(non_none[0])
            resolved["nullable"] = True
            return resolved
        # Multi-union: return anyOf
        return {"anyOf": [_resolve_type(a) for a in non_none]}

    # Pydantic BaseModel — lazy import so pydantic is optional
    try:
        from pydantic import BaseModel
        if isinstance(annotation, type) and issubclass(annotation, BaseModel):
            return annotation.model_json_schema()
    except ImportError:
        pass

    # Primitive fallback
    json_type = _PYTHON_TO_JSON_TYPE.get(annotation, "string")
    return {"type": json_type}
