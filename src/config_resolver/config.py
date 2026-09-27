"""Hierarchical configuration discovery and merging.

Searches a set of well-known system locations plus the current directory and
its ancestors for config files, then merges them (lowest to highest priority)
together with a data-file config and CLI overrides.
"""

from __future__ import annotations

import os
from typing import Any, Iterable, Mapping

from .data import parse_data
from .merge import merge_dicts

__all__ = [
    "DEFAULT_CONFIG_FOLDERS",
    "DEFAULT_CONFIG_FILENAMES",
    "search_config_folders",
    "read_config",
]

DEFAULT_CONFIG_FOLDERS = [
    "/etc/mcv/",
    "~/.config/mcv/",
]

DEFAULT_CONFIG_FILENAMES = [
    ".mcv.config.json",
    ".mcv.config.yaml",
]


def search_config_folders(
    possible_filenames: Iterable[str],
    start_folder: str | None = None,
) -> list[str]:
    """Return folders (ancestors of ``start_folder``) that contain a config file.

    The returned list is ordered from the highest ancestor down to the starting
    folder, so later entries take precedence when merged.
    """

    config_folders: list[str] = []
    current_folder = start_folder or os.getcwd()
    while current_folder != os.path.dirname(current_folder):
        for config_filename in possible_filenames:
            if os.path.exists(os.path.join(current_folder, config_filename)):
                config_folders.insert(0, current_folder)
                break
        current_folder = os.path.dirname(current_folder)

    return config_folders


def read_config(
    data_file_config: Mapping[str, Any] | None,
    cli_config: Mapping[str, Any] | None,
    config_folders: Iterable[str] | None = None,
    config_filenames: Iterable[str] | None = None,
    start_folder: str | None = None,
) -> dict[str, Any]:
    """Resolve and merge configuration from every layer.

    Priority (highest last): system folders, project ancestors, data-file
    config, CLI arguments.
    """

    filenames = list(config_filenames or DEFAULT_CONFIG_FILENAMES)
    folders = [os.path.expanduser(folder) for folder in (config_folders or DEFAULT_CONFIG_FOLDERS)]

    folders.extend(search_config_folders(filenames, start_folder=start_folder))

    configs: list[Mapping[str, Any]] = []

    for folder in folders:
        for filename in filenames:
            full_path = os.path.join(folder, filename)
            if os.path.exists(full_path):
                try:
                    configs.append(parse_data(full_path))
                except Exception:
                    pass

    configs.append(data_file_config or {})
    configs.append(cli_config or {})

    return merge_dicts(*configs)
