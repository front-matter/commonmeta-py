"""Bidirectional conversion helpers between the old v0.18-ish commonmeta
shape (camelCase, flat contributors, titles[]/descriptions[] arrays, a
nested date object, and a nested geo_locations structure) and the
commonmeta v1.0 wire format (snake_case, scalar title/description/
date_published, flattened funding_references/geo_locations, and a
{type, person|organization, roles} contributor shape).

Readers and writers are v1.0-native; this module is only needed at two
remaining boundaries:
- commonmeta/metadata.py: converts v0.18-shaped input up front, for
  commonmeta_reader.py's pass-through, when fed a v0.18-shaped document
  directly (e.g. an old export). vraix_reader.py (backed by the
  commonmeta_rs Rust crate, not migrated to v1.0) used to be a second
  source here, but is currently disabled - see vraix_reader.py.
- commonmeta/writers/commonmeta_writer.py's write_commonmeta_records_for_rust:
  converts back to v0.18 shape for the same Rust FFI boundary, since
  commonmeta_rs expects camelCase. Also currently unused while that
  integration is disabled, but kept ready for when commonmeta_rs is
  migrated to v1.0 (at which point this conversion becomes unnecessary).
"""

from __future__ import annotations

import re

from .base_utils import compact, presence, wrap
from .constants import CROSSREF_FUNDER_ID_TO_ROR_TRANSLATIONS

_ROR_ID_RE = re.compile(r"^https://ror\.org/[0-9a-z]{9}$")


def _to_ror_id(_id: str | None) -> str | None:
    """organization.id is ROR-only per the v1.0 schema; non-ROR identifiers
    (Wikidata, ISNI, etc.) are dropped rather than leaking a non-ROR id into
    a ROR-only field."""
    if _id and _ROR_ID_RE.match(_id):
        return _id
    return None


# ---------------------------------------------------------------------------
# titles


def titles_to_v1(titles: list | None) -> tuple[str | None, list]:
    """[{title, type, language}, ...] -> (title, additional_titles)"""
    items = wrap(titles)
    if not items:
        return None, []
    title = items[0].get("title", None)
    return title, items[1:]


def v1_to_titles(title: str | None, additional_titles: list | None) -> list | None:
    """(title, additional_titles) -> [{title, type, language}, ...]"""
    items = []
    if title is not None:
        items.append({"title": title})
    items += wrap(additional_titles)
    return presence(items)


# ---------------------------------------------------------------------------
# descriptions


def descriptions_to_v1(descriptions: list | None) -> tuple[str | None, list]:
    """[{description, type, language}, ...] -> (description, additional_descriptions)"""
    items = wrap(descriptions)
    if not items:
        return None, []
    description = items[0].get("description", None)
    return description, items[1:]


def v1_to_descriptions(
    description: str | None, additional_descriptions: list | None
) -> list | None:
    """(description, additional_descriptions) -> [{description, type, language}, ...]"""
    items = []
    if description is not None:
        items.append({"description": description, "type": "Abstract"})
    items += wrap(additional_descriptions)
    return presence(items)


# ---------------------------------------------------------------------------
# date


DATE_SUBFIELDS = [
    "created",
    "submitted",
    "accepted",
    "accessed",
    "available",
    "withdrawn",
]


def date_to_v1(date: dict | None) -> tuple[str | None, str | None, dict | None]:
    """{published, updated, created, ...} -> (date_published, date_updated, dates)"""
    date = date or {}
    date_published = date.get("published", None)
    date_updated = date.get("updated", None)
    dates = compact({k: date.get(k, None) for k in DATE_SUBFIELDS})
    return date_published, date_updated, presence(dates)


def v1_to_date(
    date_published: str | None, date_updated: str | None, dates: dict | None
) -> dict | None:
    """(date_published, date_updated, dates) -> {published, updated, created, ...}"""
    dates = dates or {}
    result = compact(
        {
            "published": date_published,
            "updated": date_updated,
            **{k: dates.get(k, None) for k in DATE_SUBFIELDS},
        }
    )
    return presence(result)


