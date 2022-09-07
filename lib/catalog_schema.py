from pathlib import Path
from typing import List, Set

from lib.constants import COMMON_SCHEMA_FIELD_NAMES

from .common import get_paths


def get_schema_paths(path: Path) -> List[Path]:
    return get_paths(path, "catalog_schema.json")


def has_field(field_name: str, field_list: List[str]) -> bool:
    return any(field_name in field for field in field_list)


def get_missing_fields(field_names: List[str]) -> Set[str]:
    return COMMON_SCHEMA_FIELD_NAMES - set(field_names)


def get_extra_fields(field_names: List[str]) -> Set[str]:
    return set(field_names) - COMMON_SCHEMA_FIELD_NAMES
