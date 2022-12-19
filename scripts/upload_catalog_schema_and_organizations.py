import argparse
import sys
import traceback
from pathlib import Path

import dotenv
import httpx
from frictionless import Schema

from lib.catalog_schema import get_extra_fields
from lib.common import get_paths, is_valid_svg, transform_schema_field_to_payload
from lib.format_text import format_error_message, format_success_message
from lib.http_client import get_client
from lib.organization import get_organization


def get_logo_url(organization_directory: Path) -> str:
    return f"https://raw.githubusercontent.com/etalab/catalogage-donnees-config/master/{str(organization_directory)}/logo.svg"  # noqa: E501


def main(directory: Path, client: httpx.Client = None) -> int:
    code = 0
    if client is None:
        client = get_client()

    for path in get_paths(directory):
        organization_path = path / "organization.json"
        organization = get_organization(organization_path)
        organization_logo = path / "logo.svg"
        organization_logo_exists = Path(organization_logo).is_file()

        schema_path = path / "catalog_schema.json"
        catalog_schema_exists = Path(schema_path).is_file()

        # Upload organization

        payload = {
            "siret": organization.siret,
            "name": organization.name,
            "logo_url": None,
        }
        if organization_logo_exists:
            if is_valid_svg(organization_logo):
                payload = {
                    "siret": organization.siret,
                    "name": organization.name,
                    "logo_url": get_logo_url(organization_directory=path),
                }
            else:
                code = 1
                print(
                    format_error_message(
                        f"ERROR: file {organization_logo} is not a valid svg"
                    ),
                    file=sys.stderr,
                )

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

        if catalog_schema_exists:

            friction_less_schema = Schema(schema_path)
            extra_fields = get_extra_fields(friction_less_schema.field_names)
            schema_fields = friction_less_schema.get("fields")
            extra_field_payloads = []

            for schema_field in schema_fields:
                if schema_field["name"] in extra_fields:
                    extra_field_payloads.append(
                        transform_schema_field_to_payload(schema_field)
                    )

                schema_payload = {
                    "organization_siret": organization.siret,
                    "extra_fields": extra_field_payloads,
                }

            try:

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

            if response.status_code == 201:
                print(
                    format_success_message(
                        f"[Created] Catalog {organization.name} with {payload}"
                    )
                )

            if response.status_code > 201:
                print(
                    format_error_message(
                        f"ERROR: unexpected response status code: {response.status_code}"  # noqa: E501
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
