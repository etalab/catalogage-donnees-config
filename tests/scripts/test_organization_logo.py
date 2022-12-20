from pathlib import Path

from scripts.check_logo_files import main


def test_return_1_exit_code_if_logo_is_not_a_valid_svg() -> None:
    code = main(Path("tests/fixtures/with_invalid_logo"))  # noqa: E501
    assert code == 1


def test_return_0_exit_code_if_logo_is_a_valid_svg() -> None:
    code = main(Path("tests/fixtures/with_orgnization_logo"))  # noqa: E501
    assert code == 0
