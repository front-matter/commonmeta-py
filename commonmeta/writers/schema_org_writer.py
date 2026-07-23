"""Schema.org writer for commonmeta-py"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..base_utils import compact, container_identifier, parse_attributes, wrap
from ..constants import CM_TO_SO_TRANSLATIONS
from ..utils import get_language, github_as_repo_url, to_schema_org_creators

if TYPE_CHECKING:
    from ..metadata import Metadata, MetadataList


def write_schema_org(metadata: Metadata) -> dict:
    """Write schema.org"""
    container = metadata.container
    if metadata.type == "Dataset" and metadata.files is not None:
        media_objects = [
            compact(
                {
                    "@type": "DataDownload",
                    "contentUrl": file.get("url"),
                    "encodingFormat": file.get("mime_type", None),
                    "name": file.get("key", None),
                    "sha256": (
                        file["checksum"]
                        if file.get("checksum", None)
                        and file["checksum"].startswith("sha256")
                        else None
                    ),
                    "size": file.get("size", None),
                }
            )
            for file in metadata.files
        ]
    elif metadata.files is not None:
        media_objects = [
            compact(
                {
                    "@type": "MediaObject",
                    "contentUrl": file.get("url"),
                    "encodingFormat": file.get("mime_type", None),
                    "name": file.get("key", None),
                    "sha256": (
                        file["checksum"]
                        if file.get("checksum", None)
                        and file["checksum"].startswith("sha256")
                        else None
                    ),
                    "size": file.get("size", None),
                }
            )
            for file in metadata.files
        ]
    else:
        media_objects = None
    cid, cid_type = container_identifier(container)
    if metadata.type == "Dataset" and container is not None:
        data_catalog = compact(
            {
                "@id": cid if cid_type in ("DOI", "URL") else None,
                "@type": "DataCatalog",
                "name": container.get("title", None),
            }
        )
        periodical = None
    elif container is not None:
        is_journal = container.get("type", None) == "Journal"
        periodical = compact(
            {
                "@id": cid if cid_type == "DOI" else None,
                "@type": "Periodical" if is_journal else None,
                "additionalType": None if is_journal else container.get("type", None),
                "issn": cid if cid_type == "ISSN" else None,
                "name": container.get("title", None),
            }
        )
        data_catalog = None
    else:
        periodical = None
        data_catalog = None
    schema_org = CM_TO_SO_TRANSLATIONS.get(metadata.type, "CreativeWork")
    additional_type = metadata.additional_type
    authors = [au for au in wrap(metadata.contributors) if au["roles"] == ["Author"]]
    editors = [au for au in wrap(metadata.contributors) if au["roles"] == ["Editor"]]
    if metadata.type == "Software":
        rel = next(
            (
                relation
                for relation in metadata.relations
                if relation["type"] == "IsSupplementTo"
            ),
            None,
        )
        code_repository = (
            github_as_repo_url(rel["id"]) if rel and rel.get("id", None) else None
        )
    else:
        code_repository = None

    return compact(
        {
            "@context": "http://schema.org",
            "@id": metadata.id,
            "identifier": [metadata.id] if metadata.id else None,
            "@type": schema_org,
            "url": metadata.url,
            "additionalType": additional_type,
            "name": metadata.title,
            "author": to_schema_org_creators(authors),
            "editor": to_schema_org_creators(editors),
            "citation": to_schema_org_citations(metadata.references),
            "description": metadata.description,
            "license": metadata.license.get("url", None) if metadata.license else None,
            "version": metadata.version,
            "keywords": parse_attributes(
                wrap(metadata.subjects), content="subject", first=False
            ),
            "inLanguage": get_language(metadata.language, format="alpha_2"),
            "dateCreated": (metadata.dates or {}).get("created", None),
            "datePublished": metadata.date_published,
            "dateModified": metadata.date_updated,
            "pageStart": container.get("first_page", None) if container else None,
            "pageEnd": container.get("last_page", None) if container else None,
            # "isPartOf": unwrap(to_schema_org_relations(
            #     related_items=metadata.related_items,
            #     relation_type="IsPartOf",
            # )),
            "periodical": periodical if periodical else None,
            "includedInDataCatalog": data_catalog if data_catalog else None,
            "distribution": media_objects if metadata.type == "Dataset" else None,
            "encoding": media_objects if metadata.type != "Dataset" else None,
            "codeRepository": code_repository,
            "publisher": (
                {
                    "@type": "Organization",
                    "name": metadata.publisher.get("name", None),
                }
                if metadata.publisher
                else None
            ),
            "provider": {"@type": "Organization", "name": metadata.provider or ""},
        }
    )


def to_schema_org_citations(references) -> list | None:
    """Convert v1.0 references to schema.org citations (CreativeWork)."""
    citations = [
        compact(
            {
                "@id": r.get("id", None),
                "@type": "CreativeWork",
                "name": r.get("reference", None) or r.get("title", None),
            }
        )
        for r in wrap(references)
    ]
    return citations or None


def write_schema_org_list(metalist: MetadataList) -> list | None:
    """Write Schema.org list"""
    if metalist is None:
        return None
    return [write_schema_org(item) for item in metalist.items]
