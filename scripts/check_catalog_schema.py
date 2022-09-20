import argparse
import sys
from pathlib import Path

from frictionless import FrictionlessException, Schema
from tabulate import tabulate

from lib.catalog_schema import (
    get_extra_fields,
    get_missing_fields,
    get_schema_paths,
    get_unsupported_constraints,
)
from lib.format_text import format_error_message, format_success_message


def main(directory: Path) -> int:
    code = 0
    for schema_path in get_schema_paths(directory):
        try:
            schema = Schema(schema_path)
            report = schema.validate()
            if not report.valid:
                print(format_error_message(f"Error: {schema_path} schema is not valid"))
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
                    f"Error: {missing_fields_string} fields are missing in the schema in {schema_path}"  # noqa: E501
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
                        f"Error: {field} in {schema_path} has unsupported constraint. Only constraint of enum type is supported"  # noqa: E501
                    )
                )
                code = 1
                break

    if code == 0:

        print(format_success_message("Success: All data schema files are valid!"))

    return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    sys.exit(main(directory=args.directory))
