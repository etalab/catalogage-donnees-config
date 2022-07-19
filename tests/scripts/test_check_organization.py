from pathlib import Path

from scripts.check_organizations import main


def test_return_0_exit_code_if_all_organizations_have_the_right_format() -> None:
    code = main(Path("tests/fixtures/with_well_formatted_organizations"))
    assert code == 0


def test_return_1_exit_code_if_all_organizations_have_not_the_right_format() -> None:
    code = main(Path("tests/fixtures/with_badly_formatted_organizations"))
    assert code == 1
