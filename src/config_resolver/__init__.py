"""Reusable configuration resolution and YAML/JSON parsing utilities."""

from .config import (
    DEFAULT_CONFIG_FILENAMES,
    DEFAULT_CONFIG_FOLDERS,
    read_config,
    search_config_folders,
)
from .data import get_file_content, load_json, load_yaml, parse_data
from .folders import create_folder_if_not_exists, generate_folder_name
from .merge import merge_dicts

__version__ = "0.1.0"

__all__ = [
    "DEFAULT_CONFIG_FILENAMES",
    "DEFAULT_CONFIG_FOLDERS",
    "create_folder_if_not_exists",
    "generate_folder_name",
    "get_file_content",
    "load_json",
    "load_yaml",
    "merge_dicts",
    "parse_data",
    "read_config",
    "search_config_folders",
    "__version__",
]
