import pathlib
import sys
from tabulate import tabulate

from frictionless import Resource, validate, Schema
from lib.data_schema import get_schema_path


import argparse
from pathlib import Path


def main(directory: Path) -> int:
    code = 0
    for org_path in get_schema_path(directory):
        report = validate(org_path)
        if not report.valid:
            print(f"{org_path} schema is not valid\n")
            code = 1
            errors = report.flatten(["code", "message"])
            print(tabulate(errors, headers=["code", "message"]))
            continue
    if code == 0:
        print("OK")
    return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    sys.exit(main(directory=args.directory))
