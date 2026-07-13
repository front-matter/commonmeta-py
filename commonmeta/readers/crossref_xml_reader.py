"""crossref_xml reader for commonmeta-py"""

from __future__ import annotations

import requests

from ..author_utils import get_authors
from ..base_utils import (
    compact,
    dig,
    first,
    parse_attributes,
    parse_xml,
    pascal_case,
    presence,
    sanitize,
    unique,
    wrap,
)
from ..constants import (
    CR_TO_CM_CONTAINER_TRANSLATIONS,
    CR_TO_CM_TRANSLATIONS,
    CROSSREF_CONTAINER_TYPES,
    Commonmeta,
)
from ..date_utils import get_date_from_crossref_parts, get_iso8601_date
from ..doi_utils import crossref_xml_api_url, get_doi_ra, normalize_doi
from ..utils import (
    dict_to_spdx,
    doi_from_url,
    from_crossref_xml,
    issn_as_url,
    normalize_cc_url,
    normalize_issn,
    normalize_url,
    validate_id,
)


def get_crossref_xml(pid: str, **kwargs) -> dict:
    """Get crossref_xml metadata from a DOI"""
    doi = doi_from_url(pid)
    if doi is None:
        return {"state": "not_found"}
    url = crossref_xml_api_url(doi)
    response = requests.get(
        url, headers={"Accept": "text/xml;charset=utf-8"}, timeout=10, **kwargs
    )
    if response.status_code != 200:
        return {"state": "not_found"}

    dct = parse_xml(response.text, dialect="crossref")
    return dct if isinstance(dct, dict) else {"state": "not_found"}


