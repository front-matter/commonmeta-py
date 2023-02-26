"""Citeproc writer for commonmeta-py"""
import json

from ..utils import pages_as_string, to_citeproc
from ..base_utils import wrap, presence, parse_attributes, compact
from ..date_utils import get_date_by_type, get_date_parts
from ..doi_utils import doi_from_url
from ..constants import CM_TO_CP_TRANSLATIONS, Commonmeta


def write_citeproc(metadata: Commonmeta) -> str:
    """Write citeproc"""
    if len(wrap(metadata.creators)) == 0:
        author = None
    else:
        author = to_citeproc(wrap(metadata.creators))

    if (
        metadata.type == "Software"
        and metadata.version is not None
    ):
        type_ = "book"
    else:
        type_ = CM_TO_CP_TRANSLATIONS.get(metadata.type, 'Document')

    container = metadata.container or {}
    data = compact(
        {
            "type": type_,
            "id": metadata.id,
            "DOI": doi_from_url(metadata.id) if metadata.id else None,
            "URL": metadata.url,
            "categories": presence(
                parse_attributes(
                    wrap(metadata.subjects), content="subject", first=False
                )
            ),
            "language": metadata.language,
            "author": author,
            "contributor": to_citeproc(wrap(metadata.contributors)),
            "issued": get_date_parts(
                get_date_by_type(metadata.dates, "Issued")
                or str(metadata.publication_year)
            ),
            "submitted": get_date_by_type(metadata.dates, "Submitted"),
            "abstract": parse_attributes(
                metadata.descriptions, content="description", first=True
            ),
            "container-title": container.get("title", None),
            "volume": container.get("volume", None),
            "issue": container.get("issue", None),
            "page": pages_as_string(container),
            "publisher": metadata.publisher,
            "title": parse_attributes(metadata.titles, content="title", first=True),
            "copyright": metadata.rights[0].get("rights", None)
            if metadata.rights
            else None,
            "version": metadata.version,
        }
    )
    return json.dumps(data, indent=4)