# ---------------------------------------------------------------------------
# contributors
#
# Internal shape (as produced by author_utils.get_authors/get_one_author and
# consumed by every writer): a flat dict, e.g.
#   {id, type: "Person"|"Organization", name, givenName, familyName,
#    affiliations: [{id, name}], contributorRoles: [...]}
# v1.0 shape: {type, person: {...} | organization: {...}, roles: [...]}


def contributor_to_v1(contributor: dict) -> dict:
    """flat internal contributor -> v1.0 {type, person|organization, roles}"""
    _type = contributor.get("type", None) or "Person"
    roles = contributor.get("contributorRoles", None)
    affiliations = [
        compact({"id": _to_ror_id(a.get("id", None)), "name": a.get("name", None)})
        for a in wrap(contributor.get("affiliations", None))
    ]

    if _type == "Organization":
        organization = compact(
            {
                "id": _to_ror_id(contributor.get("id", None)),
                "name": contributor.get("name", None),
            }
        )
        return compact({"type": _type, "organization": organization, "roles": roles})

    person = compact(
        {
            "id": contributor.get("id", None),
            "given_name": contributor.get("givenName", None),
            "family_name": contributor.get("familyName", None),
            "affiliations": presence(affiliations),
        }
    )
    return compact({"type": _type, "person": person, "roles": roles})


def v1_to_contributor(contributor: dict) -> dict:
    """v1.0 {type, person|organization, roles} -> flat internal contributor"""
    _type = contributor.get("type", None) or "Person"
    roles = contributor.get("roles", None)

    if _type == "Organization":
        organization = contributor.get("organization", None) or {}
        return compact(
            {
                "id": organization.get("id", None),
                "type": _type,
                "name": organization.get("name", None),
                "contributorRoles": roles,
            }
        )

    person = contributor.get("person", None) or {}
    affiliations = [
        compact({"id": a.get("id", None), "name": a.get("name", None)})
        for a in wrap(person.get("affiliations", None))
    ]
    return compact(
        {
            "id": person.get("id", None),
            "type": _type,
            "givenName": person.get("given_name", None),
            "familyName": person.get("family_name", None),
            "affiliations": presence(affiliations),
            "contributorRoles": roles,
        }
    )


# ---------------------------------------------------------------------------
# funding_references
#
# Internal shape: {funderName, funderIdentifier, funderIdentifierType,
#                   awardNumber, awardTitle, awardUri}
# v1.0 shape: {funder_id (ROR only), funder_name, award_id, award_title,
#              award_number}


def funding_reference_to_v1(funding: dict) -> dict:
    """flat internal funding reference -> v1.0 flat (ROR-only funder_id)"""
    funder_identifier = funding.get("funderIdentifier", None)
    funder_identifier_type = funding.get("funderIdentifierType", None)
    funder_id = None
    if funder_identifier_type == "ROR":
        funder_id = funder_identifier
    elif funder_identifier_type == "Crossref Funder ID":
        funder_id = CROSSREF_FUNDER_ID_TO_ROR_TRANSLATIONS.get(funder_identifier, None)
    # GRID/ISNI/Ringgold/Other/None have no ROR equivalent: funder_id stays None
    # rather than leaking a non-ROR identifier into a ROR-only field.

    return compact(
        {
            "funder_id": funder_id,
            "funder_name": funding.get("funderName", None),
            "award_id": funding.get("awardUri", None),
            "award_title": funding.get("awardTitle", None),
            "award_number": funding.get("awardNumber", None),
        }
    )


def v1_to_funding_reference(funding: dict) -> dict:
    """v1.0 flat funding reference -> flat internal (camelCase)"""
    funder_id = funding.get("funder_id", None)
    return compact(
        {
            "funderName": funding.get("funder_name", None),
            "funderIdentifier": funder_id,
            "funderIdentifierType": "ROR" if funder_id else None,
            "awardUri": funding.get("award_id", None),
            "awardTitle": funding.get("award_title", None),
            "awardNumber": funding.get("award_number", None),
        }
    )


# ---------------------------------------------------------------------------
# container


def container_to_v1(container: dict | None) -> dict | None:
    if not container:
        return container
    container = dict(container)
    if "identifierType" in container:
        container["identifier_type"] = container.pop("identifierType")
    if "favicon" in container:
        container["image"] = container.pop("favicon")
    if "firstPage" in container:
        container["first_page"] = container.pop("firstPage")
    if "lastPage" in container:
        container["last_page"] = container.pop("lastPage")
    return container


