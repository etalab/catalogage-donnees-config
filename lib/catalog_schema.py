from pathlib import Path
from typing import List

from .common import get_paths


def get_schema_paths(path: Path) -> List[Path]:
    return get_paths(path, "catalog_schema.json")
