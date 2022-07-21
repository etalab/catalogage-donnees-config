from pathlib import Path

from lib.organization import (
    contains_one_organization_per_file,
    get_organizations,
    get_organizations_path,
)


def test_get_org_paths() -> None:
    root = Path("tests/fixtures/with_well_formatted_organizations")

    org_paths = get_organizations_path(root)
    assert len(org_paths) == 2

    org_paths = sorted(path.relative_to(root) for path in org_paths)
    assert str(org_paths[0]) == "test_orga_1/organization.json"
    assert str(org_paths[1]) == "test_orga_2/organization.json"


def test_get_organizations_list() -> None:
    organizations = get_organizations(
        Path("tests/fixtures/with_well_formatted_organizations")
    )
    assert len(organizations) == 2


def test_contains_one_organization_per_file() -> None:

    organization_file_path = Path(
        "tests/fixtures/with_badly_formatted_organizations/test_orga_1/organization.json"  # noqa: E501
    )
    assert contains_one_organization_per_file(organization_file_path)


def test_does_not_contain_one_organization_per_file() -> None:
    organization_file_path = Path(
        "tests/fixtures/with_badly_formatted_organizations/test_orga_bad/organization.json"  # noqa: E501
    )
    assert not contains_one_organization_per_file(organization_file_path)
