"""ROR writer for commonmeta-py.

Writes a commonmeta *organization* entity as a `ROR v2 API
<https://ror.readme.io/v2/docs/data-structure>`_ record: the inverse of
:mod:`commonmeta.readers.ror_reader`, so a ROR record read and written back
returns to its original shape.

Only what commonmeta models is written. A ROR record carries fields commonmeta
has no home for (``domains``, ``admin.created``, per-name ``lang``, the GeoNames
``continent_*``/``country_subdivision_code`` detail), and those are not
reconstructed - reading ROR into commonmeta is lossy, and writing it back cannot
invent what was dropped.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..base_utils import compact, presence, wrap
from ..constants import CM_TO_ROR_IDENTIFIER_TYPES, CM_TO_ROR_RELATION_TYPES

if TYPE_CHECKING:
    from ..metadata import Metadata


def write_ror(metadata: Metadata | None) -> dict | None:
    """Write a commonmeta organization as a ROR v2 API record."""
    if metadata is None:
        return None
    if getattr(metadata, "entity_type", None) != "organization":
        raise ValueError("Only organization entities can be written as ROR")

    return compact(
        {
            "id": metadata.id,
            "admin": presence(format_admin(metadata)),
            "established": metadata.established,
            "external_ids": presence(format_external_ids(metadata)),
            "links": presence(format_links(metadata)),
            "locations": presence(format_locations(metadata)),
            "names": presence(format_names(metadata)),
            "relationships": presence(format_relationships(metadata)),
            "status": metadata.status,
            "types": presence(wrap(metadata.types)),
        }
    )


def format_admin(metadata: Metadata) -> dict:
    """The admin block, which carries the last-modified date."""
    if not metadata.date_updated:
        return {}
    return {"last_modified": {"date": metadata.date_updated, "schema_version": "2.1"}}


def format_names(metadata: Metadata) -> list:
    """Rebuild ROR's names list from name/acronym/additional_names.

    ROR tags the display name with both "ror_display" and "label"; aliases and
    the acronym are separate entries. `lang` isn't modelled by commonmeta, so it
    is left null.
    """
    names = []
    if metadata.name:
        names.append(
            {"lang": None, "types": ["label", "ror_display"], "value": metadata.name}
        )
    if metadata.acronym:
        names.append({"lang": None, "types": ["acronym"], "value": metadata.acronym})
    for value in wrap(metadata.additional_names):
        names.append({"lang": None, "types": ["alias"], "value": value})
    return names


def format_external_ids(metadata: Metadata) -> list:
    """Rebuild ROR's external_ids from commonmeta identifiers.

    commonmeta keeps a single value per identifier, so `all` has one entry and
    `preferred` repeats it - the distinction ROR draws between them isn't
    modelled.
    """
    external_ids = []
    for identifier in wrap(metadata.identifiers):
        ror_type = CM_TO_ROR_IDENTIFIER_TYPES.get(identifier.get("identifier_type"))
        value = identifier.get("identifier")
        if ror_type is None or not value:
            continue
        external_ids.append({"all": [value], "preferred": value, "type": ror_type})
    return external_ids


def format_links(metadata: Metadata) -> list:
    """Rebuild ROR's links, whose `type` is the commonmeta url name."""
    return [
        {"type": url.get("name"), "value": url.get("url")}
        for url in wrap(metadata.urls)
        if url.get("url")
    ]


def format_locations(metadata: Metadata) -> list:
    """Rebuild ROR's locations from geo_locations plus the country code.

    `place` is a composed "city, subdivision, country" string, so it is split
    back on ", ": one part is the city, two are city+country, three are
    city+subdivision+country. A city whose name contains a comma would split
    wrongly, which is why the reader's composition is the authority and this is
    best-effort.
    """
    locations = []
    for geo_location in wrap(metadata.geo_locations):
        geonames_id = None
        if geo_location.get("id"):
            tail = str(geo_location["id"]).rstrip("/").rsplit("/", 1)[-1]
            geonames_id = int(tail) if tail.isdigit() else None

        parts = [i.strip() for i in (geo_location.get("place") or "").split(",")]
        parts = [i for i in parts if i]
        name = parts[0] if parts else None
        subdivision = parts[1] if len(parts) > 2 else None
        country_name = parts[-1] if len(parts) > 1 else None

        details = compact(
            {
                "country_code": metadata.country,
                "country_name": country_name,
                "country_subdivision_name": subdivision,
                "lat": geo_location.get("point_latitude"),
                "lng": geo_location.get("point_longitude"),
                "name": name,
            }
        )
        locations.append(
            compact({"geonames_id": geonames_id, "geonames_details": presence(details)})
        )
    return locations


def format_relationships(metadata: Metadata) -> list:
    """Rebuild ROR's relationships, whose `label` is the commonmeta name."""
    relationships = []
    for relation in wrap(metadata.relations):
        ror_type = CM_TO_ROR_RELATION_TYPES.get(relation.get("type"))
        if ror_type is None or not relation.get("id"):
            continue
        relationships.append(
            compact(
                {
                    "id": relation.get("id"),
                    "label": relation.get("name"),
                    "type": ror_type,
                }
            )
        )
    return relationships
