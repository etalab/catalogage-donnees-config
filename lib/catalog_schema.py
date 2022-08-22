from pathlib import Path
from typing import List

from .common import get_paths


def get_schema_paths(path: Path) -> List[Path]:
    return get_paths(path, "catalog_schema.json")


REQUIRED_FIELDS_NAME = [
    "titre",
    "description",
    "mots_cles",
    "nom_orga",
    "siret_orga",
    "id_alt_orga",
    "service",
    "si",
    "contact_service",
    "contact_personne",
    "date_pub",
    "date_maj",
    "freq_maj",
    "couv_geo",
    "url",
    "format",
    "licence",
    "producteur_type",
]


def has_field(field_name: str, field_list: List[str]) -> bool:
    return any(field_name in field for field in field_list)


def get_missing_fields(field_names: List[str]) -> List[str]:
    missing_fields: List[str] = []
    for ref in REQUIRED_FIELDS_NAME:
        if not has_field(field_name=ref, field_list=field_names):
            missing_fields.append(ref)
    return missing_fields
