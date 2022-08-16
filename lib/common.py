from pathlib import Path
from typing import List


def get_paths(org_dir_path: Path, file_name: str) -> List[Path]:
    org_paths: List[Path] = []
    for orgdir in Path(org_dir_path).iterdir():
        if not orgdir.is_dir() and orgdir.name == ".gitkeep":
            continue

        org_path = orgdir / file_name
        org_paths.append(org_path)

    # Order of iterdir() is not deterministic.
    # Force it for cross-platform testing purposes.
    org_paths = sorted(org_paths, key=lambda p: p.relative_to(org_dir_path))

    return org_paths
