import json
from pathlib import Path

import httpx

from scripts.upload_organizations import main


def test_upload_new_orgs() -> None:
    payloads = []

    def app(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/organizations"
        payloads.append(json.loads(request.content))
        return httpx.Response(201)

    client = httpx.Client(
        base_url="http://testserver/api",
        transport=httpx.MockTransport(app),
    )

    code = main(Path("tests/fixtures/with_well_formatted_organizations"), client=client)
    assert code == 0

    assert payloads == [
        {"siret": "566688866", "name": "test_1"},
        {"siret": "566688866", "name": "test_2"},
    ]


def test_existing_orgs() -> None:
    added = set()
    existing = set()

    def app(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)

        if payload["name"] in added:
            existing.add(payload["name"])
            return httpx.Response(200)
        else:
            added.add(payload["name"])
            return httpx.Response(201)

    client = httpx.Client(
        base_url="http://testserver/api",
        transport=httpx.MockTransport(app),
    )

    code = main(Path("tests/fixtures/with_well_formatted_organizations"), client=client)
    assert code == 0
    assert added == {"test_1", "test_2"}
    assert existing == set()

    # Do it once again to simulate existing organizations.
    code = main(Path("tests/fixtures/with_well_formatted_organizations"), client=client)
    assert code == 0
    assert existing == {"test_1", "test_2"}


def test_server_http_error() -> None:
    def app(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    client = httpx.Client(
        base_url="http://testserver/api",
        transport=httpx.MockTransport(app),
    )

    code = main(Path("tests/fixtures/with_well_formatted_organizations"), client=client)
    assert code == 1


def test_server_failure() -> None:
    def app(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Network failed")

    client = httpx.Client(
        base_url="http://testserver/api",
        transport=httpx.MockTransport(app),
    )

    code = main(Path("tests/fixtures/with_well_formatted_organizations"), client=client)
    assert code == 1
