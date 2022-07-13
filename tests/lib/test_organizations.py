import pathlib

import pytest

from lib.organization import (
    contains_one_organization_per_file,
    get_organizations,
    get_organizations_path,
)


def test_get_org_paths() -> None:
    org_paths = get_organizations_path("tests/fixtures")
    assert len(org_paths) == 3
    org_1 = org_paths[0]
    assert str(org_1) == "tests/fixtures/test_orga_bad/organization.json"
    org_2 = org_paths[0]
    assert str(org_2) == "tests/fixtures/test_orga_1/organization.json"


def test_get_organizations_list() -> None:
    organizations = get_organizations("tests/fixtures")
    assert len(organizations) == 3


def test_contains_one_organization_per_file() -> None:
    organization_file_path = pathlib.Path(
        "tests/fixtures/test_orga_1/organization.json"
    )
    assert contains_one_organization_per_file(organization_file_path) is True


def test_does_not_contain_one_organization_per_file() -> None:
    organization_file_path = pathlib.Path(
        "tests/fixtures/test_orga_bad/organization.json"
    )
    assert contains_one_organization_per_file(organization_file_path) is False
