import pathlib
import sys

from frictionless import Resource, validate

template = {
    "path": "...",
    "name": "organization",
    "profile": "tabular-data-resource",
    "scheme": "file",
    "format": "json",
    "hashing": "md5",
    "encoding": "utf-8",
    "schema": {
    "fields": [
            {
                "name": "siret",
                "title": "Numéro SIRET de l'organisation",
                "type": "string",
            },
            {
                "name": "name",
                "title": "Nom de l'organisation",
                "type": "string",
            },
        ]
    },
}

code = 0

for orgdir in pathlib.Path("organizations").iterdir():
    org_path = orgdir / "organization.json"

    descriptor = template.copy()
    descriptor["path"] = str(org_path)

    with Resource(descriptor=descriptor) as resource:
        report = validate(resource, type="resource")
        if not report.valid:
            code = 1
            print(report.to_summary())

if code == 0:
    print("OK")

sys.exit(code)