def read_crossref_xml(data: dict | None, **kwargs) -> Commonmeta:
    """read_crossref_xml"""
    if data is None:
        return {"state": "not_found"}
    meta = dig(data, "crossref_result.query_result.body.query.doi_record.crossref", {})

    # query contains information from outside metadata schema, e.g. publisher name
    query = dig(data, "crossref_result.query_result.body.query", {})

    # read_options = ActiveSupport::HashWithIndifferentAccess.
    # new(options.except(:doi, :id, :url,
    # :sandbox, :validate, :ra))
    read_options = kwargs or {}

    # organization.id is ROR-only per the v1.0 schema; Crossref member API
    # URLs have no ROR equivalent, so publisher carries no id here (matching
    # crossref_reader.py, the JSON-based Crossref reader, which never sets
    # one either).
    publisher = compact(
        {
            "name": next(
                (
                    i
                    for i in wrap(query.get("crm-item", None))
                    if i.get("name", None) == "publisher-name"
                ),
                {},
            ).get("#text", None),
        }
    )

    # fetch metadata depending of Crossref type
    if dig(meta, "journal.journal_article", None):
        bibmeta = dig(meta, "journal.journal_article", {})
        resource_type = "journal-article"
        language = dig(meta, "journal.journal_metadata.language")
    elif dig(meta, "journal.journal_issue", None):
        bibmeta = dig(meta, "journal.journal_issue", {})
        resource_type = "journal-issue"
        language = dig(meta, "journal.journal_metadata.language")
    elif dig(meta, "journal", None):
        bibmeta = dig(meta, "journal", {})
        resource_type = "journal"
        language = dig(meta, "journal.journal_metadata.language")
    elif dig(meta, "posted_content", None):
        bibmeta = meta.get("posted_content", {})
        if publisher.get("name", None) is None:
            publisher = {"name": dig(bibmeta, "institution.institution_name", None)}
        resource_type = "posted-content"
        language = dig(meta, "posted_content.language")
    elif dig(meta, "book.content_item"):
        bibmeta = dig(meta, "book.content_item")
        resource_type = "book-chapter"
        language = dig(meta, "book.book_metadata.language")
    elif dig(meta, "book.book_series_metadata"):
        bibmeta = dig(meta, "book.book_series_metadata")
        resource_type = "book-series"
        language = bibmeta.get("language", None)
    elif dig(meta, "book.book_set_metadata"):
        bibmeta = dig(meta, "book.book_set_metadata")
        resource_type = "book-set"
        language = bibmeta.get("language", None)
    elif dig(meta, "book.book_metadata"):
        bibmeta = dig(meta, "book.book_metadata")
        resource_type = "book"
        language = bibmeta.get("language", None)
    elif dig(meta, "conference", None):
        bibmeta = dig(meta, "conference.conference_paper", {})
        resource_type = "proceedings-article"
        language = bibmeta.get("language", None)
    elif dig(meta, "sa_component", None):
        bibmeta = dig(meta, "sa_component.component_list.component", {})
        resource_type = "component"
        language = None
    elif dig(meta, "database", None):
        bibmeta = dig(meta, "database.dataset", {})
        resource_type = "dataset"
        language = dig(meta, "database.database_metadata.language")
    elif dig(meta, "report_paper", None):
        bibmeta = dig(meta, "report_paper.report_paper_metadata", {})
        resource_type = "report"
        language = bibmeta.get("language", None)
    elif dig(meta, "peer_review", None):
        bibmeta = dig(meta, "peer_review", {})
        resource_type = "peer-review"
        language = bibmeta.get("language", None)
    elif dig(meta, "dissertation", None):
        bibmeta = dig(meta, "dissertation", {})
        resource_type = "dissertation"
        language = bibmeta.get("language", None)
    else:
        bibmeta = {}
        resource_type = ""
        language = None

    _id = normalize_doi(
        kwargs.get("doi", None)
        or kwargs.get("id", None)
        or dig(bibmeta, "doi_data.doi")
    )
    _type = CR_TO_CM_TRANSLATIONS.get(resource_type, "Other")
    # Front Matter blog content is registered as posted-content (Preprint) or a
    # journal (Journal) but maps to BlogPost / Blog. Front Matter may be the
    # publisher (Rogue Scholar) or the institution (Crossref-registered blogs).
    institution_names = [
        i.get("institution_name", None)
        for i in wrap(dig(bibmeta, "institution"))
        if isinstance(i, dict)
    ]
    if "Front Matter" in institution_names or dig(publisher, "name") == "Front Matter":
        if _type == "Preprint":
            _type = "BlogPost"
        elif _type == "Journal":
            _type = "Blog"

    url = first(parse_attributes(dig(bibmeta, "doi_data.resource")))
    url = normalize_url(url)
    title, additional_titles = crossref_titles(bibmeta)
    contributors = crossref_people(bibmeta)

    created = next(
        (
            i
            for i in wrap(query.get("crm-item", None))
            if i.get("name", None) == "created"
        ),
        {},
    ).get("#text", None)
    updated = next(
        (
            i
            for i in wrap(query.get("crm-item", None))
            if i.get("name", None) == "last-update"
        ),
        {},
    ).get("#text", None)
    published = (
        get_date_from_crossref_parts(bibmeta.get("publication_date", {}))
        or get_date_from_crossref_parts(bibmeta.get("review_date", {}))
        or created
    )
    # date_published is normalized to a plain ISO date; date_updated keeps the
    # full Crossref timestamp (e.g. 2018-08-23T13:41:49Z).
    date_published = get_iso8601_date(published)
    date_updated = updated
    dates = crossref_dates(bibmeta)

    description, additional_descriptions = crossref_description(bibmeta)

    # fr:program / ai:program / rel:program all deserialize as `program`,
    # both directly under the work and nested inside crossmark metadata.
    programs = wrap(bibmeta.get("program", None)) + wrap(
        dig(bibmeta, "crossmark.custom_metadata.program")
    )
    funding_references = crossref_funding(programs)
    license_ = crossref_license(programs)

    # By using book_metadata, we can account for where resource_type is `BookChapter` and not assume its a whole book
    # if book_metadata:
    #     #   identifiers = crossref_alternate_identifiers(book_metadata)
    #     container = compact(
    #         {
    #             "type": "Book",
    #             "title": dig(book_metadata, "titles.title"),
    #             "firstPage": dig(bibmeta, "pages.first_page"),
    #             "lastPage": dig(bibmeta, "pages.last_page"),
    #             #'identifiers' => identifiers
    #         }
    #     )

    # elif book_series_metadata.get("series_metadata", None):
    #     issn = normalize_issn(
    #         dig(book_series_metadata, "series_metadata.issn.0.#text")
    #     )
    #     container = compact(
    #         {
    #             "type": "Book Series",
    #             "identifier": issn,
    #             "identifierType": "ISSN" if issn else None,
    #             "title": dig(book_series_metadata, "series_metadata.titles.title"),
    #             "volume": bibmeta.get("volume", None),
    #         }
    #     )
    # else:
    #     container = None
    container = crossref_container(meta, resource_type=resource_type)
    if _type == "BlogPost" and container:
        container = {**container, "type": "Blog"}
    references = crossref_references(dig(bibmeta, "citation_list.citation"))
    files = crossref_files(dig(bibmeta, "doi_data.collection"))
    identifiers = crossref_identifiers(_id, bibmeta)
    archive_locations = crossref_archive_locations(bibmeta)
    relations = crossref_relations(container, programs)
    provider = bibmeta.get("reg-agency", None)
    provider = provider.capitalize() if provider else get_doi_ra(_id)
    state = "findable" if meta or read_options else "not_found"

    return {
        # required properties
        "id": _id,
        "type": _type,
        # recommended and optional properties
        "additional_descriptions": presence(additional_descriptions),
        "additional_titles": presence(additional_titles),
        "archive_locations": presence(archive_locations),
        "container": presence(container),
        "contributors": presence(contributors),
        "date_published": presence(date_published),
        "date_updated": presence(date_updated),
        "dates": presence(dates),
        "description": description,
        "files": presence(files),
        "funding_references": presence(funding_references),
        "geo_locations": None,
        "identifiers": presence(identifiers),
        "language": language,
        "license": presence(license_),
        "provider": provider,
        "publisher": publisher,
        "references": references,
        "relations": presence(relations),
        "state": state,
        "subjects": presence(None),
        "title": title,
        "url": url,
        "version": None,
    } | read_options


