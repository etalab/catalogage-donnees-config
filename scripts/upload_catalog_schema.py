import argparse
import sys
import traceback
from pathlib import Path

import dotenv
import httpx

from lib.http_client import get_client
from lib.organization import get_organizations


def main(directory: Path, client: httpx.Client = None) -> int:
    if client is None:
        client = get_client()
    code = 0

    organizations = get_organizations(directory)

    for organization in organizations:
        payload = {"organization_siret": organization.siret}

        try:
            response = client.post("/catalogs/", json=payload)
            response.raise_for_status()
        except (httpx.HTTPStatusError, httpx.HTTPError) as exc:
            print(
                f"ERROR: while requesting {exc.request.url!r} with {payload=}:",
                file=sys.stderr,
            )
            traceback.print_exc()
            code = 1
            continue

        if response.status_code == 201:
            print(f"[created] {payload}")
        elif response.status_code == 200:
            print(f"[ok] {payload}")
        else:
            print(
                f"ERROR: unexpected response status code: {response.status_code}",
                file=sys.stderr,
            )
            code = 1

    return code


if __name__ == "__main__":
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    sys.exit(main(directory=args.directory))
