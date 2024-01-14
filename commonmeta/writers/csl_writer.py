"""CSL-JSON writer for commonmeta-py"""
import json

from ..utils import pages_as_string, to_csl
from ..base_utils import wrap, presence, parse_attributes, compact
from ..date_utils import get_date_parts
from ..doi_utils import doi_from_url
from ..constants import CM_TO_CSL_TRANSLATIONS, Commonmeta


def write_csl(metadata: Commonmeta) -> str:
    """Write CSL-JSON"""
    if len(wrap(metadata.contributors)) == 0:
        author = None
    else:
        author = to_csl(wrap(metadata.contributors))

    if metadata.type == "Software" and metadata.version is not None:
        type_ = "book"
    else:
        type_ = CM_TO_CSL_TRANSLATIONS.get(metadata.type, "Document")

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
            # "contributor": to_csl(wrap(metadata.contributors)),
            "issued": get_date_parts(metadata.date.get("published", None)),
            "submitted": get_date_parts(metadata.date.get("submitted"))
            if metadata.date.get("submitted", None)
            else None,
            "abstract": parse_attributes(
                metadata.descriptions, content="description", first=True
            ),
            "container-title": container.get("title", None),
            "volume": container.get("volume", None),
            "issue": container.get("issue", None),
            "page": pages_as_string(container),
            "publisher": metadata.publisher.get("name", None),
            "title": parse_attributes(metadata.titles, content="title", first=True),
            "copyright": metadata.license.get("id", None) if metadata.license else None,
            "version": metadata.version,
        }
    )
    return json.dumps(data, indent=4)
