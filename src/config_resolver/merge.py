"""Dictionary merging helpers."""

from __future__ import annotations

from typing import Any, Mapping

__all__ = ["merge_dicts"]


def merge_dicts(*configs: Mapping[str, Any] | None) -> dict[str, Any]:
    """Shallow-merge mappings from left to right.

    ``None`` mappings and ``None`` values are skipped so that later layers can
    explicitly leave earlier values untouched.
    """

    result: dict[str, Any] = {}
    for config in configs:
        if not config:
            continue
        for key, value in config.items():
            if value is not None:
                result[key] = value
    return result
