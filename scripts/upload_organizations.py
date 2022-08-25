import argparse
import sys
import traceback
from pathlib import Path

import dotenv
import httpx

from lib.http_client import get_client
from lib.organization import get_organizations
from lib.format_text import format_error_message, format_success_message


def main(directory: Path, client: httpx.Client = None) -> int:
    if client is None:
        client = get_client()

    code = 0

    for organization in get_organizations(directory):
        payload = {"siret": organization.siret, "name": organization.name}

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
            continue

        if response.status_code == 201:
            print(format_success_message(f"[created] {payload}"))
        elif response.status_code == 200:
            print(format_success_message(f"[ok] {payload}"))
        else:
            print(
                format_error_message(
                    f"ERROR: unexpected response status code: {response.status_code}"
                ),
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
