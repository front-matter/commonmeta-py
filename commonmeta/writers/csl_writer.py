"""CSL-JSON writer for commonmeta-py"""

from typing import Optional

import orjson as json
import orjsonl
import yaml

from ..base_utils import compact, parse_attributes, presence, wrap
from ..constants import CM_TO_CSL_TRANSLATIONS, Commonmeta
from ..date_utils import get_date_parts
from ..doi_utils import doi_from_url
from ..file_utils import get_extension, write_gz_file, write_zip_file
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
            "categories": presence(
                parse_attributes(
                    wrap(metadata.subjects), content="subject", first=False
                )
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
            "abstract": parse_attributes(
                metadata.descriptions, content="description", first=True
            ),
            "container-title": container.get("title", None),
            "volume": container.get("volume", None),
            "issue": container.get("issue", None),
            "page": presence(pages_as_string(container)),
            "publisher": publisher.get("name", None),
            "title": parse_attributes(metadata.titles, content="title", first=True),
            "copyright": metadata.license.get("id", None) if metadata.license else None,
            "version": metadata.version,
        }
    )


def write_csl_list(metalist):
    """Write CSL-JSON list"""
    if metalist is None:
        return None
    items = [write_csl_item(item) for item in metalist.items]

    if metalist.file:
        filename, extension, compress = get_extension(metalist.file)
        if not extension:
            extension = "json"
        if extension == "jsonl":
            orjsonl.save(metalist.file, items)
        elif extension == "json":
            json_output = json.dumps(items).decode("utf-8")
            if compress == "gz":
                write_gz_file(filename, json_output)
            elif compress == "zip":
                write_zip_file(filename, json_output)
            else:
                with open(metalist.file, "w") as file:
                    file.write(json_output)
        elif extension == "yaml":
            yaml_output = yaml.dump(items).decode("utf-8")
            if compress == "gz":
                write_gz_file(filename, yaml_output)
            elif compress == "zip":
                write_zip_file(filename, yaml_output)
            else:
                with open(metalist.file, "w") as file:
                    file.write(yaml_output)
        return metalist.file
    else:
        return json.dumps(items)
