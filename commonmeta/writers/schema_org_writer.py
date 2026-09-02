"""Schema.org writer for commonmeta-py"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..base_utils import compact, parse_attributes, wrap
from ..constants import CM_TO_SO_TRANSLATIONS
from ..utils import (
    get_identifier,
    get_language,
    github_as_repo_url,
    to_schema_org_creators,
)

if TYPE_CHECKING:
    from ..metadata import Metadata, MetadataList


def write_schema_org(metadata: Metadata, **kwargs) -> dict:
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
    if metadata.type == "Dataset" and container is not None:
        data_catalog = compact(
            {
                "@id": get_identifier(container, "DOI")
                or get_identifier(container, "URL"),
                "@type": "DataCatalog",
                "name": container.get("title", None),
            }
        )
        is_part_of = None
    elif container is not None:
        container_type = container.get("type", None)
        # the two container types schema.org names; the rest say what they are
        # with additionalType, which is where the reader looks for them
        schema_org_container = {"Journal": "Periodical", "Blog": "Blog"}.get(
            container_type, None
        )
        is_part_of = compact(
            {
                "@id": get_identifier(container, "DOI"),
                "@type": schema_org_container,
                "additionalType": (None if schema_org_container else container_type),
                "issn": get_identifier(container, "ISSN"),
                "name": container.get("title", None),
                # the platform a blog is published on is the service behind
                # the container rather than a work of its own, which is what
                # schema.org calls a provider
                "provider": (
                    {"@type": "Organization", "name": container["platform"]}
                    if container.get("platform", None)
                    else None
                ),
            }
        )
        data_catalog = None
    else:
        is_part_of = None
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
            **to_schema_org_relations(metadata.relations),
            "@context": "http://schema.org",
            "@id": metadata.id,
            "@type": schema_org,
            "url": metadata.url,
            "additionalType": additional_type,
            "name": metadata.title,
            "author": to_schema_org_creators(authors) or None,
            "editor": to_schema_org_creators(editors) or None,
            "citation": to_schema_org_citations(metadata.references),
            "description": metadata.description,
            "license": metadata.license.get("url", None) if metadata.license else None,
            "version": metadata.version,
            "keywords": parse_attributes(
                wrap(metadata.subjects), content="subject", first=False
            ),
            # keywords are strings, so the id and scheme of a classification
            # only survive as a DefinedTerm
            "about": to_schema_org_subjects(metadata.subjects),
            "articleBody": metadata.content,
            "image": metadata.image,
            "identifier": to_schema_org_identifiers(metadata.identifiers),
            "funder": to_schema_org_funders(metadata.funding_references),
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
            "isPartOf": is_part_of if is_part_of else None,
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
                # `reference` is what the schema calls the citation text;
                # readers written against earlier drafts still say
                # `unstructured`, and both are accepted here
                "name": r.get("reference", None)
                or r.get("unstructured", None)
                or r.get("title", None),
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


# The commonmeta relation types schema.org has a property for. The seven it has
# none for - IsNewVersionOf, IsPreviousVersionOf, IsVariantFormOf,
# IsOriginalFormOf, IsPreprintOf, HasPreprint and Other - are left out rather
# than written as an extension property no other consumer would read.
CM_TO_SO_RELATION_TYPES = {
    "IsPartOf": "isPartOf",
    "HasPart": "hasPart",
    "IsIdenticalTo": "sameAs",
    # the FRBR reading schema.org gives these: a version is an instance of the
    # work ("the paperback edition, first edition, or eBook")
    "IsVersionOf": "exampleOfWork",
    "HasVersion": "workExample",
    "IsTranslationOf": "translationOfWork",
    "HasTranslation": "workTranslation",
    "IsSupplementTo": "isBasedOn",
    "HasReview": "review",
    "IsReviewOf": "itemReviewed",
}

# what a work that cites this one is, in schema.org: the citation, reversed
CM_TO_SO_REVERSE_RELATION_TYPES = {"IsReferencedBy": "citation"}


def to_schema_org_relations(relations) -> dict:
    """Relations as the schema.org properties that carry them.

    A property takes a single node or a list, so the ones with more than one
    relation of a type get a list. `IsReferencedBy` has no forward property -
    schema.org says it with `@reverse`, which is where the reader looks.
    """
    forward: dict = {}
    reverse: dict = {}
    for relation in wrap(relations):
        _id, _type = relation.get("id", None), relation.get("type", None)
        if not _id or not _type:
            continue
        if _type in CM_TO_SO_RELATION_TYPES:
            forward.setdefault(CM_TO_SO_RELATION_TYPES[_type], []).append(_id)
        elif _type in CM_TO_SO_REVERSE_RELATION_TYPES:
            reverse.setdefault(CM_TO_SO_REVERSE_RELATION_TYPES[_type], []).append(_id)

    def nodes(property_, ids):
        # sameAs is a url in schema.org, the rest are creative works
        items = ids if property_ == "sameAs" else [{"@id": i} for i in ids]
        return items[0] if len(items) == 1 else items

    data = {p: nodes(p, ids) for p, ids in forward.items()}
    if reverse:
        data["@reverse"] = {p: nodes(p, ids) for p, ids in reverse.items()}
    return data


def to_schema_org_subjects(subjects) -> list | None:
    """Subjects as DefinedTerms, which keep the id a keyword string drops."""
    terms = [
        compact(
            {
                "@id": subject.get("id", None),
                "@type": "DefinedTerm",
                "name": subject.get("subject", None),
                "inDefinedTermSet": subject.get("scheme_uri", None)
                or subject.get("scheme", None),
            }
        )
        for subject in wrap(subjects)
        if isinstance(subject, dict) and subject.get("subject", None)
    ]
    return terms or None


def to_schema_org_identifiers(identifiers) -> list | None:
    """Identifiers as PropertyValues, the schema.org way to say what a value is."""
    values = [
        compact(
            {
                "@type": "PropertyValue",
                "propertyID": identifier.get("identifier_type", None),
                "value": identifier.get("identifier", None),
                # the scheme an identifier belongs to, where the record names one
                "name": identifier.get("scheme", None),
            }
        )
        for identifier in wrap(identifiers)
        if isinstance(identifier, dict) and identifier.get("identifier", None)
    ]
    return values or None


def to_schema_org_funders(funding_references) -> list | None:
    """Funders as Organizations, which is what the reader reads back."""
    funders = [
        compact(
            {
                "@id": funding.get("funder_id", None),
                "@type": "Organization",
                "name": funding.get("funder_name", None),
            }
        )
        for funding in wrap(funding_references)
        if isinstance(funding, dict) and funding.get("funder_name", None)
    ]
    return funders or None
