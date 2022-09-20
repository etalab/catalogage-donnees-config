from lib.catalog_schema import get_extra_fields, get_missing_fields, has_field


def test_has_field() -> None:
    field = "title"

    fields = ["title", "service"]
    assert has_field(field, fields) is True


def test_has_no_field() -> None:
    field = "tarte"

    fields = ["title", "service"]
    assert has_field(field, fields) is False


def test_has_no_missing_fields() -> None:
    fields = [
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

    assert get_missing_fields(fields) == set([])


def test_has_missing_fields() -> None:
    fields = [
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
    ]

    missing_fields = get_missing_fields(fields)
    assert len(missing_fields) == 2
    assert missing_fields == set(["licence", "producteur_type"])


def test_has_extra_fields() -> None:
    fields = [
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
        "extra_field_1",
    ]

    assert get_extra_fields(fields) == {"extra_field_1"}
