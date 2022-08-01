import os

import httpx


def get_client() -> httpx.Client:
    try:
        api_url = os.environ["CATALOGAGE_API_URL"]
        api_key = os.environ["CATALOGAGE_API_KEY"]
    except KeyError as exc:
        env_var = exc.args[0]
        raise RuntimeError(f"No {env_var} set")

    headers = {"X-Api-Key": api_key}

    return httpx.Client(base_url=api_url, headers=headers)
