from pathlib import Path
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
    for path in get_path(organization_directory_path):
        org_path = path / file_name
        paths.append(org_path)
    return paths