def v1_to_container(container: dict | None) -> dict | None:
    if not container:
        return container
    container = dict(container)
    if "identifier_type" in container:
        container["identifierType"] = container.pop("identifier_type")
    if "image" in container:
        container["favicon"] = container.pop("image")
    if "first_page" in container:
        container["firstPage"] = container.pop("first_page")
    if "last_page" in container:
        container["lastPage"] = container.pop("last_page")
    return container


# ---------------------------------------------------------------------------
# identifiers


def identifiers_to_v1(identifiers: list | None) -> list | None:
    items = []
    for i in wrap(identifiers):
        i = dict(i)
        if "identifierType" in i:
            i["identifier_type"] = i.pop("identifierType")
        items.append(i)
    return presence(items)


def v1_to_identifiers(identifiers: list | None) -> list | None:
    items = []
    for i in wrap(identifiers):
        i = dict(i)
        if "identifier_type" in i:
            i["identifierType"] = i.pop("identifier_type")
        items.append(i)
    return presence(items)


# ---------------------------------------------------------------------------
# files


def files_to_v1(files: list | None) -> list | None:
    items = []
    for f in wrap(files):
        f = dict(f)
        if "mimeType" in f:
            f["mime_type"] = f.pop("mimeType")
        items.append(f)
    return presence(items)


def v1_to_files(files: list | None) -> list | None:
    items = []
    for f in wrap(files):
        f = dict(f)
        if "mime_type" in f:
            f["mimeType"] = f.pop("mime_type")
        items.append(f)
    return presence(items)


# ---------------------------------------------------------------------------
# geo_locations
#
# Internal shape: [{geoLocationPlace, geoLocationPoint: {pointLongitude,
#                    pointLatitude}, geoLocationBox: {westBoundLongitude,
#                    eastBoundLongitude, southBoundLatitude,
#                    northBoundLatitude}, geoLocationPolygon: [...]}]
# v1.0 shape: flat scalars per item, polygon as a WKT string.


def _polygon_points_to_wkt(polygon: list | None) -> str | None:
    points = wrap(polygon)
    if not points:
        return None
    coords = [
        f"{p.get('pointLongitude')} {p.get('pointLatitude')}"
        for p in points
        if p.get("pointLongitude") is not None and p.get("pointLatitude") is not None
    ]
    if not coords:
        return None
    return f"POLYGON(({', '.join(coords)}))"


def _wkt_to_polygon_points(wkt: str | None) -> list | None:
    if not wkt or not wkt.startswith("POLYGON((") or not wkt.endswith("))"):
        return None
    body = wkt[len("POLYGON((") : -2]
    points = []
    for pair in body.split(", "):
        parts = pair.strip().split(" ")
        if len(parts) == 2:
            points.append(
                {"pointLongitude": float(parts[0]), "pointLatitude": float(parts[1])}
            )
    return points or None


def geo_locations_to_v1(geo_locations: list | None) -> list | None:
    items = []
    for g in wrap(geo_locations):
        point = g.get("geoLocationPoint", None) or {}
        box = g.get("geoLocationBox", None) or {}
        items.append(
            compact(
                {
                    "geo_location_place": g.get("geoLocationPlace", None),
                    "geo_location_point_longitude": point.get("pointLongitude", None),
                    "geo_location_point_latitude": point.get("pointLatitude", None),
                    "geo_location_box_west_longitude": box.get(
                        "westBoundLongitude", None
                    ),
                    "geo_location_box_east_longitude": box.get(
                        "eastBoundLongitude", None
                    ),
                    "geo_location_box_south_latitude": box.get(
                        "southBoundLatitude", None
                    ),
                    "geo_location_box_north_latitude": box.get(
                        "northBoundLatitude", None
                    ),
                    "geo_location_polygon": _polygon_points_to_wkt(
                        g.get("geoLocationPolygon", None)
                    ),
                }
            )
        )
    return presence(items)


