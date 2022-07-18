from pathlib import Path

from scripts.check_organizations import main


def test_return_0_exit_code_if_all_organizations_have_the_right_format() -> None:
    code = main(Path("tests/fixtures"))
    assert code == 0
