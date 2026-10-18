"""Property-based tests: a record written to a format reads back the same"""

import datetime
import json
import unicodedata

import pytest

# hypothesis is a dev dependency on Python 3.11+ only.
pytest.importorskip("hypothesis")

from hypothesis import given, settings  # noqa: E402
from hypothesis import strategies as st  # noqa: E402

from commonmeta import Metadata  # noqa: E402
from commonmeta.author_utils import ORGANIZATION_WORDS  # noqa: E402

# "ı" and "İ" change length when their case changes, which a writer that
# capitalizes a name is free to do.
letters = st.characters(categories=["L"], exclude_characters="ıİ")
words = st.text(letters, min_size=1, max_size=8)
# A name that is an organization word ("Lab", "Team") reads back as an
# organization, and rightly: a reader cannot tell it from one.
names = (
    st.text(letters, min_size=2, max_size=10)
    .map(str.capitalize)
    .filter(lambda name: not ORGANIZATION_WORDS.search(name))
)

# Names may repeat: two people can share one, and a reader must keep both.
contributors = st.lists(
    st.builds(
        lambda given_name, family_name: {
            "type": "Person",
            "roles": ["Author"],
            "person": {"given_name": given_name, "family_name": family_name},
        },
        names,
        names,
    ),
    min_size=1,
    max_size=3,
)

records = st.builds(
    lambda doi, title, contributors, published: {
        "id": f"https://doi.org/{doi}",
        "type": "JournalArticle",
        "url": f"https://example.org/{doi}",
        "title": title,
        "contributors": contributors,
        "date_published": published,
        "publisher": {"name": "Example Press"},
        "container": {
            "type": "Journal",
            "title": "Journal of Examples",
            "volume": "1",
            "identifiers": [{"identifier": "2050-084X", "identifier_type": "ISSN"}],
        },
    },
    st.builds(
        lambda prefix, suffix: f"10.{prefix}/{suffix}",
        st.integers(1000, 99999),
        st.from_regex(r"\A[a-z0-9]{1,8}\Z"),
    ),
    st.lists(words, min_size=1, max_size=6).map(" ".join),
    contributors,
    st.dates(datetime.date(1900, 1, 1), datetime.date(2030, 12, 31)).map(str),
)


def nfc(value: str | None) -> str | None:
    # bibtexparser composes characters: "豈" (U+F900) reads back as U+8C48.
    return unicodedata.normalize("NFC", value) if value else value


def summary(metadata: Metadata, date_length: int = 10) -> dict:
    """The fields every one of these formats carries."""
    return {
        "id": metadata.id,
        "title": nfc(metadata.title),
        "date_published": (metadata.date_published or "")[:date_length],
        "contributors": [
            (
                nfc((c.get("person") or {}).get("given_name")),
                nfc((c.get("person") or {}).get("family_name")),
            )
            for c in metadata.contributors or []
        ],
    }


@pytest.mark.parametrize(
    ("to", "date_length"),
    [
        pytest.param("commonmeta", 10),
        pytest.param("csl", 10),
        pytest.param("datacite", 10),
        pytest.param("schema_org", 10),
        pytest.param("inveniordm", 10),
        # RIS writes only the year (PY), BibTeX the year and month.
        pytest.param("ris", 4),
        pytest.param("bibtex", 7),
    ],
)
@settings(max_examples=50)
@given(record=records)
def test_write_then_read_keeps_the_record(to, date_length, record):
    metadata = Metadata(json.dumps(record), via="commonmeta")
    output = metadata.write(to=to)
    if isinstance(output, bytes):
        output = output.decode()
    roundtripped = Metadata(output, via=to)
    assert summary(roundtripped) == summary(metadata, date_length)