def crossref_titles(bibmeta: dict) -> tuple[str | None, list]:
    """Title information from Crossref metadata.

    Returns a tuple of (title, additional_titles) per the commonmeta v1.0
    schema, where title is a single scalar string and additional_titles
    holds subtitles/translated titles.
    """
    title = first(parse_attributes(dig(bibmeta, "titles.0.title")))
    subtitle = first(parse_attributes(dig(bibmeta, "titles.0.subtitle")))
    original_language_title = first(
        parse_attributes(dig(bibmeta, "titles.0.original_language_title"))
    )
    language = first(
        parse_attributes(
            dig(bibmeta, "titles.0.original_language_title"), content="language"
        )
    )
    if title is None and original_language_title is None:
        return None, []
    if original_language_title and title is None:
        # no separate translated title: original_language_title is the
        # only title present, so it's the primary title, not a translation.
        return sanitize(original_language_title), []
    if original_language_title:
        return sanitize(title), [
            compact(
                {
                    "title": sanitize(original_language_title),
                    "type": "TranslatedTitle",
                    "language": language,
                }
            )
        ]
    additional_titles = (
        [
            {
                "title": sanitize(subtitle),
                "type": "Subtitle",
            }
        ]
        if subtitle
        else []
    )
    return sanitize(title), additional_titles


def _abstract_paragraph_text(paragraph) -> str:
    """Extract the text of a single JATS ``<p>`` element."""
    if isinstance(paragraph, dict):
        return paragraph.get("#text") or paragraph.get("font") or ""
    return paragraph or ""


def map_abstract_type(raw: str | None) -> str:
    """Map a Crossref abstract-type attribute to a commonmeta description type."""
    return {
        None: "Abstract",
        "": "Abstract",
        "abstract": "Abstract",
        "executive-summary": "Summary",
        "summary": "Summary",
        "methods": "Methods",
        "materials|methods": "Methods",
        "technical-info": "TechnicalInfo",
        "technical_info": "TechnicalInfo",
    }.get(raw, "Other")


def crossref_description(bibmeta: dict) -> tuple[str | None, list]:
    """Description information from Crossref metadata.

    Returns a tuple of (description, additional_descriptions) per the
    commonmeta v1.0 schema, where description is a single scalar string.
    All ``<p>`` paragraphs of an abstract are joined with a single space.
    """

    def format_abstract(element: dict) -> dict:
        """Format abstract"""
        text = " ".join(
            _abstract_paragraph_text(p).strip() for p in wrap(element.get("p", None))
        ).strip()
        return compact(
            {
                "type": map_abstract_type(element.get("abstract-type", None)),
                "description": sanitize(text) if text else None,
            }
        )

    abstracts = [format_abstract(i) for i in wrap(bibmeta.get("abstract", None))]
    abstracts = [a for a in abstracts if a.get("description", None)]
    if not abstracts:
        return None, []
    description = abstracts[0].get("description", None)
    additional_descriptions = [
        compact(
            {"description": a.get("description", None), "type": a.get("type", None)}
        )
        for a in abstracts[1:]
    ]
    return description, additional_descriptions


