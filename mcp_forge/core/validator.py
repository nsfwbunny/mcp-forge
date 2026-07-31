"""Input/output validation engine."""

from __future__ import annotations

from typing import Any

from mcp_forge.core.exceptions import ValidationError


def validate_input(params: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    """
    Validate and coerce tool input params against the JSON Schema.
    Returns a clean dict ready to unpack into the tool function.
    """
    input_schema = schema.get("input", {})
    properties = input_schema.get("properties", {})
    required = input_schema.get("required", [])

    # Check required fields
    missing = [f for f in required if f not in params]
    if missing:
        raise ValidationError(f"Missing required fields: {missing}")

    # Coerce types
    coerced: dict[str, Any] = {}
    for key, value in params.items():
        if key in properties:
            coerced[key] = _coerce(value, properties[key])
        else:
            coerced[key] = value

    return coerced


def validate_output(result: Any, schema: dict[str, Any]) -> Any:
    """Validate tool output — currently passthrough, extensible."""
    return result


def _coerce(value: Any, type_def: dict[str, Any]) -> Any:
    """Best-effort type coercion for common JSON types."""
    t = type_def.get("type")
    try:
        if t == "integer":
            return int(value)
        elif t == "number":
            return float(value)
        elif t == "boolean":
            if isinstance(value, str):
                return value.lower() in ("true", "1", "yes")
            return bool(value)
        elif t == "string":
            return str(value)
    except (ValueError, TypeError) as e:
        raise ValidationError(f"Cannot coerce '{value}' to {t}: {e}") from e
    return value
