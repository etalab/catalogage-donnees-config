from pathlib import Path

from scripts.check_organizations import main


def test_return_0_exit_code_if_all_organizations_have_the_right_format() -> None:
    code = main(Path("tests/fixtures/with_well_formatted_organizations"))
    assert code == 0


def test_return_1_exit_code_if_a_property_is_missing_in_a_organization_file() -> None:
    code = main(Path("tests/fixtures/with_missing_organization_properties"))
    assert code == 1


def test_return_1_exit_code_if_an_organization_file_contains_more_than_one_organization() -> None:  # noqa: E501
    code = main(Path("tests/fixtures/with_more_than_one_organization_in_a_single_file"))
    assert code == 1
