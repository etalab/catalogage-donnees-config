import json
from pathlib import Path
from typing import List

from frictionless import Field, Resource, Schema
from frictionless.report import Report

from .common import get_paths_of
from .entities import Organization


def get_organizations_path(path: Path) -> List[Path]:
    return get_paths_of(path, "organization.json")


def get_organizations(path: Path) -> List[Organization]:
    organizations: List[Organization] = []

    for org_path in get_organizations_path(path):
        data = json.loads(org_path.read_text())
        organization = data[0]
        new_organization = Organization(
            siret=organization["siret"], name=organization["name"]
        )
        organizations.append(new_organization)

    return organizations


def contains_one_organization_per_file(path: Path) -> bool:
    data = json.loads(path.read_text())
    return len(data) == 1


def get_organization_validation_report(path: Path) -> Report:
    schema = Schema(
        fields=[
            Field(name="name", title="Nom de l'organisation", type="string"),
            Field(name="siret", title="Numéro SIRET de l'organisation", type="string"),
        ]
    )

    with Resource(path=str(path), schema=schema) as resource:
        report = resource.validate()

    return report
