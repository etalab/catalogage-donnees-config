import pathlib
import sys

from frictionless import Resource, validate
from lib.organization import (
    get_organizations_path,
    contains_one_organization_per_file,
    get_organization_validation_report,
)

code = 0

for org_path in get_organizations_path("organizations"):

    if not contains_one_organization_per_file(org_path):
        print(
            f"an organization file must contain only one organization. Multiple organizations found in {org_path}"
        )
        code = 1
        break

    report = get_organization_validation_report(org_path)

    if report.valid == False:
        code = 1
        print(report.to_summary())
        break

if code == 0:
    print("OK")

sys.exit(code)
