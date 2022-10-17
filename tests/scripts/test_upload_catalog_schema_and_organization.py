# flake8: noqa: E501
import json
from pathlib import Path
from typing import Tuple

import dotenv
import httpx
import pytest

from scripts.upload_catalog_schema_and_organizations import main


def test_upload_new_catalog_schema_and_new_organization(
    capsys: pytest.CaptureFixture,
) -> None:
    payloads: Tuple[str, str, dict]
    requests = []

    def app(request: httpx.Request) -> httpx.Response:
        requests.append((request.method, request.url.path, json.loads(request.content)))
        return httpx.Response(201)

    client = httpx.Client(
        base_url="http://testserver/api",
        transport=httpx.MockTransport(app),
    )

    code = main(
        Path(
            "tests/fixtures/with_well_formatted_organizations_and_valid_catalog_schema"
        ),
        client=client,
    )
    assert code == 0

    request1, request2 = requests

    assert request1 == (
        "POST",
        "/api/organizations/",
        {"siret": "55566688899991", "name": "test_1"},
    )
    assert request2 == (
        "POST",
        "/api/catalogs/",
        {
            "organization_siret": "55566688899991",
            "extra_fields": [
                {
                    "name": "direction",
                    "title": "Direction",
                    "hint_text": "Nom de l'entité (direction) qui produit le jeu de données au sein du Ministère de la Culture",
                    "type": "ENUM",
                    "data": {
                        "values": [
                            "1. Secrétariat général",
                            "1. Direction générale des patrimoines et de l'architecture",
                            "1. Direction générale de la création artistique",
                            "1. Direction générale des médias et des industries culturelles",
                            "1. Délégation générale à la transmission aux territoires et à la démocratie culturelle",
                            "1. Délégation générale à la langue française et aux langues de France",
                            "1. Centre national du cinéma et de l'image animée",
                            "2. DRAC Auvergne-Rhône-Alpes",
                            "2. DRAC Bourgogne-France-Comté",
                            "2. DRAC Bretagne",
                            "2. DRAC Centre-Val de Loire",
                            "2. DRAC Corse",
                            "2. DRAC Grand-Est",
                            "2. DRAC Hauts-de-France",
                            "2. DRAC Île-de-France",
                            "2. DRAC Normandie",
                            "2. DRAC Nouvelle Aquitaine",
                            "2. DRAC Occitanie",
                            "2. DRAC Pays-de-la-Loire",
                            "2. DRAC Provence-Alpes-Côte d'Azur",
                            "2. DAC Guadeloupe",
                            "2. DAC Martinique",
                            "2. DAC Océan Indien",
                            "2. DAC Mayotte",
                            "2. Direction de la culture, de la jeunesse et des sports de Guyane",
                            "2. Mission aux affaires culturelles de Nouvelle-Calédonie",
                            "2. Mission aux affaires culturelles en Polynésie française",
                            "2. Mission Saint-Pierre et Miquelon",
                            "3. Archives nationales",
                            "3. Archives nationales d'Outre-Mer",
                            "3. Archives nationales du monde du travail",
                            "3. Centre de recherche et de restauration des musées de France (C2RMF)",
                            "3. Département des recherches archéologiques subaquatiques et sous-marines (DRASSM)",
                            "3. Laboratoire de recherche des monuments historiques (LRMH)",
                            "3. Médiathèque de l'architecture et du patrimoine",
                            "3. Mobilier national et manufactures nationales des Gobelins, de Beauvais et de la Savonnerie",
                            "3. Musée Clémenceau et de Lattre de Tassigny",
                            "3. Musée d'Archéologie nationale et domaine national de Saint-Germain-en-Laye",
                            "3. Musée de la Renaissance au château d'Écouen",
                            "3. Musée de Port-Royal des Champs",
                            "3. Musée de la Préhistoire",
                            "3. Musée des châteaux de Malmaison et de Bois-Préau (annexes : maison Bonaparte et musées de l'île d'Aix)",
                            "3. Musée des plans-reliefs",
                            "3. Musée du Moyen Age, thermes et hôtel de Cluny",
                            "3. Musée Magnin",
                            "3. Musée national et domaine du château de Pau",
                            "3. Musées et domaines de Compiègne et Blérancourt",
                            "3. Musées nationaux du XXe siècle des Alpes-Maritimes (musée Fernand Léger, musée Marc Chagall, musée La guerre et la paix de Picasso)",
                        ]
                    },
                },
                {
                    "name": "domaine",
                    "title": "Domaine",
                    "hint_text": "Nom du domaine associé au jeu de données.",
                    "type": "ENUM",
                    "data": {
                        "values": [
                            "Pluridisciplinaire",
                            "Audiovisuel",
                            "Livres et Presse",
                            "Archives",
                            "Patrimoine",
                            "Architecture",
                            "Artisanat d'art",
                            "Arts visuels",
                            "Spectacle vivant",
                            "Bibliothèques",
                            "Gestion et administration",
                            "Langues",
                        ]
                    },
                },
                {
                    "name": "sous_domaine",
                    "title": "Sous-domaine",
                    "hint_text": "Nom du sous-domaine associé au jeu de données.",
                    "type": "ENUM",
                    "data": {
                        "values": [
                            "Archéologie",
                            "Arts plastiques",
                            "Autre spectacle vivant",
                            "Danse",
                            "Design et mode",
                            "Film et cinéma",
                            "Finance",
                            "Langue française",
                            "Langues de France",
                            "Livre",
                            "Monuments",
                            "Multimedia",
                            "Musées",
                            "Musique",
                            "Musique enregistrée",
                            "Organisation",
                            "Photographie",
                            "Presse",
                            "Radio",
                            "Ressources Humaines",
                            "Télévision",
                            "Théâtre",
                            "Vidéo",
                        ]
                    },
                },
                {
                    "name": "donnees_qualite",
                    "title": "Qualité des données",
                    "hint_text": "Le jeu de données nécessite-t-il selon vous un accompagnement dans la montée en qualité des données ? si oui, lequel ?",
                    "type": "TEXT",
                    "data": {},
                },
                {
                    "name": "donnees_geoloc",
                    "title": "Données géolocalisées",
                    "hint_text": "Ces données sont-elles géolocalisées ?",
                    "type": "BOOL",
                    "data": {"true_value": "Oui", "false_value": "Non"},
                },
                {
                    "name": "donnees_taille",
                    "title": "Taille du jeu de données",
                    "hint_text": "Information sur la volumétrie et l'unité de mesure (taille du fichier, nombre d'entrées ou d'enregistrements...) associées au jeu de données.",
                    "type": "TEXT",
                    "data": {},
                },
                {
                    "name": "referentiel",
                    "title": "Référentiel ou norme",
                    "hint_text": "Ce jeu de données contient-il un référentiel ou une norme ? si oui, lequel ?",
                    "type": "TEXT",
                    "data": {},
                },
                {
                    "name": "donnees_diffusion",
                    "title": "Perspectives de diffusion",
                    "hint_text": "Ce jeu de données peut-il être ouvert ? si non, pourquoi ? (Pour plus d'informations, [lire le guide d'Etalab](https://guides.etalab.gouv.fr/juridique/ouverture/).)",
                    "type": "TEXT",
                    "data": {},
                },
                {
                    "name": "donnees_perso",
                    "title": "Données à caractère personnel",
                    "hint_text": "Ce jeu de données contient-il des [données à caractère personnel](https://guides.etalab.gouv.fr/juridique/ouverture/#que-faire-si-mes-documents-administratifs-contiennent-des-donnees-a-caractere-personnel) ?.",
                    "type": "BOOL",
                    "data": {"true_value": "Oui", "false_value": "Non"},
                },
                {
                    "name": "donnees_secret",
                    "title": "Données confidentielles",
                    "hint_text": "Ce jeu de données contient-il des [secrets légaux](https://guides.etalab.gouv.fr/juridique/ouverture/#que-faire-si-mes-documents-administratifs-contiennent-des-secrets-legaux) ?",
                    "type": "BOOL",
                    "data": {"true_value": "Oui", "false_value": "Non"},
                },
                {
                    "name": "donnees_pi",
                    "title": "Propriété intellectuelle",
                    "hint_text": "Le Ministère de la Culture peut-il se prévaloir d'un [droit de propriété intellectuelle](https://guides.etalab.gouv.fr/juridique/reutilisation/#le-cas-de-la-propriete-intellectuelle) sur le jeu de données ?",
                    "type": "BOOL",
                    "data": {"true_value": "Oui", "false_value": "Non"},
                },
            ],
        },
    )