def crossref_dates(bibmeta: dict) -> dict:
    """Submitted/accepted dates from Crossmark publication-history assertions."""
    dates: dict = {}
    for assertion in wrap(dig(bibmeta, "crossmark.custom_metadata.assertion")):
        if not isinstance(assertion, dict):
            continue
        name = assertion.get("name", None)
        text = assertion.get("#text", None)
        if not text:
            continue
        if name == "received":
            dates["submitted"] = text
        elif name == "accepted":
            dates["accepted"] = text
    return dates


def crossref_people(bibmeta: dict) -> list:
    """Person information from Crossref metadata."""

    person = dig(bibmeta, "contributors.person_name") or bibmeta.get(
        "person_name", None
    )
    organization = wrap(dig(bibmeta, "contributors.organization"))

    return get_authors(from_crossref_xml(wrap(person) + wrap(organization)))

    #     (Array.wrap(person) + Array.wrap(organization)).select do |a|
    #       a['contributor_role'] == contributor_role
    #     end.map do |a|
    #       name_identifiers = if normalize_orcid(parse_attributes(a['ORCID'])).present?
    #                            [{
    #                              'nameIdentifier' => normalize_orcid(parse_attributes(a['ORCID'])), 'nameIdentifierScheme' => 'ORCID', 'schemeUri' => 'https://orcid.org'
    #                            }]
    #                          end
    #       if a['surname'].present? || a['given_name'].present? || name_identifiers.present?
    #         given_name = parse_attributes(a['given_name'])
    #         family_name = parse_attributes(a['surname'])
    #         affiliation = Array.wrap(a['affiliation']).map do |a|
    #           if a.is_a?(Hash)
    #             a
    #           elsif a.is_a?(Hash) && a.key?('#text') && a[#text'].strip.blank?
    #             nil
    #           elsif a.is_a?(Hash) && a.key?('_#text_')
    #             { 'name' => a['#text'] }
    #           elsif a.strip.blank?
    #             nil
    #           elsif a.is_a?(String)
    #             { 'name' => a }
    #           end
    #         end.compact

    #         { 'nameType' => 'Personal',
    #           'nameIdentifiers' => name_identifiers,
    #           'name' => [family_name, given_name].compact.join(', '),
    #           'givenName' => given_name,
    #           'familyName' => family_name,
    #           'affiliation' => affiliation.presence,
    #           'contributorType' => contributor_role == 'editor' ? 'Editor' : nil }.compact
    #       else
    #         { 'nameType' => 'Organizational',
    #           'name' => a['name'] || a['#text'] }


def normalize_provider(provider: str | None) -> str | None:
    """Normalize a Crossref DOI provider to a commonmeta provider name."""
    if not provider:
        return None
    return {
        "crossref": "Crossref",
        "publisher": "Publisher",
        "author": "Author",
    }.get(provider, provider)


def crossref_reference(reference: dict | None) -> dict | None:
    """Get reference from a Crossref citation.

    The citation's ``doi`` may be a bare string or a dict carrying a
    ``@provider`` attribute. Per the commonmeta v1.0 reference schema the
    structured ``article_title`` maps to ``reference`` (the formatted
    string); an unstructured citation without an article title falls back to
    the ``unstructured`` text on write. A citation with neither a DOI nor
    unstructured text is dropped (returns None).
    """
    if reference is None or not isinstance(reference, dict):
        return None
    doi_el = reference.get("doi", None)
    if isinstance(doi_el, dict):
        doi = doi_el.get("#text", None)
        provider = doi_el.get("provider", None)
    else:
        doi = doi_el
        provider = None
    doi = doi.strip() if isinstance(doi, str) else doi
    _id = normalize_doi(doi) if doi else None

    unstructured = reference.get("unstructured_citation", None)
    if isinstance(unstructured, dict):
        unstructured = unstructured.get("font", None) or unstructured.get("#text", None)

    if not _id and not unstructured:
        return None

    # The formatted reference string prefers the unstructured citation, then
    # falls back to the structured article title.
    reference_text = (
        sanitize(unstructured) if unstructured else reference.get("article_title", None)
    )

    return compact(
        {
            "key": reference.get("key", None),
            "id": _id,
            "reference": reference_text,
            "asserted_by": normalize_provider(provider) if _id else None,
        }
    )


def crossref_references(citations) -> list:
    """Build the reference list, dropping duplicate keys and empty citations."""
    out: list = []
    seen: set = set()
    for citation in wrap(citations):
        reference = crossref_reference(citation)
        if reference is None:
            continue
        key = reference.get("key", None)
        if key:
            if key in seen:
                continue
            seen.add(key)
        out.append(reference)
    return out


