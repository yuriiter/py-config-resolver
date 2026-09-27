"""YAML/JSON parsing helpers.

The public entry point is :func:`parse_data`, which accepts a path (relative to
the current working directory or absolute) or an inline JSON/YAML string.
"""

from __future__ import annotations

import json
import os
from typing import Any

import yaml

__all__ = ["parse_data", "get_file_content", "load_yaml", "load_json"]


def _parse_text(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:  # pragma: no cover - defensive
            raise ValueError("Invalid JSON or YAML data provided") from exc


def parse_data(data_path_or_string: Any) -> Any:
    """Parse JSON/YAML from a file path, an inline string, or pass through mappings.

    Mirrors the original ``mcv.utils.parse_data`` behaviour but avoids opening
    arbitrary long strings as filesystem paths.
    """

    if isinstance(data_path_or_string, (dict, list)):
        return data_path_or_string

    if isinstance(data_path_or_string, os.PathLike):
        data_path_or_string = os.fspath(data_path_or_string)

    if isinstance(data_path_or_string, str):
        candidate = data_path_or_string
        if not os.path.isabs(candidate):
            candidate = os.path.join(os.getcwd(), candidate)
        if os.path.isfile(candidate):
            with open(candidate, "r", encoding="utf-8") as handle:
                return _parse_text(handle.read())

    return _parse_text(data_path_or_string)


def load_yaml(path: str | os.PathLike[str]) -> Any:
    """Load a YAML file by path (relative paths resolve against the cwd)."""

    full_path = path if os.path.isabs(os.fspath(path)) else os.path.join(os.getcwd(), os.fspath(path))
    with open(full_path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_json(path: str | os.PathLike[str]) -> Any:
    """Load a JSON file by path (relative paths resolve against the cwd)."""

    full_path = path if os.path.isabs(os.fspath(path)) else os.path.join(os.getcwd(), os.fspath(path))
    with open(full_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def get_file_content(path: str | os.PathLike[str]) -> str:
    """Read a text file, resolving relative paths against the cwd."""

    full_path = path if os.path.isabs(os.fspath(path)) else os.path.join(os.getcwd(), os.fspath(path))
    with open(full_path, "r", encoding="utf-8") as handle:
        return handle.read()
