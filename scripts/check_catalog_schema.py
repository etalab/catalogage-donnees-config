import pathlib
import sys
from tabulate import tabulate

from frictionless import Resource, validate, Schema

from lib.format_text import format_error_message, format_success_message
from lib.catalog_schema import get_schema_paths


import argparse
from pathlib import Path


def main(directory: Path) -> int:
    code = 0
    for org_path in get_schema_paths(directory):
        report = validate(org_path)
        if not report.valid:
            print(format_error_message(f"{org_path} schema is not valid"))
            code = 1
            errors = report.flatten(["code", "message"])
            print(tabulate(errors, headers=["code", "message"]))
            continue
    if code == 0:
        print(format_success_message(f"Success: All data schema files are valid!"))
    return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    sys.exit(main(directory=args.directory))
