import pathlib
import sys
from tabulate import tabulate
from frictionless import Resource, validate, Schema

from lib.format_text import format_error_message, format_success_message
from lib.catalog_schema import get_schema_paths, get_missing_fields


import argparse
from pathlib import Path


def main(directory: Path) -> int:
    code = 0
    for org_path in get_schema_paths(directory):
        try:
            schema = Schema(org_path)
            report = schema.validate()
            if not report.valid:
                print(format_error_message(f"Error: {org_path} schema is not valid"))
                code = 1
                errors = report.flatten(["code", "message"])
                print(tabulate(errors, headers=["code", "message"]))
                continue

        except FileNotFoundError as exc:
            print(format_error_message(f"Error: {exc}"))
            code = 1
            continue

        missing_fields = get_missing_fields(schema.field_names)

        if len(missing_fields) > 0:
            missing_fields_string = ",".join(missing_fields)
            print(
                format_error_message(
                    f"Error: {missing_fields_string} fields are missing in the schema in {org_path}"
                )
            )
            code = 1

    if code == 0:

        print(format_success_message(f"Success: All data schema files are valid!"))

    return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    sys.exit(main(directory=args.directory))
