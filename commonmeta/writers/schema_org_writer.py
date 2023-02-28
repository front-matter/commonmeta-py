"""Schema.org writer for commonmeta-py"""
import json
from ..utils import (
    to_schema_org,
    to_schema_org_creators
)
from ..base_utils import compact, wrap, presence, parse_attributes
from ..constants import CM_TO_SO_TRANSLATIONS


def write_schema_org(metadata):
    """Write schema.org"""
    container = metadata.container
    if metadata.type != "Dataset" and container is not None:
        periodical = to_schema_org(container)
    else:
        periodical = None
    schema_org = CM_TO_SO_TRANSLATIONS.get(metadata.type, "CreativeWork")
    additional_type = metadata.additional_type

    data = compact(
        {
            "@context": "http://schema.org",
            "@id": metadata.id,
            # 'identifier': metadata.id,
            "@type": schema_org,
            "url": metadata.url,
            "additionalType": additional_type,
            "name": parse_attributes(metadata.titles, content="title", first=True),
            "author": to_schema_org_creators(wrap(metadata.creators)),
            "editor": to_schema_org_creators(wrap(metadata.contributors)),
            "description": parse_attributes(
                metadata.descriptions, content="description", first=True
            ),
            "license": metadata.license.get("url", None)
            if metadata.license
            else None,
            "version": metadata.version,
            "keywords": presence(
                parse_attributes(
                    wrap(metadata.subjects), content="subject", first=False
                )
            ),
            "inLanguage": metadata.language,
            "dateCreated": metadata.date.get('created', None),
            "datePublished": metadata.date.get('published', None),
            "dateModified": metadata.date.get('updated', None),
            "pageStart": container.get("firstPage", None) if container else None,
            "pageEnd": container.get("lastPage", None) if container else None,
            # "isPartOf": unwrap(to_schema_org_relations(
            #     related_items=metadata.related_items,
            #     relation_type="IsPartOf",
            # )),
            "periodical": periodical,
            "publisher": {"@type": "Organization", "name": metadata.publisher.get("name", None)}
            if metadata.publisher
            else None,
            "provider": {"@type": "Organization", "name": metadata.provider}
            if metadata.provider
            else None,
        }
    )
    return json.dumps(data, indent=4)

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
