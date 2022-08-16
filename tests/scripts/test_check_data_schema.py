from pathlib import Path

from scripts.check_catalog_schema import main


def test_return_0_exit_code_if_all_catalog_schema_are_valid_table_schema() -> None:
    code = main(
        Path(
            "tests/fixtures/with_well_formatted_organizations_and_valid_catalog_schema"  # noqa: E501
        )
    )
    assert code == 0


def test_return_1_exit_code_if_all_organizations_have_not_the_right_format() -> None:
    code = main(
        Path(
            "tests/fixtures/with_well_formatted_organizations_and_not_valid_catalog_schema"  # noqa: E501
        )
    )
    assert code == 1
