"""CSL-JSON writer for commonmeta-py"""

from typing import Optional

import orjson as json

from ..base_utils import compact, first, parse_attributes, presence, wrap
from ..constants import CM_TO_CSL_TRANSLATIONS, Commonmeta
from ..date_utils import get_date_parts
from ..doi_utils import doi_from_url
from ..utils import pages_as_string, to_csl


def write_csl(metadata: Commonmeta) -> Optional[str]:
    """Write CSL-JSON"""
    item = write_csl_item(metadata)
    if item is None:
        return None
    return json.dumps(item)


def write_csl_item(metadata) -> Optional[dict]:
    """Write CSL-JSON item"""
    if metadata is None or metadata.write_errors is not None:
        return None
    if len(wrap(metadata.contributors)) == 0:
        author = None
    else:
        author = to_csl(wrap(metadata.contributors))

    if metadata.type == "Software" and metadata.version is not None:
        _type = "book"
    else:
        _type = CM_TO_CSL_TRANSLATIONS.get(metadata.type, "Document")

    container = metadata.container or {}
    publisher = metadata.publisher or {}
    date = metadata.date or {}

    return compact(
        {
            "type": _type,
            "id": metadata.id,
            "DOI": doi_from_url(metadata.id),
            "URL": metadata.url,
            "categories": parse_attributes(
                wrap(metadata.subjects), content="subject", first=False
            ),
            "language": metadata.language,
            "author": author,
            # "contributor": to_csl(wrap(metadata.contributors)),
            "issued": get_date_parts(date.get("published"))
            if date.get("published", None)
            else None,
            "submitted": get_date_parts(date.get("submitted"))
            if date.get("submitted", None)
            else None,
            "accessed": get_date_parts(date.get("accessed"))
            if date.get("accessed", None)
            else None,
            "abstract": first(
                parse_attributes(
                    metadata.descriptions, content="description", first=True
                )
            ),
            "container-title": container.get("title", None),
            "volume": container.get("volume", None),
            "issue": container.get("issue", None),
            "page": presence(pages_as_string(container)),
            "publisher": publisher.get("name", None),
            "title": first(
                parse_attributes(metadata.titles, content="title", first=True)
            ),
            "copyright": metadata.license.get("id", None) if metadata.license else None,
            "version": metadata.version,
        }
    )


def write_csl_list(metalist):
    """Write CSL-JSON list"""
    if metalist is None:
        return None
    return [write_csl_item(item) for item in metalist.items]
