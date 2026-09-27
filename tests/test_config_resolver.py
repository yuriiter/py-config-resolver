import os
from pathlib import Path

from config_resolver import (
    generate_folder_name,
    merge_dicts,
    parse_data,
    read_config,
    search_config_folders,
)


def test_parse_inline_yaml_and_json():
    assert parse_data("a: 1") == {"a": 1}
    assert parse_data('{"a": 1}') == {"a": 1}
    assert parse_data({"already": "parsed"}) == {"already": "parsed"}


def test_parse_file(tmp_path, monkeypatch):
    config = tmp_path / "data.yaml"
    config.write_text("name: Ada\n")
    monkeypatch.chdir(tmp_path)
    assert parse_data("data.yaml") == {"name": "Ada"}
    assert parse_data(str(config)) == {"name": "Ada"}


def test_merge_dicts_skips_none():
    assert merge_dicts({"a": 1, "b": 2}, {"b": None, "c": 3}) == {"a": 1, "b": 2, "c": 3}


def test_search_config_folders(tmp_path, monkeypatch):
    (tmp_path / ".mcv.config.yaml").write_text("x: 1\n")
    child = tmp_path / "a" / "b"
    child.mkdir(parents=True)
    monkeypatch.chdir(child)
    folders = search_config_folders([".mcv.config.yaml"])
    assert folders[-1] == str(tmp_path)
    assert os.getcwd() not in folders


def test_read_config_priority(tmp_path, monkeypatch):
    (tmp_path / ".mcv.config.yaml").write_text("a: root\nb: root\n")
    child = tmp_path / "child"
    child.mkdir()
    (child / ".mcv.config.yaml").write_text("b: child\n")
    monkeypatch.chdir(child)

    merged = read_config(
        {"c": "data"},
        {"a": "cli"},
        config_folders=[],
        config_filenames=[".mcv.config.yaml"],
    )
    assert merged == {"a": "cli", "b": "child", "c": "data"}


def test_generate_folder_name_format():
    name = generate_folder_name()
    date_part, hash_part = name.rsplit("_", 1)
    assert len(hash_part) == 4
    assert len(date_part.split("_")) == 6
