import json
from pathlib import Path

import httpx
import pytest

from scripts.upload_organizations import main


def test_upload_new_orgs(capsys: pytest.CaptureFixture) -> None:
    payloads = []

    def app(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/organizations/"
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

    captured = capsys.readouterr()
    assert "[created] {'siret': '566688866', 'name': 'test_1'}" in captured.out
    assert "[created] {'siret': '566688866', 'name': 'test_2'}" in captured.out


def test_existing_orgs(capsys: pytest.CaptureFixture) -> None:
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
    captured = capsys.readouterr()
    assert "[created]" in captured.out

    # Do it once again to simulate existing organizations.
    code = main(Path("tests/fixtures/with_well_formatted_organizations"), client=client)
    assert code == 0
    assert existing == {"test_1", "test_2"}

    captured = capsys.readouterr()
    assert "[ok] {'siret': '566688866', 'name': 'test_1'}" in captured.out
    assert "[ok] {'siret': '566688866', 'name': 'test_2'}" in captured.out


def test_server_http_error(capsys: pytest.CaptureFixture) -> None:
    def app(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    client = httpx.Client(
        base_url="http://testserver/api",
        transport=httpx.MockTransport(app),
    )

    code = main(Path("tests/fixtures/with_well_formatted_organizations"), client=client)
    assert code == 1

    captured = capsys.readouterr()
    assert "ERROR" in captured.err


def test_server_unexpected_status(capsys: pytest.CaptureFixture) -> None:
    def app(request: httpx.Request) -> httpx.Response:
        return httpx.Response(202)

    client = httpx.Client(
        base_url="http://testserver/api",
        transport=httpx.MockTransport(app),
    )

    code = main(Path("tests/fixtures/with_well_formatted_organizations"), client=client)
    assert code == 1

    captured = capsys.readouterr()
    assert "ERROR" in captured.err


def test_server_failure(capsys: pytest.CaptureFixture) -> None:
    def app(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Network failed")

    client = httpx.Client(
        base_url="http://testserver/api",
        transport=httpx.MockTransport(app),
    )

    code = main(Path("tests/fixtures/with_well_formatted_organizations"), client=client)
    assert code == 1

    captured = capsys.readouterr()
    assert "ERROR" in captured.err
