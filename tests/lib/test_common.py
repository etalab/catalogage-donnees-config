import json
from pathlib import Path

from lib.common import get_paths, get_paths_of, transform_schema_field_to_payload


def test_get_paths() -> None:
    paths = get_paths(Path("tests/fixtures"))
    assert len(paths) == 9


def test_get_paths_of() -> None:
    paths = get_paths_of(Path("tests/fixtures"), "catalog_schema.json")
    assert len(paths) == 9


def test_transform_to_boolean_field_payload() -> None:

    data = {
        "name": "donnees_geoloc",
        "title": "Données géolocalisées",
        "description": "Ces données sont-elles géolocalisées ?",
        "type": "boolean",
        "trueValues": ["Oui"],
        "falseValues": ["Non"],
    }

    result = transform_schema_field_to_payload(data)
    expected_result = {
        "name": "donnees_geoloc",
        "title": "Données géolocalisées",
        "hint_text": "Ces données sont-elles géolocalisées ?",
        "type": "BOOL",
        "data": {"true_value": "Oui", "false_value": "Non"},
    }

    assert json.dumps(result) == json.dumps(expected_result)


def test_transform_to_enum_field_payload() -> None:

    data = {
        "name": "producteur_type",
        "title": "Type de producteur",
        "description": "Type de l'entité qui produit le jeu de données",
        "type": "string",
        "constraints": {
            "enum": [
                "1. Administration centrale",
                "2. Direction régionale des affaires culturelles",
                "3. Service à compétence nationale",
            ]
        },
    }

    result = transform_schema_field_to_payload(data)
    expected_result = {
        "name": "producteur_type",
        "title": "Type de producteur",
        "hint_text": "Type de l'entité qui produit le jeu de données",
        "type": "ENUM",
        "data": {
            "values": [
                "1. Administration centrale",
                "2. Direction régionale des affaires culturelles",
                "3. Service à compétence nationale",
            ]
        },
    }

    assert json.dumps(result) == json.dumps(expected_result)


def test_transform_to_string_field_payload() -> None:

    data = {
        "name": "service",
        "title": "Service",
        "description": "Nom de l'entité qui produit le jeu de données",
        "type": "string",
        "constraints": {"required": "true"},
    }

    result = transform_schema_field_to_payload(data)
    expected_result = {
        "name": "service",
        "title": "Service",
        "hint_text": "Nom de l'entité qui produit le jeu de données",
        "type": "TEXT",
        "data": {},
    }

    assert json.dumps(result) == json.dumps(expected_result)