def v1_to_geo_locations(geo_locations: list | None) -> list | None:
    items = []
    for g in wrap(geo_locations):
        point = compact(
            {
                "pointLongitude": g.get("geo_location_point_longitude", None),
                "pointLatitude": g.get("geo_location_point_latitude", None),
            }
        )
        box = compact(
            {
                "westBoundLongitude": g.get("geo_location_box_west_longitude", None),
                "eastBoundLongitude": g.get("geo_location_box_east_longitude", None),
                "southBoundLatitude": g.get("geo_location_box_south_latitude", None),
                "northBoundLatitude": g.get("geo_location_box_north_latitude", None),
            }
        )
        items.append(
            compact(
                {
                    "geoLocationPlace": g.get("geo_location_place", None),
                    "geoLocationPoint": presence(point),
                    "geoLocationBox": presence(box),
                    "geoLocationPolygon": _wkt_to_polygon_points(
                        g.get("geo_location_polygon", None)
                    ),
                }
            )
        )
    return presence(items)


# ---------------------------------------------------------------------------
# top-level normalization
#
# Superseded by is_v018_shaped()/v018_to_v1() below: Metadata.__init__ no
# longer needs a bidirectional "normalize whatever shape shows up" entry
# point now that every reader except commonmeta_reader's pass-through
# emits genuine v1.0 JSON directly (vraix_reader.py is currently disabled).


def is_v018_contributors(contributors: list | None) -> bool:
    items = wrap(contributors)
    if not items:
        return False
    first_item = items[0]
    return "contributorRoles" in first_item or "givenName" in first_item


# ---------------------------------------------------------------------------
# v0.18 -> v1.0
#
# Metadata.__init__ is v1.0-native: it reads title/date_published/dates/
# contributors-as-{type,person,roles}/etc. directly. One source still
# emits the old v0.18-ish shape and needs converting up front:
#   - commonmeta_reader.py's pass-through, when fed a v0.18-shaped document
#     directly (e.g. an old export).
# vraix_reader.py (records from the commonmeta_rs Rust crate, rename_all =
# "camelCase", not migrated to v1.0) used to be a second source here, but
# is currently disabled - see vraix_reader.py.
# Already-v1.0 input (every other reader, now migrated) passes through
# unchanged.


def is_v018_shaped(meta: dict) -> bool:
    """Detect a v0.18-ish meta dict: present only if at least one
    old-style marker key is set to something other than None."""
    markers = [
        "titles",
        "date",
        "descriptions",
        "additionalType",
        "archiveLocations",
        "fundingReferences",
        "geoLocations",
    ]
    return any(meta.get(k) is not None for k in markers) or is_v018_contributors(
        meta.get("contributors")
    )


def v018_to_v1(meta: dict) -> dict:
    """Convert a v0.18-shaped meta dict into v1.0 shape."""
    meta = dict(meta)

    title, additional_titles = titles_to_v1(meta.pop("titles", None))
    meta["title"] = title
    meta["additional_titles"] = presence(additional_titles)

    description, additional_descriptions = descriptions_to_v1(
        meta.pop("descriptions", None)
    )
    meta["description"] = description
    meta["additional_descriptions"] = presence(additional_descriptions)

    date_published, date_updated, dates = date_to_v1(meta.pop("date", None))
    meta["date_published"] = date_published
    meta["date_updated"] = date_updated
    meta["dates"] = dates

    if meta.get("additionalType") is not None:
        meta["additional_type"] = meta.pop("additionalType")
    if meta.get("archiveLocations") is not None:
        meta["archive_locations"] = meta.pop("archiveLocations")

    if "contributors" in meta:
        meta["contributors"] = presence(
            [contributor_to_v1(c) for c in wrap(meta["contributors"])]
        )

    if meta.get("fundingReferences") is not None:
        meta["funding_references"] = [
            funding_reference_to_v1(f) for f in wrap(meta.pop("fundingReferences"))
        ]

    if meta.get("geoLocations") is not None:
        meta["geo_locations"] = geo_locations_to_v1(meta.pop("geoLocations"))

    if "container" in meta:
        meta["container"] = container_to_v1(meta["container"])

    if "identifiers" in meta:
        meta["identifiers"] = identifiers_to_v1(meta["identifiers"])

    if "files" in meta:
        meta["files"] = files_to_v1(meta["files"])
    if "relations" in meta:
        meta["relations"] = presence(meta["relations"])

    return meta
