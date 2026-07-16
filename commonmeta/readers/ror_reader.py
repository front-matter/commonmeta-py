"""ROR reader for Commonmeta.

Reads a `ROR v2 API <https://ror.readme.io/v2/docs/data-structure>`_ record and
returns a commonmeta *organization* entity. The inverse is
:mod:`commonmeta.writers.ror_writer`.
"""

from __future__ import annotations

import requests

from ..base_utils import compact, presence, wrap
from ..constants import (
    ROR_TO_CM_IDENTIFIER_TYPES,
    ROR_TO_CM_RELATION_TYPES,
    Commonmeta,
)
from ..utils import normalize_ror, validate_ror


def get_ror(pid: str | None, **kwargs) -> dict:
    """Fetch a ROR record by ROR ID or URL."""
    ror = validate_ror(pid)
    if ror is None:
        return {"state": "not_found"}
    url = f"https://api.ror.org/v2/organizations/{ror}"
    response = requests.get(url, timeout=10, **kwargs)
    if response.status_code != 200:
        return {"state": "not_found"}
    return {**response.json(), "via": "ror"}


def read_ror(data: dict | None, **kwargs) -> Commonmeta:
    """read_ror"""
    if data is None:
        return {"state": "not_found"}
    meta = data
    read_options = kwargs or {}

    _id = normalize_ror(meta.get("id", None))

    names = wrap(meta.get("names", None))

    def name_of(*types: str) -> str | None:
        """First name value carrying any of the given ROR name types."""
        for name in names:
            if set(wrap(name.get("types", None))) & set(types):
                return name.get("value", None)
        return None

    name = name_of("ror_display")
    acronym = name_of("acronym")

    # Aliases and labels other than the display name. ROR tags the display name
    # with both "label" and "ror_display", so exclude it explicitly rather than
    # relying on the value comparison alone.
    additional_names = [
        value
        for i in names
        if (set(wrap(i.get("types", None))) & {"alias", "label"})
        and "ror_display" not in wrap(i.get("types", None))
        and (value := i.get("value", None))
        and value != name
    ]

    identifiers = []
    for external_id in wrap(meta.get("external_ids", None)):
        identifier_type = ROR_TO_CM_IDENTIFIER_TYPES.get(
            (external_id.get("type", None) or "").lower()
        )
        if identifier_type is None:
            continue
        # `preferred` is null when ROR holds several equivalent ids and hasn't
        # picked one; fall back to the first of `all`.
        identifier = external_id.get("preferred", None) or next(
            iter(wrap(external_id.get("all", None))), None
        )
        if not identifier:
            continue
        identifiers.append(
            {"identifier": identifier, "identifier_type": identifier_type}
        )

    urls = [
        {"name": i.get("type", None), "url": i.get("value", None)}
        for i in wrap(meta.get("links", None))
        if i.get("value", None)
    ]

    locations = wrap(meta.get("locations", None))
    country = None
    if locations:
        country = locations[0].get("geonames_details", {}).get("country_code", None)

    geo_locations = [
        geo for i in locations if (geo := format_geo_location(i)) is not None
    ]

    relations = [
        compact(
            {
                "id": normalize_ror(i.get("id", None)),
                "type": ROR_TO_CM_RELATION_TYPES.get(i.get("type", None), "Other"),
                "name": i.get("label", None),
            }
        )
        for i in wrap(meta.get("relationships", None))
        if validate_ror(i.get("id", None))
    ]

    return {
        **compact(
            {
                "id": _id,
                "name": name,
                "acronym": acronym,
                "additional_names": presence(additional_names),
                "types": presence([i.lower() for i in wrap(meta.get("types", None))]),
                "status": meta.get("status", None),
                "established": meta.get("established", None),
                "date_updated": (meta.get("admin", None) or {})
                .get("last_modified", {})
                .get("date", None),
                "identifiers": presence(identifiers),
                "urls": presence(urls),
                "country": country,
                "geo_locations": presence(geo_locations),
                "relations": presence(relations),
                "asserted_by": "ROR",
            }
        ),
        **read_options,
    }


def format_geo_location(location: dict) -> dict | None:
    """Convert a ROR location to a commonmeta geo_location."""
    details = location.get("geonames_details", None) or {}
    latitude = details.get("lat", None)
    longitude = details.get("lng", None)
    # ROR sends 0/0 for records with no resolved coordinates; that's the Null
    # Island placeholder rather than a real location, so skip it.
    if not latitude and not longitude:
        return None

    name = details.get("name", None)
    subdivision = details.get("country_subdivision_name", None)
    country_name = details.get("country_name", None)
    # "Alexandria, Virginia, United States", but avoid "Vancouver, Vancouver,
    # Canada" for city-states and places named after their subdivision.
    parts = [name, subdivision if subdivision != name else None, country_name]
    place = ", ".join([i for i in parts if i])

    geonames_id = location.get("geonames_id", None)
    return compact(
        {
            "id": f"https://www.geonames.org/{geonames_id}" if geonames_id else None,
            "place": presence(place),
            "point_latitude": latitude,
            "point_longitude": longitude,
        }
    )
