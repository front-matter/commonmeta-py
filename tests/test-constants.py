"""Test constants against the commonmeta schema"""

import json
from os import path

import pytest

import commonmeta
from commonmeta.constants import (
    CM_TO_BIB_TRANSLATIONS,
    CM_TO_CR_TRANSLATIONS,
    CM_TO_CSL_TRANSLATIONS,
    CM_TO_DC_TRANSLATIONS,
    CM_TO_INVENIORDM_TRANSLATIONS,
    CM_TO_RIS_TRANSLATIONS,
    CM_TO_SO_TRANSLATIONS,
    COMMONMETA_RELATION_TYPES,
    OA_TO_CM_TRANSLATIONS,
)


def _schema() -> dict:
    file_path = path.join(
        path.dirname(commonmeta.__file__), "resources", "commonmeta_v1.0.json"
    )
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)


@pytest.mark.parametrize("work_type", ["Erratum", "Retraction"])
@pytest.mark.parametrize(
    "table",
    [
        CM_TO_BIB_TRANSLATIONS,
        CM_TO_CR_TRANSLATIONS,
        CM_TO_CSL_TRANSLATIONS,
        CM_TO_DC_TRANSLATIONS,
        CM_TO_INVENIORDM_TRANSLATIONS,
        CM_TO_RIS_TRANSLATIONS,
        CM_TO_SO_TRANSLATIONS,
    ],
)
def test_update_notices_are_written_as_journal_articles(table, work_type):
    """An erratum or retraction notice is a journal article in every format
    without a type of its own, as commonmeta-rs writes it."""
    assert table[work_type] == table["JournalArticle"]


@pytest.mark.parametrize(
    "openalex_type,work_type",
    [("erratum", "Erratum"), ("retraction", "Retraction")],
)
def test_openalex_update_notice_types(openalex_type, work_type):
    assert OA_TO_CM_TRANSLATIONS[openalex_type] == work_type


def test_relation_types_are_in_the_schema():
    """Every relation type the readers keep is one the schema allows."""
    relation = _schema()["$defs"]["work"]["properties"]["relations"]["items"]
    allowed = set(relation["properties"]["type"]["enum"])
    assert set(COMMONMETA_RELATION_TYPES) <= allowed
    assert {"IsRetractedBy", "Retracts", "IsCorrectedBy", "Corrects"} <= set(
        COMMONMETA_RELATION_TYPES
    )
