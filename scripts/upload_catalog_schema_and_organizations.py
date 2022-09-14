import argparse
import sys
import traceback
from pathlib import Path
import json
import dotenv
import httpx

from lib.http_client import get_client
from lib.organization import get_organization
from lib.catalog_schema import get_schema, get_extra_fields
from frictionless import Schema
from lib.common import get_paths, transform_schema_field_to_payload
from lib.format_text import format_error_message, format_success_message


def main(directory: Path, client: httpx.Client = None) -> int:
    code = 0
    if client is None:
        client = get_client()

    for path in get_paths(directory):
        organization_path = path / "organization.json"
        organization = get_organization(organization_path)

        schema_path = path / "catalog_schema.json"
        schema = get_schema(schema_path)

        payload = {"siret": organization.siret, "name": organization.name}

        # Upload organization

        try:
            response = client.post("/organizations/", json=payload)
            response.raise_for_status()
        except (httpx.HTTPStatusError, httpx.HTTPError) as exc:
            print(
                format_error_message(
                    f"ERROR: while requesting {exc.request.url!r} with {payload=}:"
                ),
                file=sys.stderr,
            )
            traceback.print_exc()
            code = 1
            break

        if response.status_code == 201:
            print(
                format_success_message(
                    f"[OK] Organization {organization.name} with {payload}"
                )
            )

        if response.status_code > 201:
            print(
                format_error_message(
                    f"ERROR: unexpected response status code: {response.status_code}"
                ),
                file=sys.stderr,
            )
            code = 1
            break

        # Upload catalog schema
        friction_less_schema = Schema(schema_path)
        extra_fields = get_extra_fields(friction_less_schema.field_names)
        schema_fields = friction_less_schema.get("fields")
        fields_payload = []

        for schema_field in schema_fields:
            if schema_field["name"] in extra_fields:
                fields_payload.append(transform_schema_field_to_payload(schema_field))
        try:
            schema_payload = {
                "organization_siret": organization.siret,
                "extra_fields": fields_payload,
            }

            response = client.post("/catalogs/", json=schema_payload)
            response.raise_for_status()
        except (httpx.HTTPStatusError, httpx.HTTPError) as exc:

            print(
                format_error_message(
                    f"ERROR: while requesting {exc.request.url!r} with {payload=}:"
                ),
                file=sys.stderr,
            )
            traceback.print_exc()
            code = 1
            break

        if response.status_code == 201 or response.status_code == 200:
            print(
                format_success_message(f"[OK] Catalog schema for {organization.name}")
            )
        else:
            print(
                format_error_message(
                    f"ERROR: unexpected response status code: {response.status_code}"
                ),
                file=sys.stderr,
            )
            code = 1
            break

    return code


if __name__ == "__main__":
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    sys.exit(main(directory=args.directory))