def crossref_files(collection) -> list:
    """Get text-mining files from Crossref ``doi_data.collection`` items."""
    out: list = []
    seen: set = set()
    for coll in wrap(collection):
        for item in wrap(coll.get("item", None) if isinstance(coll, dict) else None):
            resource = item.get("resource", None) if isinstance(item, dict) else None
            if isinstance(resource, dict):
                url = resource.get("#text", None)
                mime_type = resource.get("mime_type", None)
            else:
                url = resource
                mime_type = None
            if not url or not mime_type or url in seen:
                continue
            seen.add(url)
            out.append({"url": url, "mime_type": mime_type})
    return out


def crossref_archive_locations(bibmeta: dict) -> list:
    """Get archive names from Crossref ``archive_locations``."""
    return [
        a.get("name", None)
        for a in wrap(dig(bibmeta, "archive_locations.archive"))
        if isinstance(a, dict) and a.get("name", None)
    ]


def crossref_identifiers(doi_id: str | None, bibmeta: dict) -> list:
    """Get identifiers (DOI plus any publisher item number) from Crossref."""
    identifiers: list = []
    if doi_id:
        identifiers.append({"identifier": doi_id, "identifier_type": "DOI"})
    for item in wrap(dig(bibmeta, "publisher_item.item_number")):
        if isinstance(item, dict):
            text = item.get("#text", None)
            raw_type = item.get("item_number_type", None)
        else:
            text = item
            raw_type = None
        if not text:
            continue
        identifiers.append(map_item_number(raw_type, text))
    return identifiers


# Crossref item_number types that map directly onto commonmeta identifier_type
# values (Crossref uppercases the type name).
_KNOWN_ITEM_NUMBER_TYPES = {
    "ARK",
    "BIBCODE",
    "DOI",
    "HANDLE",
    "ISBN",
    "ISSN",
    "OPENALEX",
    "PMID",
    "PMCID",
    "PURL",
    "RAID",
    "SWHID",
    "URL",
    "URN",
    "GUID",
}


def map_item_number(raw_type: str | None, text: str) -> dict:
    """Map a Crossref publisher item_number to a commonmeta identifier."""
    rt = (raw_type or "").upper()
    if rt == "UUID":
        if len(text) == 32:
            text = f"{text[:8]}-{text[8:12]}-{text[12:16]}-{text[16:20]}-{text[20:]}"
        return {"identifier": text, "identifier_type": "UUID"}
    if rt == "ARXIV":
        return {"identifier": text, "identifier_type": "arXiv"}
    identifier_type = rt if rt in _KNOWN_ITEM_NUMBER_TYPES else "Other"
    return {"identifier": text, "identifier_type": identifier_type}


def resolve_relation_id(text: str, id_type: str | None) -> str | None:
    """Resolve a related-item identifier to a normalized URL/PID."""
    if id_type == "doi":
        return normalize_doi(text)
    if id_type == "issn":
        return issn_as_url(text)
    pid, _ = validate_id(text)
    return pid or text


def crossref_relations(container: dict | None, programs: list) -> list:
    """Get relations: an ISSN IsPartOf plus any rel:program related items."""
    out: list = []
    if (
        container
        and container.get("identifier_type", None) == "ISSN"
        and container.get("identifier", None)
    ):
        url = issn_as_url(container["identifier"])
        if url:
            out.append({"id": url, "type": "IsPartOf"})
    # the relations program (rel:program) carries the related_item elements
    for program in programs:
        if not isinstance(program, dict):
            continue
        for item in wrap(program.get("related_item", None)):
            if not isinstance(item, dict):
                continue
            for rel_key in ("inter_work_relation", "intra_work_relation"):
                relation = item.get(rel_key, None)
                if not isinstance(relation, dict):
                    continue
                text = relation.get("#text", None)
                if not text:
                    continue
                _id = resolve_relation_id(text, relation.get("identifier-type", None))
                _type = pascal_case(relation.get("relationship-type", None) or "")
                if _id and _type:
                    out.append({"id": _id, "type": _type})
    return unique(out)


