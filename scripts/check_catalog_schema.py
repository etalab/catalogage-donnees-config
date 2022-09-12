import pathlib
import sys
from tabulate import tabulate
from frictionless import Resource, validate, Schema, FrictionlessException
from typing import Set

from lib.format_text import format_error_message, format_success_message
from lib.catalog_schema import (
    get_schema_paths,
    get_missing_fields,
    get_extra_fields,
    get_unsupported_constraints,
)

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

        except FrictionlessException as exc:
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
            break

        extra_fields = get_extra_fields(schema.field_names)

        for extra_field in extra_fields:
            field = schema.get_field(extra_field)
            if field.type not in ("boolean", "string"):
                print(
                    format_error_message(
                        f"Error: {extra_field} field must be a boolean or string"
                    )
                )
                code = 1
            break
            if len(get_unsupported_constraints(field.constraints)) != 0:
                print(
                    format_error_message(
                        f"Error: {field} in {org_path} has unsupported constraint. Only constraint of enum type is supported"
                    )
                )
            code = 1
            break

    if code == 0:

        print(format_success_message(f"Success: All data schema files are valid!"))

    return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    sys.exit(main(directory=args.directory))
