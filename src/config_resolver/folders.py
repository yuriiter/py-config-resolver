"""Filesystem helpers used by generated-output workflows."""

from __future__ import annotations

import datetime
import hashlib
import os

__all__ = ["create_folder_if_not_exists", "generate_folder_name"]


def create_folder_if_not_exists(folder_path: str | os.PathLike[str]) -> str:
    """Create ``folder_path`` (relative to the cwd) when missing.

    Returns the (possibly absolute) path that was created or already existed.
    """

    full_path = os.fspath(folder_path)
    if not os.path.isabs(full_path):
        full_path = os.path.join(os.getcwd(), full_path)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    return full_path


def generate_folder_name(moment: datetime.datetime | None = None) -> str:
    """Return a sortable, collision-resistant folder name.

    Format: ``%d_%m_%Y_%H_%M_%S_<4 hex chars>``.
    """

    current_time = moment or datetime.datetime.now()
    formatted_time = current_time.strftime("%d_%m_%Y_%H_%M_%S")
    hash_value = hashlib.md5(formatted_time.encode()).hexdigest()[:4]
    return f"{formatted_time}_{hash_value}"
