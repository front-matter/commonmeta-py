import json
from ..utils import (compact, wrap, presence, to_schema_org, to_schema_org_creators, 
    to_schema_org_contributors, to_schema_org_relation, parse_attributes, get_date)
from ..doi_utils import doi_from_url

def write_schema_org(metadata):
    """Write schema.org"""
    container = metadata.container or {}
    if metadata.types.get("schemaOrg", None) != "Dataset" and container is not None:
        periodical = to_schema_org(container)
    else:
        periodical = None

    dictionary = compact({
        '@context': 'http://schema.org',
        '@type': metadata.types.get('schema_org', 'ScholarlyArticle') if metadata.types is not None else None,
        '@id': metadata.id,
        # 'identifier': metadata.id,
        'url': metadata.url,
        'additionalType': metadata.types.get('resourceType', None) if metadata.types is not None else None,
        'name': parse_attributes(metadata.titles, content='title', first=True),
        'author': to_schema_org_creators(metadata.creators),
        'editor': to_schema_org_contributors(metadata.contributors),
        'description': parse_attributes(metadata.descriptions, content='description', first=True),
        'license': metadata.rights_list[0].get('rightsURI', None) if metadata.rights_list else None,
        'version': metadata.version_info,
        'keywords': presence(parse_attributes(wrap(metadata.subjects), content='subject', first=False)),
        'inLanguage': metadata.language,
        'dateCreated': get_date(metadata.dates, 'Created'),
        'datePublished': get_date(metadata.dates, 'Issued') or metadata.publication_year,
        'dateModified': get_date(metadata.dates, 'Updated'),
        'pageStart': container.get('firstPage', None),
        'pageEnd': container.get('lastPage', None),
        'isPartOf': to_schema_org_relation(related_identifiers=metadata.related_identifiers, relation_type="IsPartOf"),
        'periodical': periodical,
        'publisher': { "@type": "Organization", "name": metadata.publisher } if metadata.publisher else None,
        'provider': { "@type": "Organization", "name": metadata.agency } if metadata.agency else None,
    })
    return json.dumps(dictionary, indent = 4)

      #     "keywords" => subjects.present? ? Array.wrap(subjects).map { |k| parse_attributes(k, content: "subject", first: true) }.join(", ") : nil,
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