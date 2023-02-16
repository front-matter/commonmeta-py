"""Schema.org writer for Talbot"""
import json
from ..utils import (
    to_schema_org,
    to_schema_org_creators,
    to_schema_org_relations,
)
from ..base_utils import compact, wrap, unwrap, presence, parse_attributes
from ..date_utils import get_date_by_type


def write_schema_org(metadata):
    """Write schema.org"""
    container = metadata.container
    if metadata.types.get("schemaOrg", None) != "Dataset" and container is not None:
        periodical = to_schema_org(container)
    else:
        periodical = None

    dictionary = compact(
        {
            "@context": "http://schema.org",
            "@type": metadata.types.get("schema_org", "ScholarlyArticle")
            if metadata.types is not None
            else None,
            "@id": metadata.pid,
            # 'identifier': metadata.id,
            "url": metadata.url,
            "additionalType": metadata.types.get("resourceType", None)
            if metadata.types is not None
            else None,
            "name": parse_attributes(metadata.titles, content="title", first=True),
            "author": to_schema_org_creators(wrap(metadata.creators)),
            "editor": to_schema_org_creators(wrap(metadata.contributors)),
            "description": parse_attributes(
                metadata.descriptions, content="description", first=True
            ),
            "license": metadata.rights[0].get("rightsUri", None)
            if metadata.rights
            else None,
            "version": metadata.version,
            "keywords": presence(
                parse_attributes(
                    wrap(metadata.subjects), content="subject", first=False
                )
            ),
            "inLanguage": metadata.language,
            "dateCreated": get_date_by_type(metadata.dates, "Created"),
            "datePublished": get_date_by_type(metadata.dates, "Issued")
            or metadata.publication_year,
            "dateModified": get_date_by_type(metadata.dates, "Updated"),
            "pageStart": container.get("firstPage", None) if container else None,
            "pageEnd": container.get("lastPage", None) if container else None,
            "isPartOf": unwrap(to_schema_org_relations(
                related_items=metadata.related_items,
                relation_type="IsPartOf",
            )),
            "periodical": periodical,
            "publisher": {"@type": "Organization", "name": metadata.publisher}
            if metadata.publisher
            else None,
            "provider": {"@type": "Organization", "name": metadata.agency}
            if metadata.agency
            else None,
        }
    )
    return json.dumps(dictionary, indent=4)

    #     "contentSize" => Array.wrap(sizes).unwrap,
    #     "encodingFormat" => Array.wrap(formats).unwrap,
    #     "spatialCoverage" => to_schema_org_spatial_coverage(geo_locations),

    #     "sameAs" => to_schema_org_relation(related_identifiers: related_identifiers, relation_type: "IsIdenticalTo"),
    #     "hasPart" => to_schema_org_relation(related_identifiers: related_identifiers, relation_type: "HasPart"),
    #     "predecessor_of" => to_schema_org_relation(related_identifiers: related_identifiers, relation_type: "IsPreviousVersionOf"),
    #     "successor_of" => to_schema_org_relation(related_identifiers: related_identifiers, relation_type: "IsNewVersionOf"),
    #     "citation" => to_schema_org_relation(related_identifiers: related_identifiers, relation_type: "References"),
    #     "@reverse" => reverse.presence,
    #     "contentUrl" => Array.wrap(content_url).unwrap,
    #     "schemaVersion" => schema_version,
    #         #     "includedInDataCatalog" => types.present? ? ((types["schemaOrg"] == "Dataset") && container.present? ? to_schema_org_container(container, type: "Dataset") : nil) : nil,
    #     "funder" => to_schema_org_funder(funding_references),
