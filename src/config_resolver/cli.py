"""Command line interface for :mod:`config_resolver`."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

import yaml

from .config import read_config
from .data import parse_data
from .merge import merge_dicts


def _dump(data: object) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def _parse_overrides(pairs: Sequence[str] | None) -> dict[str, object]:
    overrides: dict[str, object] = {}
    for pair in pairs or []:
        if "=" not in pair:
            raise SystemExit(f"Invalid --set value '{pair}', expected KEY=VALUE")
        key, value = pair.split("=", 1)
        try:
            overrides[key] = parse_data(value)
        except Exception:
            overrides[key] = value
    return overrides


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="config-resolver",
        description="Resolve merged configuration and parse YAML/JSON data.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    show = subparsers.add_parser("show", help="Print the merged configuration.")
    show.add_argument("--config-folder", action="append", default=None, help="Extra config folder (repeatable).")
    show.add_argument("--filename", action="append", default=None, help="Config filename to look for (repeatable).")
    show.add_argument("--start-folder", default=None, help="Folder to start the ancestor search from.")
    show.add_argument("--data-file", default=None, help="Optional data file whose 'config' key is merged in.")
    show.add_argument("--set", action="append", default=None, metavar="KEY=VALUE", help="CLI override (repeatable).")

    parse = subparsers.add_parser("parse", help="Parse an inline YAML/JSON string or file path.")
    parse.add_argument("data", help="YAML/JSON string or path to a file.")

    merge = subparsers.add_parser("merge", help="Merge YAML/JSON files and print the result.")
    merge.add_argument("files", nargs="+", help="Files to merge, later files win.")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.command == "parse":
        print(_dump(parse_data(args.data)))
        return 0

    if args.command == "merge":
        configs = [parse_data(path) for path in args.files]
        print(_dump(merge_dicts(*configs)))
        return 0

    data_config = {}
    if args.data_file:
        data_config = parse_data(args.data_file).get("config", {})
    merged = read_config(
        data_config,
        _parse_overrides(args.set),
        config_folders=args.config_folder,
        config_filenames=args.filename,
        start_folder=args.start_folder,
    )
    print(_dump(merged))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
