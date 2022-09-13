from pathlib import Path
import json
from typing import List


def get_paths(organization_directory_path: Path) -> List[Path]:
    paths: List[Path] = []
    for dir in Path(organization_directory_path).iterdir():
        if not dir.is_dir() and dir.name == ".gitkeep":
            continue
        paths.append(dir)

    # Order of iterdir() is not deterministic.
    # Force it for cross-platform testing purposes.
    paths = sorted(paths, key=lambda p: p.relative_to(organization_directory_path))

    return paths


def get_paths_of(organization_directory_path: Path, file_name: str) -> List[Path]:
    paths: List[Path] = []
    for path in get_paths(organization_directory_path):
        org_path = path / file_name
        paths.append(org_path)
    return paths


def transform_to_boolean_field_payload(field: json) -> json:

    return {
        "name": field["name"],
        "title": field["title"],
        "hint_text": field["description"],
        "type": "BOOL",
        "data": {
            "true_value": field["trueValues"][0],
            "false_value": field["falseValues"][0],
        },
    }


def transform_to_enum_field_payload(field: json) -> json:
    return {
        "name": field["name"],
        "title": field["title"],
        "hint_text": field["description"],
        "type": "ENUM",
        "data": {"values": field["constraints"]["enum"]},
    }


def transform_to_string_field_payload(field: json) -> json:
    return {
        "name": field["name"],
        "title": field["title"],
        "hint_text": field["description"],
        "type": "TEXT",
        "data": {},
    }


def transform_to_field_payload(field: json) -> json:

    field_type = field["type"]

    is_of_type_enum = (
        field_type == "string"
        and field.get("constraints") is not None
        and field.get("constraints").get("enum") is not None
    )

    if is_of_type_enum:
        return transform_to_enum_field_payload(field)

    if field_type == "boolean":
        return transform_to_boolean_field_payload(field)

    return transform_to_string_field_payload(field)
