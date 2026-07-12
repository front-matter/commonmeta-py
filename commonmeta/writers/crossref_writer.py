"""Crossref JSON writer for commonmeta-py"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..base_utils import compact, wrap
from ..doi_utils import doi_from_url

if TYPE_CHECKING:
    from ..metadata import Metadata, MetadataList

# commonmeta type → Crossref REST API type
_CM_TO_CR_TYPE: dict[str, str] = {
    "Preprint": "posted-content",
    "Blog": "journal",
    "BlogPost": "posted-content",
    "BlogVolume": "journal-volume",
    "BookChapter": "book-chapter",
    "BookSeries": "book-series",
    "Book": "book",
    "Component": "component",
    "Dataset": "dataset",
    "Dissertation": "dissertation",
    "Grant": "grant",
    "JournalArticle": "journal-article",
    "JournalIssue": "journal-issue",
    "JournalVolume": "journal-volume",
    "Journal": "journal",
    "PeerReview": "peer-review",
    "ProceedingsArticle": "proceedings-article",
    "ProceedingsSeries": "proceedings-series",
    "Proceedings": "proceedings",
    "ReportComponent": "report-component",
    "ReportSeries": "report-series",
    "Report": "report",
    "Standard": "standard",
}


def _cr_type(cm_type: str | None) -> str:
    return _CM_TO_CR_TYPE.get(cm_type or "", "other")


def _parse_date_to_parts(date: str | None) -> list[list[int]] | None:
    """Convert an ISO 8601 date string to Crossref date-parts format."""
    if not date:
        return None
    date_only = date.split("T")[0]
    parts = []
    for segment in date_only.split("-"):
        try:
            parts.append(int(segment))
        except ValueError:
            break
    return [parts] if parts else None


def _contributor_to_cr(contributor: dict, sequence: str) -> dict:
    """Convert a commonmeta v1.0 contributor to a Crossref author/editor dict."""
    person = contributor.get("person")
    organization = contributor.get("organization")

    if organization:
        return compact(
            {
                "name": organization.get("name"),
                "sequence": sequence,
            }
        )

    if not person:
        return {"sequence": sequence}

    orcid = person.get("id", "")
    given_name = person.get("given_name") or None
    family_name = person.get("family_name") or None

    authenticated_orcid = None
    if orcid:
        asserted_by = person.get("asserted_by", "")
        authenticated_orcid = asserted_by == "Author"

    affiliations = []
    for aff in wrap(person.get("affiliations")):
        aff_id = aff.get("identifier", "")
        aff_ids = []
        if aff_id:
            id_type = aff.get("identifier_type", "") or "other"
            asserted_by = aff.get("asserted_by", "publisher")
            aff_ids.append(
                {
                    "id": aff_id,
                    "id-type": id_type,
                    "asserted-by": asserted_by.lower(),
                }
            )
        aff_entry = compact({"name": aff.get("name", ""), "id": aff_ids or None})
        if aff_entry:
            affiliations.append(aff_entry)

    result: dict[str, Any] = {"sequence": sequence}
    if orcid:
        result["ORCID"] = orcid
        result["authenticated-orcid"] = authenticated_orcid
    if given_name:
        result["given"] = given_name
    if family_name:
        result["family"] = family_name
    if affiliations:
        result["affiliation"] = affiliations
    return result


def _build_contributors(
    contributors: list[dict] | None,
) -> tuple[list[dict], list[dict]]:
    """Split contributors into author and editor lists."""
    authors: list[dict] = []
    editors: list[dict] = []
    for i, c in enumerate(wrap(contributors)):
        roles = c.get("roles", ["Author"])
        if "Editor" in roles:
            seq = "first" if len(editors) == 0 else "additional"
            editors.append(_contributor_to_cr(c, seq))
        else:
            seq = "first" if len(authors) == 0 else "additional"
            authors.append(_contributor_to_cr(c, seq))
    return authors, editors


def _build_funder(funding_references: list[dict] | None) -> list[dict]:
    """Group funding references by funder, collecting awards."""
    seen: dict[str, dict] = {}
    order: list[str] = []
    for f in wrap(funding_references):
        funder_id = f.get("funder_id", "")
        funder_name = f.get("funder_name", "")
        key = f"{funder_id}|{funder_name}"
        if key not in seen:
            seen[key] = {
                "doi": doi_from_url(funder_id) or "",
                "name": funder_name,
                "award": [],
            }
            order.append(key)
        award = f.get("award_number", "")
        if award:
            seen[key]["award"].append(award)

    result = []
    for key in order:
        entry = seen[key]
        cr_funder: dict[str, Any] = {"name": entry["name"]}
        if entry["doi"]:
            cr_funder["DOI"] = entry["doi"]
        if entry["award"]:
            cr_funder["award"] = entry["award"]
        result.append(cr_funder)
    return result


def _build_references(references: list[dict] | None) -> list[dict]:
    result = []
    for r in wrap(references):
        ref_doi = doi_from_url(r.get("id", "")) or ""
        unstructured = r.get("unstructured", "")
        title = r.get("title", "")
        # Use the separately-stored title; fall back to reference text only
        # when there is no unstructured field (the reference text IS the title).
        article_title = (
            title if title else ("" if unstructured else r.get("reference", ""))
        )
        pub_year = r.get("publication_year", "")
        entry = compact(
            {
                "key": r.get("key", ""),
                "DOI": ref_doi or None,
                "doi-asserted-by": (
                    r.get("asserted_by", "").lower() if ref_doi else None
                ),
                "article-title": article_title or None,
                "unstructured": unstructured or None,
                "year": pub_year or None,
                "volume": r.get("volume", "") or None,
                "issue": r.get("issue", "") or None,
                "first-page": r.get("first_page", "") or None,
                "last-page": r.get("last_page", "") or None,
                "publisher": r.get("publisher", "") or None,
            }
        )
        if entry:
            result.append(entry)
    return result


def _to_cr_work(metadata: Metadata) -> dict:
    cr_type = _cr_type(metadata.type)
    is_posted_content = cr_type == "posted-content"

    doi = doi_from_url(metadata.id) or ""

    # Title / subtitle
    titles: list[str] = []
    subtitles: list[str] = []
    if metadata.title:
        titles.append(metadata.title)
    for t in wrap(metadata.additional_titles):
        if t.get("type") == "Subtitle":
            subtitles.append(t["title"])
        elif t.get("title"):
            titles.append(t["title"])

    authors, editors = _build_contributors(metadata.contributors)

    # Container
    container = metadata.container or {}
    container_title_str = container.get("title", "")
    issn = (
        container.get("identifier")
        if container.get("identifier_type") == "ISSN"
        else None
    )
    volume = container.get("volume") or None
    issue = container.get("issue") or None
    first_page = container.get("first_page", "")
    last_page = container.get("last_page", "")
    if first_page and last_page:
        page = f"{first_page}-{last_page}"
    elif first_page:
        page = first_page
    else:
        page = None

    # posted-content uses group-title; other types use container-title
    if container_title_str and is_posted_content:
        container_title: list[str] = []
        group_title: str | None = container_title_str
    elif container_title_str:
        container_title = [container_title_str]
        group_title = None
    else:
        container_title = []
        group_title = None

    # License: always emit vor + tdm when present
    license_ = metadata.license or {}
    license_url = license_.get("url", "")
    license_list = (
        [
            {"URL": license_url, "content-version": "vor"},
            {"URL": license_url, "content-version": "tdm"},
        ]
        if license_url
        else []
    )

    date_parts = _parse_date_to_parts(metadata.date_published)
    issued = {"date-parts": date_parts} if date_parts else None
    posted = {"date-parts": date_parts} if (date_parts and is_posted_content) else None

    publisher_name = (
        (metadata.publisher or {}).get("name", "") if metadata.publisher else ""
    )

    subjects = [s["subject"] for s in wrap(metadata.subjects) if s.get("subject")]

    funder = _build_funder(metadata.funding_references)
    reference = _build_references(metadata.references)

    url = metadata.url or ""
    resource = {"primary": {"URL": url}} if url else None

    link = [
        {"URL": f.get("url"), "content-type": f.get("mime_type")}
        for f in wrap(metadata.files)
        if f.get("url") and f.get("mime_type") != "unspecified"
    ]

    version = {"version": metadata.version} if metadata.version else None

    doi_url = f"https://doi.org/{doi}" if doi else ""

    work: dict[str, Any] = {}
    if doi:
        work["DOI"] = doi
    work["type"] = cr_type
    if metadata.additional_type:
        work["subtype"] = metadata.additional_type
    if titles:
        work["title"] = titles
    if subtitles:
        work["subtitle"] = subtitles
    if authors:
        work["author"] = authors
    if editors:
        work["editor"] = editors
    if publisher_name:
        work["publisher"] = publisher_name
    if container_title:
        work["container-title"] = container_title
    if group_title:
        work["group-title"] = group_title
    if volume:
        work["volume"] = volume
    if issue:
        work["issue"] = issue
    if page:
        work["page"] = page
    if issn:
        work["ISSN"] = [issn]
    if metadata.description:
        work["abstract"] = f"<jats:p>{metadata.description}</jats:p>"
    if metadata.language:
        work["language"] = metadata.language
    if subjects:
        work["subject"] = subjects
    if license_list:
        work["license"] = license_list
    if funder:
        work["funder"] = funder
    if reference:
        work["reference"] = reference
    if posted:
        work["posted"] = posted
    if issued:
        work["issued"] = issued
    if version:
        work["version"] = version
    if doi_url:
        work["URL"] = doi_url
    if resource:
        work["resource"] = resource
    if link:
        work["link"] = link

    return work


def write_crossref(metadata: Metadata | None) -> dict | None:
    """Serialize a Metadata record as a Crossref REST API JSON response."""
    if metadata is None:
        return None
    return {
        "status": "ok",
        "message-type": "work",
        "message-version": "1.0.0",
        "message": _to_cr_work(metadata),
    }


def write_crossref_list(metalist: MetadataList | None) -> dict | None:
    """Serialize a MetadataList as a Crossref REST API work-list response."""
    if metalist is None:
        return None
    items = [_to_cr_work(m) for m in wrap(metalist.items)]
    return {
        "status": "ok",
        "message-type": "work-list",
        "message-version": "1.0.0",
        "message": {
            "total-results": len(items),
            "items": items,
        },
    }
