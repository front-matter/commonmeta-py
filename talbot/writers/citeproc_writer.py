"""Citeproc writer for Talbot"""
import json

from ..utils import pages_as_string, to_citeproc
from ..base_utils import wrap, presence, parse_attributes, compact
from ..date_utils import get_date_by_type, get_date_parts
from ..doi_utils import doi_from_url


def write_citeproc(metadata):
    """Write citeproc"""
    if (
        len(wrap(metadata.creators)) == 1
        and wrap(metadata.creators)[0].get("name", None) == ":(unav)"
    ):
        author = None
    else:
        author = to_citeproc(wrap(metadata.creators))

    if (
        metadata.types.get("resourceTypeGeneral", None) == "Software"
        and metadata.version is not None
    ):
        type_ = "book"
    else:
        type_ = metadata.types.get("citeproc", "article")

    container = metadata.container or {}
    dictionary = compact(
        {
            "type": type_,
            "id": metadata.pid,
            "DOI": doi_from_url(metadata.pid),
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
                get_date_by_type(metadata.dates, "Issued") or str(
                    metadata.publication_year)
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
    return json.dumps(dictionary, indent=4)
