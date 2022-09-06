from pathlib import Path
from typing import List


def get_paths(org_dir_path: Path, file_name: str) -> List[Path]:
    paths: List[Path] = []
    for dir in Path(org_dir_path).iterdir():
        if not dir.is_dir() and dir.name == ".gitkeep":
            continue

        org_path = dir / file_name
        paths.append(org_path)

    # Order of iterdir() is not deterministic.
    # Force it for cross-platform testing purposes.
    paths = sorted(paths, key=lambda p: p.relative_to(org_dir_path))

    return paths
