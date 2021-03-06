import pathlib
import sys

from frictionless import Resource, validate
from lib.organization import (
    get_organizations_path,
    contains_one_organization_per_file,
    get_organization_validation_report,
)

import argparse
from pathlib import Path


def main(directory: Path) -> int:
    code = 0
    for org_path in get_organizations_path(directory):
        if not contains_one_organization_per_file(org_path):
            print(
                f"an organization file must contain only one organization. Multiple organizations found in {org_path}"
            )
            code = 1
            break

        report = get_organization_validation_report(org_path)

        if not report.valid:
            code = 1
            print(report.to_summary())
            continue

    if code == 0:
        print("OK")
    return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    sys.exit(main(directory=args.directory))
