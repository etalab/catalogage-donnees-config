from pathlib import Path

from scripts.upload_organizations import main


def test_return_0_exit_code_if_upload_succeed() -> None:
    code = main(Path("tests/fixtures/with_well_formatted_organizations"))
    assert code == 0
