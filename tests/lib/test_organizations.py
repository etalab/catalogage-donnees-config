from pathlib import Path

from lib.organization import (
    contains_one_organization_per_file,
    get_organizations,
    get_organizations_path,
)


def test_get_org_paths() -> None:
    org_paths = get_organizations_path(
        Path("tests/fixtures/with_well_formatted_organizations")
    )
    assert len(org_paths) == 2
    org_1 = org_paths[0]

    expectedPath1 = (
        "tests/fixtures/with_well_formatted_organizations/test_orga_1/organization.json"
    )
    assert str(org_1) == expectedPath1
    org_2 = org_paths[1]

    expectedPath2 = (
        "tests/fixtures/with_well_formatted_organizations/test_orga_2/organization.json"
    )
    assert str(org_2) == expectedPath2


def test_get_organizations_list() -> None:
    organizations = get_organizations(
        Path("tests/fixtures/with_well_formatted_organizations")
    )
    assert len(organizations) == 2
    assert organizations[0].name == "test_1"


def test_contains_one_organization_per_file() -> None:

    organization_file_path = Path(
        "tests/fixtures/with_badly_formatted_organizations/test_orga_1/organization.json"  # noqa: E501
    )
    assert contains_one_organization_per_file(organization_file_path) is True


def test_does_not_contain_one_organization_per_file() -> None:
    organization_file_path = Path(
        "tests/fixtures/with_badly_formatted_organizations/test_orga_bad/organization.json"  # noqa: E501
    )
    assert contains_one_organization_per_file(organization_file_path) is False