def test_upload_organization_without_schema() -> None:
    payloads: Tuple[str, str, dict]
    requests = []

    def app(request: httpx.Request) -> httpx.Response:
        requests.append((request.method, request.url.path, json.loads(request.content)))
        return httpx.Response(201)

    client = httpx.Client(
        base_url="http://testserver/api",
        transport=httpx.MockTransport(app),
    )

    code = main(
        Path("tests/fixtures/with_no_existing_catalog_schema"),
        client=client,
    )
    assert code == 0
    assert len(requests) == 1

    assert requests[0] == (
        "POST",
        "/api/organizations/",
        {"siret": "55566688899992", "name": "test_2"},
    )


def test_server_http_error(capsys: pytest.CaptureFixture) -> None:
    def app(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    client = httpx.Client(
        base_url="http://testserver/api",
        transport=httpx.MockTransport(app),
    )

    code = main(
        Path(
            "tests/fixtures/with_well_formatted_organizations_and_valid_catalog_schema"
        ),
        client=client,
    )
    assert code == 1

    captured = capsys.readouterr()
    assert "ERROR" in captured.err


def test_server_unexpected_status(capsys: pytest.CaptureFixture) -> None:
    def app(request: httpx.Request) -> httpx.Response:
        return httpx.Response(202)

    client = httpx.Client(
        base_url="http://testserver/api",
        transport=httpx.MockTransport(app),
    )

    code = main(
        Path(
            "tests/fixtures/with_well_formatted_organizations_and_valid_catalog_schema"
        ),
        client=client,
    )
    assert code == 1

    captured = capsys.readouterr()
    assert "ERROR" in captured.err


def test_server_failure(capsys: pytest.CaptureFixture) -> None:
    def app(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Network failed")

    client = httpx.Client(
        base_url="http://testserver/api",
        transport=httpx.MockTransport(app),
    )

    code = main(
        Path(
            "tests/fixtures/with_well_formatted_organizations_and_valid_catalog_schema"
        ),
        client=client,
    )
    assert code == 1

    captured = capsys.readouterr()
    assert "ERROR" in captured.err


def _is_local_instance_serving() -> bool:
    try:
        httpx.get("http://localhost:3579")
    except httpx.ConnectError:  # pragma: no cover
        return False
    else:
        return True


@pytest.mark.xfail(
    not _is_local_instance_serving(), reason="Local instance is not running"
)
def test_localhost_server() -> None:
    dotenv.load_dotenv()

    code = main(
        Path(
            "tests/fixtures/with_well_formatted_organizations_and_valid_catalog_schema"
        )
    )
    assert code == 0
