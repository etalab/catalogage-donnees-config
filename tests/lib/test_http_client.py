import pytest

from lib.http_client import get_client


def test_get_client_missing_api_url() -> None:
    with pytest.raises(RuntimeError) as ctx:
        get_client()
    assert "No CATALOGAGE_API_URL set" in str(ctx.value)


def test_get_client_missing_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CATALOGAGE_API_URL", "https://catalogue.multi.coop/api")
    with pytest.raises(RuntimeError) as ctx:
        get_client()
    assert "No CATALOGAGE_API_KEY set" in str(ctx.value)


def test_get_client_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CATALOGAGE_API_URL", "https://catalogue.multi.coop/api")
    monkeypatch.setenv("CATALOGAGE_API_KEY", "abcd1234")
    client = get_client()
    assert client.base_url == "https://catalogue.multi.coop/api/"
    assert client.headers["X-Api-Key"] == "abcd1234"