def crossref_container(meta: dict, resource_type: str = "JournalArticle") -> dict:
    """Get container from Crossref"""
    container_type = CROSSREF_CONTAINER_TYPES.get(resource_type, None)
    issn = next(
        (
            i
            for i in wrap(dig(meta, f"{container_type}.{container_type}_metadata.issn"))
            + wrap(
                dig(
                    meta,
                    f"{container_type}.{container_type}_series_metadata.series_metadata.issn",
                )
            )
            if i.get("media_type", None) == "electronic"
        ),
        {},
    ) or next(
        (
            i
            for i in wrap(dig(meta, f"{container_type}.{container_type}_metadata.issn"))
            + wrap(
                dig(
                    meta,
                    f"{container_type}.{container_type}_series_metadata.series_metadata.issn",
                )
            )
            if i.get("media_type", None) == "print"
        ),
        {},
    )
    issn = normalize_issn(issn) if issn else None
    isbn = dig(meta, f"conference.{container_type}_metadata.isbn.#text")
    container_title = (
        dig(meta, f"{container_type}.{container_type}_metadata.full_title")
        or dig(meta, f"{container_type}.{container_type}_metadata.titles.0.title")
        or dig(meta, f"conference.{container_type}_metadata.{container_type}_title")
        or dig(
            meta,
            f"{container_type}.{container_type}_series_metadata.series_metadata.titles.0.title",
        )
    )
    volume = dig(
        meta,
        f"{container_type}.{container_type}_issue.{container_type}_volume.volume",
    )
    issue = dig(meta, f"{container_type}.{container_type}_issue.issue")
    return compact(
        {
            "type": CR_TO_CM_CONTAINER_TRANSLATIONS.get(container_type, None),
            "identifier": issn or isbn,
            "identifier_type": "ISSN" if issn else "ISBN" if isbn else None,
            "title": container_title,
            "volume": volume,
            "issue": issue,
            "first_page": dig(
                meta, f"{container_type}.{container_type}_article.pages.first_page"
            )
            or dig(meta, f"{container_type}.content_item.pages.first_page")
            or dig(meta, "conference.conference_paper.pages.first_page"),
            "last_page": dig(
                meta, f"{container_type}.{container_type}_article.pages.last_page"
            )
            or dig(meta, f"{container_type}.content_item.pages.last_page")
            or dig(meta, "conference.conference_paper.pages.last_page"),
            "location": dig(meta, "conference.event_metadata.conference_location"),
            "series": dig(meta, "conference.event_metadata.conference_acronym"),
        }
    )


def crossref_funding(programs: list) -> list:
    """Get funding references from the first fundref (fr:program) program."""
    program = next(
        (
            p
            for p in programs
            if isinstance(p, dict) and p.get("name", None) == "fundref"
        ),
        None,
    )
    if not program:
        return []
    references: list = []
    for fundgroup in wrap(program.get("assertion", None)):
        if not isinstance(fundgroup, dict) or fundgroup.get("name", None) != "fundgroup":
            continue
        assertions = wrap(fundgroup.get("assertion", None))
        award_numbers = [
            a.get("#text", None)
            for a in assertions
            if isinstance(a, dict) and a.get("name", None) == "award_number"
        ]
        funder_name = None
        funder_id = None
        for assertion in assertions:
            if not isinstance(assertion, dict) or assertion.get("name") != "funder_name":
                continue
            funder_name = (assertion.get("#text", None) or "").strip()
            for child in wrap(assertion.get("assertion", None)):
                if (
                    not isinstance(child, dict)
                    or child.get("name", None) != "funder_identifier"
                ):
                    continue
                raw = (child.get("#text", None) or "").strip()
                if child.get("provider", None) == "crossref":
                    funder_id = normalize_doi(f"10.13039/{raw}")
                else:
                    funder_id = normalize_doi(raw) or raw
        if not funder_name:
            continue
        base = compact({"funder_id": funder_id, "funder_name": funder_name})
        if not award_numbers:
            references.append(base)
        else:
            for award in award_numbers:
                references.append(compact({**base, "award_number": award}))
    return unique(references)


def crossref_license(programs: list) -> dict | None:
    """Get license from the AccessIndicators (ai:program) program.

    The program is identified by carrying a ``license_ref``; some publishers
    deposit it without the ``AccessIndicators`` name attribute.
    """
    program = next(
        (
            p
            for p in programs
            if isinstance(p, dict) and p.get("license_ref", None)
        ),
        None,
    )
    if not program:
        return None
    license_refs = wrap(program.get("license_ref", None))
    if not license_refs:
        return None
    element = next(
        (
            r
            for r in license_refs
            if isinstance(r, dict) and r.get("applies_to", None) == "vor"
        ),
        license_refs[0],
    )
    url = normalize_cc_url(first(parse_attributes(element)))
    return dict_to_spdx({"url": url})
