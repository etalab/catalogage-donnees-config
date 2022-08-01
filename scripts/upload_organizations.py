import argparse
import sys
import traceback
from pathlib import Path

import dotenv
import httpx

from lib.http_client import get_client
from lib.organization import get_organizations


def main(directory: Path, client: httpx.Client) -> int:
    code = 0

    for organization in get_organizations(directory):
        payload = {"siret": organization.siret, "name": organization.name}

        try:
            response = client.post("/organizations", json=payload)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            print(
                f"Error response {exc.response.status_code} "
                f"while requesting {exc.request.url!r}."
            )
            code = 1
        except httpx.HTTPError:
            traceback.print_exc()
            code = 1
        else:
            print(f"Created organization {organization.name} with payload {payload}")

    return code


if __name__ == "__main__":
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    sys.exit(main(directory=args.directory, client=get_client()))
