"""crossref_xml reader for commonmeta-py"""

from collections import defaultdict
from typing import Optional

import requests

from ..author_utils import get_authors
from ..base_utils import (
    compact,
    dig,
    parse_attributes,
    parse_xml,
    presence,
    sanitize,
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
    normalize_cc_url,
    normalize_issn,
    normalize_url,
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

    return parse_xml(response.text, dialect="crossref") | {"via": "crossref_xml"}


def read_crossref_xml(data: dict, **kwargs) -> Commonmeta:
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

    member_id = next(
        (
            i
            for i in wrap(query.get("crm-item", None))
            if i.get("name", None) == "member-id"
        ),
        {},
    ).get("#text", None)
    publisher_id = (
        "https://api.crossref.org/members/" + member_id if member_id else None
    )
    publisher = compact(
        {
            "id": publisher_id,
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
    if _type == "Article" and dig(publisher, "name") == "Front Matter":
        _type = "BlogPost"

    url = parse_attributes(dig(bibmeta, "doi_data.resource"))
    url = normalize_url(url)
    titles = crossref_titles(bibmeta)
    contributors = crossref_people(bibmeta)

    date: dict = defaultdict(list)
    date["created"] = next(
        (
            i
            for i in wrap(query.get("crm-item", None))
            if i.get("name", None) == "created"
        ),
        {},
    ).get("#text", None)
    date["published"] = (
        get_date_from_crossref_parts(bibmeta.get("publication_date", {}))
        or get_date_from_crossref_parts(bibmeta.get("review_date", {}))
        or date["created"]
    )
    date["updated"] = next(
        (
            i
            for i in wrap(query.get("crm-item", None))
            if i.get("name", None) == "last-update"
        ),
        {},
    ).get("#text", None)

    # TODO: fix timestamp. Until then, remove time as this is not always stable with Crossref (different server timezones)
    date = {k: get_iso8601_date(v) for k, v in date.items()}

    descriptions = crossref_description(bibmeta)
    funding = (
        dig(bibmeta, "program.0")
        or dig(bibmeta, "program.0.assertion")
        or dig(bibmeta, "crossmark.custom_metadata.program.0.assertion")
    )
    funding_references = crossref_funding(wrap(funding))

    license_ = (
        dig(bibmeta, "program.0.license_ref")
        or dig(bibmeta, "crossmark.custom_metadata.program.0.license_ref")
        or dig(bibmeta, "crossmark.custom_metadata.program.1.license_ref")
    )
    license_ = crossref_license(wrap(license_))

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
    references = [
        crossref_reference(i) for i in wrap(dig(bibmeta, "citation_list.citation"))
    ]
    files = presence(meta.get("contentUrl", None))
    provider = (
        bibmeta.get("reg-agency").capitalize()
        if bibmeta.get("reg-agency", None)
        else None
    )
    if provider is None:
        provider = get_doi_ra(_id)
    state = "findable" if meta or read_options else "not_found"

    return {
        # required properties
        "id": _id,
        "type": _type,
        "url": url,
        "contributors": presence(contributors),
        "titles": presence(titles),
        "publisher": publisher,
        "date": compact(date),
        # recommended and optional properties
        "subjects": presence(None),
        "language": language,
        "alternate_identifiers": None,
        "sizes": None,
        "formats": None,
        "version": None,
        "license": presence(license_),
        "descriptions": presence(descriptions),
        "geo_locations": None,
        "funding_references": presence(funding_references),
        "references": references,
        "relations": None,
        # other properties
        "date_created": None,
        "date_registered": None,
        "date_published": None,
        "date_updated": None,
        "content_url": presence(files),
        "container": presence(container),
        "provider": provider,
        "state": state,
        "schema_version": None,
    } | read_options


def crossref_titles(bibmeta):
    """Title information from Crossref metadata."""
    title = parse_attributes(dig(bibmeta, "titles.0.title"))
    subtitle = parse_attributes(dig(bibmeta, "titles.0.subtitle"))
    original_language_title = parse_attributes(
        dig(bibmeta, "titles.0.original_language_title")
    )
    language = parse_attributes(
        dig(bibmeta, "titles.0.original_language_title"), content="language"
    )
    if title is None and original_language_title is None:
        return None
    if title and original_language_title is None and subtitle is None:
        return [{"title": sanitize(title)}]
    if original_language_title:
        return [
            compact(
                {
                    "title": sanitize(original_language_title),
                    "lang": language,
                }
            )
        ]
    if subtitle:
        return [
            compact({"title": sanitize(title)}),
            {
                "title": sanitize(subtitle),
                "titleType": "Subtitle",
            },
        ]


def crossref_description(bibmeta):
    """Description information from Crossref metadata."""

    def format_abstract(element):
        """Format abstract"""
        if isinstance(element.get("p", None), list):
            element["p"] = element["p"][0]
        if isinstance(element.get("p", None), dict):
            element["p"] = element["p"]["#text"]
        description_type = (
            "Abstract" if element.get("abstract-type", None) == "abstract" else "Other"
        )
        return compact(
            {
                "type": description_type,
                "description": sanitize(
                    parse_attributes(element, content="p", first=True)
                ),
            }
        )

    return [format_abstract(i) for i in wrap(bibmeta.get("abstract", None))]


def crossref_people(bibmeta):
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


def crossref_reference(reference: Optional[dict]) -> Optional[dict]:
    """Get reference from Crossref reference"""
    if reference is None or not isinstance(reference, dict):
        return None
    doi = parse_attributes(reference.get("doi", None))
    unstructured = reference.get("unstructured_citation", None)
    if isinstance(unstructured, dict):
        text = unstructured.get("font", None) or unstructured.get("#text", None)
    else:
        text = reference.get("unstructured_citation", None)
    metadata = {
        "key": reference.get("key", None),
        "id": normalize_doi(doi) if doi else None,
        "contributor": reference.get("author", None),
        "title": reference.get("article_title", None),
        "publisher": reference.get("publisher", None),
        "publicationYear": reference.get("cYear", None),
        "volume": reference.get("volume", None),
        "issue": reference.get("issue", None),
        "firstPage": reference.get("first_page", None),
        "lastPage": reference.get("last_page", None),
        "containerTitle": reference.get("journal_title", None),
        "edition": None,
        "unstructured": sanitize(text) if text else None,
    }
    return compact(metadata)


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
            "identifierType": "ISSN" if issn else "ISBN" if isbn else None,
            "title": container_title,
            "volume": volume,
            "issue": issue,
            "firstPage": dig(
                meta, f"{container_type}.{container_type}_article.pages.first_page"
            )
            or dig(meta, f"{container_type}.content_item.pages.first_page")
            or dig(meta, "conference.conference_paper.pages.first_page"),
            "lastPage": dig(
                meta, f"{container_type}.{container_type}_article.pages.last_page"
            )
            or dig(meta, f"{container_type}.content_item.pages.last_page")
            or dig(meta, "conference.conference_paper.pages.last_page"),
            "location": dig(meta, "conference.event_metadata.conference_location"),
            "series": dig(meta, "conference.event_metadata.conference_acronym"),
        }
    )


def crossref_funding(funding: list) -> list:
    """Get assertions from Crossref"""
    return []


def crossref_license(licenses: list) -> dict:
    """Get license from Crossref"""

    def map_element(element):
        """Format element"""
        url = parse_attributes(element)
        url = normalize_cc_url(url)
        return dict_to_spdx({"url": url})

    # return only the first license found
    return next((map_element(i) for i in licenses), None)
