import pathlib
import sys
import os
import json
import httpx

from frictionless import Resource, validate
from lib.organization import (
    get_organizations_path,
    contains_one_organization_per_file,
    get_organization_validation_report,
    get_organizations,
)


from lib.http_client import get_client

import argparse
from pathlib import Path


def main(directory: Path) -> int:
    code = 0
    env = os.environ.get("ENV", "developement")
    print(env)
    url = os.environ.get("API_URL", "http://localhost:3579/oganizations")
    client = get_client(env)

    for organization in get_organizations(directory):
        payload = {"siret": organization.siret, "name": organization.name}
        try:
            response = client.post(url, json=payload)
            response.raise_for_status()

            print(f"Created organization {organization.name} with payload {payload}")

        except httpx.ConnectError as exc:
            print(f"Server not found")
            code = 1

        except httpx.HTTPError as exc:
            print(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
            )
            code = 1

    return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    sys.exit(main(directory=args.directory))
