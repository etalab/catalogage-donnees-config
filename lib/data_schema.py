from pathlib import Path
from typing import List

from .common import get_path


def get_schema_path(path: Path) -> List[Path]:
    return get_path(path, "catalog_schema.json")
