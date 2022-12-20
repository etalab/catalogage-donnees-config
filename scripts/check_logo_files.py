import argparse
import sys
from pathlib import Path

from lib.catalog_schema import get_logo_paths
from lib.common import is_valid_svg
from lib.format_text import format_error_message, format_success_message


def main(directory: Path) -> int:
    code = 0
    for logo_path in get_logo_paths(directory):
        if logo_path.is_file() and not is_valid_svg(logo_path):
            print(format_error_message(f"the {logo_path} file is not a valid svg"))
            code = 1
            break

    print(format_success_message("Success: all logos are valid svg files"))
    return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    sys.exit(main(directory=args.directory))
