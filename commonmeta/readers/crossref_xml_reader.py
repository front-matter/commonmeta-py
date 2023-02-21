"""crossref_xml reader for commonmeta-py"""
from typing import Optional
import ast
import traceback
import json
import requests
import xmltodict
from pydash import py_

from ..utils import (
    doi_from_url,
    dict_to_spdx,
    normalize_cc_url,
    normalize_issn,
    normalize_url,
    normalize_orcid,
)
from ..base_utils import compact, wrap, presence, sanitize, parse_attributes
from ..date_utils import get_date_from_parts, get_date_from_crossref_parts
from ..doi_utils import doi_as_url, get_doi_ra, crossref_xml_api_url, normalize_doi
from ..constants import (
    Commonmeta,
    CR_TO_DC_TRANSLATIONS,
    CR_TO_SO_TRANSLATIONS,
    CR_TO_CP_TRANSLATIONS,
    CR_TO_BIB_TRANSLATIONS,
    CR_TO_RIS_TRANSLATIONS,
)


def get_crossref_xml(pid: str, **kwargs) -> dict:
    """Get crossref_xml metadata from a DOI"""
    doi = doi_from_url(pid)
    if doi is None:
        return {"state": "not_found"}
    url = crossref_xml_api_url(doi)
    response = requests.get(
        url, kwargs, headers={"Accept": "text/xml;charset=utf-8"}, timeout=5
    )
    if response.status_code != 200:
        return {"state": "not_found"}
    data = xmltodict.parse(response.text)

    # workaround for eval, used to clean up xmltodict output
    null = None
    data = eval(json.dumps(data))

    return data


def read_crossref_xml(data: Optional[dict], **kwargs) -> Commonmeta:
    """read_crossref_xml"""
    if data is None:
        return {"state": "not_found"}

    meta = py_.get(data, "crossref_result.query_result.body.query.doi_record", {})

    # query contains information from outside metadata schema, e.g. publisher name
    query = py_.get(data, "crossref_result.query_result.body.query", {})

    # read_options = ActiveSupport::HashWithIndifferentAccess.
    # new(options.except(:doi, :id, :url,
    # :sandbox, :validate, :ra))
    read_options = kwargs or {}

    resource_type = None
    bibliographic_metadata = {}
    program_metadata = {}
    journal_metadata = {}
    book_metadata = {}
    book_series_metadata = {}
    journal_issue = {}
    issn = None

    publisher = next(
        (
            i
            for i in wrap(query.get("crm-item", None))
            if i.get("@name", None) == "publisher-name"
        ),
        {},
    ).get("#text", None)

    # fetch metadata depending of Crossref type
    if py_.get(meta, "crossref.journal", None):
        journal_metadata = py_.get(meta, "crossref.journal.journal_metadata", {})
        journal_issue = py_.get(meta, "crossref.journal.journal_issue", {})
        journal_article = py_.get(meta, "crossref.journal.journal_article", {})
        bibliographic_metadata = journal_article or journal_issue or journal_metadata
        program_metadata = py_.get(
            bibliographic_metadata, "crossmark.custom_metadata.ai:program"
        ) or py_.get(bibliographic_metadata, "ai:program")
        if journal_article:
            resource_type = "JournalArticle"
        elif journal_issue:
            resource_type = "JournalIssue"
        else:
            resource_type = "Journal"
    elif py_.get(meta, "crossref.posted_content", None):
        bibliographic_metadata = py_.get(meta, "crossref.posted_content", {})
        if publisher is None:
            publisher = py_.get(
                bibliographic_metadata, "institution.institution_name", None
            )
        resource_type = "PostedContent"
    elif py_.get(meta, "crossref.book", None):
        book_metadata = py_.get(meta, "crossref.book.book_metadata", {})
        book_series_metadata = py_.get(meta, "crossref.book.book_series_metadata", {})
        book_set_metadata = py_.get(meta, "crossref.book.book_set_metadata", {})
        bibliographic_metadata = (
            py_.get(meta, "crossref.book.content_item")
            or book_metadata
            or book_series_metadata
            or book_set_metadata
        )
        if bibliographic_metadata.get("@component_type", None):
            component_type = bibliographic_metadata.get(
                "@component_type", ""
            ).capitalize()
            resource_type = f"Book{component_type}"
        else:
            resource_type = "Book"
    elif py_.get(meta, "crossref.conference", None):
        event_metadata = py_.get(meta, "crossref.conference.event_metadata", {})
        bibliographic_metadata = py_.get(
            meta, "crossref.conference.conference_paper", {}
        )
        resource_type = "ConferencePaper"
    elif py_.get(meta, "crossref.sa_component", None):
        bibliographic_metadata = py_.get(
            meta, "crossref.sa_component.component_list.component", {}
        )
        resource_type = "Component"
    elif py_.get(meta, "crossref.database", None):
        bibliographic_metadata = py_.get(meta, "crossref.database.dataset", {})
        resource_type = "Dataset"
    elif py_.get(meta, "crossref.report_paper", None):
        bibliographic_metadata = py_.get(
            meta, "crossref.report_paper.report_paper_metadata", {}
        )
        resource_type = "Report"
    elif py_.get(meta, "crossref.peer_review", None):
        bibliographic_metadata = py_.get(meta, "crossref.peer_review", {})
        resource_type = "PeerReview"
    elif py_.get(meta, "crossref.dissertation", None):
        bibliographic_metadata = py_.get(meta, "crossref.dissertation", {})
        resource_type = "Dissertation"

    pid = normalize_doi(
        kwargs.get("doi", None)
        or kwargs.get("pid", None)
        or py_.get(bibliographic_metadata, "doi_data.doi")
    )
    if pid:
        doi = doi_from_url(pid)
    else:
        doi = None
    if resource_type is None:
        resource_type == ""

    url = normalize_url(py_.get(bibliographic_metadata, "doi_data.resource"))

    schema_org = CR_TO_SO_TRANSLATIONS.get(resource_type, None) or "CreativeWork"
    types = compact(
        {
            "resourceTypeGeneral": CR_TO_DC_TRANSLATIONS.get(resource_type, None)
            or "Text",
            "resourceType": resource_type,
            "schemaOrg": schema_org,
            "citeproc": CR_TO_CP_TRANSLATIONS.get(resource_type, None)
            or "article-journal",
            "bibtex": CR_TO_BIB_TRANSLATIONS.get(resource_type, None) or "misc",
            "ris": CR_TO_RIS_TRANSLATIONS.get(resource_type, None) or "GEN",
        }
    )

    if bibliographic_metadata.get("titles", None):

        def format_element(element):
            if element is None or (
                element.get("title", None) is None
                and element.get("original_language_title", None) is None
            ):
                return None
            if isinstance(element.get("title", None), str):
                return {"title": sanitize(element.get("title", ""))}
            if element.get("original_language_title", None):
                return {
                    "title": sanitize(
                        py_.get(element, "original_language_title.__content__")
                    ),
                    "lang": py_.get(element, "original_language_title.language"),
                }
            return compact({"title": sanitize(py_.get(element, "title.__content__"))})

        titles = [
            format_element(i) for i in wrap(bibliographic_metadata.get("titles", None))
        ]
    else:
        titles = None

    # date_registered = wrap(query.to_h['crm_item']).find do |cr|
    #     cr['name'] == 'deposit-timestamp'
    # if date_registered:
    #     date_registered = get_datetime_from_time(date_registered.get('__content__', None))

    date_created = next(
        (
            i
            for i in wrap(query.get("crm-item", None))
            if i.get("@name", None) == "created"
        ),
        {},
    ).get("#text", None)

    date_issued = get_date_from_crossref_parts(
        bibliographic_metadata.get("publication_date", {})
    )
    date_published = date_issued or date_created
    date_updated = next(
        (
            i
            for i in wrap(query.get("crm-item", None))
            if i.get("@name", None) == "last-update"
        ),
        {},
    ).get("#text", None)
    dates = [{"date": date_published, "dateType": "Issued"}]
    if date_updated is not None:
        dates.append({"date": date_updated, "dateType": "Updated"})
    publication_year = int(date_published[:4]) if date_published else None

    descriptions = crossref_description(bibliographic_metadata)
    funding_references = crossref_funding(
        wrap(py_.get(bibliographic_metadata, "fr:program.fr:assertion"))
    )

    if journal_metadata:
        issn = next(
            (
                i
                for i in wrap(journal_metadata.get("issn", None))
                if i.get("@media_type", None) == "electronic"
            ),
            {},
        ).get("#text", None)
        container = compact(
            {
                "type": "Journal",
                "identifier": issn,
                "identifierType": "ISSN" if issn else None,
                "title": parse_attributes(journal_metadata.get("full_title", None)),
                "volume": parse_attributes(
                    py_.get(journal_issue, "journal_volume.volume")
                ),
                "issue": parse_attributes(journal_issue.get("issue", None)),
                "firstPage": py_.get(bibliographic_metadata, "pages.first_page"),
                # parse_attributes(journal_article.to_h.dig('publisher_item', 'item_number'),first: true),
                "lastPage": py_.get(bibliographic_metadata, "pages.last_page"),
            }
        )
    # By using book_metadata, we can account for where resource_type is `BookChapter` and not assume its a whole book
    elif book_metadata:
        #   identifiers = crossref_alternate_identifiers(book_metadata)
        container = compact(
            {
                "type": "Book",
                "title": py_.get(book_metadata, "titles.title"),
                "firstPage": py_.get(bibliographic_metadata, "pages.first_page"),
                "lastPage": py_.get(bibliographic_metadata, "pages.last_page"),
                #'identifiers' => identifiers
            }
        )

    elif book_series_metadata.get("series_metadata", None):
        issn = normalize_issn(py_.get(book_series_metadata, "series_metadata.issn"))
        container = {
            "type": "Book Series",
            "identifier": issn,
            "identifierType": "ISSN" if issn else None,
            "title": py_.get(book_series_metadata, "series_metadata.titles.title"),
            "volume": bibliographic_metadata.get("volume", None),
        }
    else:
        container = None

    if issn is not None:
        related_items = [
            compact(
                {
                    "relationType": "IsPartOf",
                    "relatedItemIdentifierType": "ISSN",
                    "resourceTypeGeneral": "Collection",
                    "relatedItemIdentifier": issn,
                }
            )
        ]
    else:
        related_items = []
    related_items += [
        crossref_related_item(i)
        for i in wrap(py_.get(bibliographic_metadata, "citation_list.citation"))
    ]

    language = journal_metadata.get("@language", None)
    agency = bibliographic_metadata.get("@reg-agency", None) or get_doi_ra(pid)
    state = "findable" if meta or read_options else "not_found"

    return {
        # required properties
        "pid": pid,
        "doi": doi,
        "url": url,
        "creators": crossref_people(bibliographic_metadata, "author"),
        "titles": presence(titles),
        "types": types,
        "publisher": publisher,
        "publication_year": publication_year,
        # recommended and optional properties
        "subjects": presence(None),
        "contributors": crossref_people(bibliographic_metadata, "editor"),
        "dates": dates,
        "language": language,
        "alternate_identifiers": None,
        "sizes": None,
        "formats": None,
        "version": None,
        "rights": crossref_rights(program_metadata),
        "descriptions": presence(descriptions),
        "geo_locations": None,
        "funding_references": presence(funding_references),
        "related_items": related_items,
        # other properties
        "date_created": None,
        "date_registered": None,
        "date_published": None,
        "date_updated": None,
        "content_url": presence(meta.get("contentUrl", None)),
        "container": container,
        "agency": agency.capitalize() if agency else None,
        "state": state,
        "schema_version": None,
    } | read_options


def crossref_description(bibliographic_metadata):
    """Description information from Crossref metadata."""

    def format_abstract(element):
        """Format abstract"""
        if isinstance(element.get("jats:p", None), list):
            element["jats:p"] = element["jats:p"][0]
        if isinstance(element.get("jats:p", None), dict):
            element["jats:p"] = element["jats:p"]["#text"]
        description_type = (
            "Abstract" if element.get("@abstract-type", None) == "abstract" else "Other"
        )
        return compact(
            {
                "descriptionType": description_type,
                "description": sanitize(
                    parse_attributes(element, content="jats:p", first=True)
                ),
            }
        )

    return [
        format_abstract(i)
        for i in wrap(bibliographic_metadata.get("jats:abstract", None))
    ]


def crossref_people(bibliographic_metadata, contributor_role="author"):
    """Person information from Crossref metadata."""

    def format_affiliation(element):
        """Format affiliation"""
        return {"name": element}

    def format_person(element):
        """Format person"""
        element["givenName"] = element.get("given_name", None)
        element["familyName"] = element.get("surname", None)
        element["nameType"] = "Personal"
        element["affiliation"] = presence(
            [format_affiliation(i) for i in wrap(element.get("affiliation", None))]
        )
        if element.get("ORCID", None) is not None:
            orcid = element.get("ORCID")
            orcid = orcid.get("#text", None) if isinstance(orcid, dict) else orcid
            element["nameIdentifiers"] = [
                {
                    "nameIdentifier": normalize_orcid(orcid),
                    "nameIdentifierScheme": "ORCID",
                    "schemeUri": "https://orcid.org",
                }
            ]
        element = py_.omit(
            element, "@contributor_role", "@sequence", "given_name", "surname", "ORCID"
        )
        return compact(element)

    def format_organization(element):
        """Format organization"""
        return compact({element})

    person = py_.get(
        bibliographic_metadata, "contributors.person_name"
    ) or bibliographic_metadata.get("person_name", None)
    organization = wrap(py_.get(bibliographic_metadata, "contributors.organization"))
    # + [format_organization(i) for i in wrap(organization)]
    return compact(
        [
            format_person(i)
            for i in wrap(person)
            if i.get("@contributor_role", None) == contributor_role
        ]
    )

    # if contributor_role == 'author' and wrap(person).select do |a|
    #          a['contributor_role'] == 'author'
    #        end.blank? && Array.wrap(organization).select do |a|
    #                        a['contributor_role'] == 'author'
    #                      end.blank?
    #       person = [{ 'name' => ':(unav)', 'contributor_role' => 'author' }]
    #     end

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
    #           elsif a.is_a?(Hash) && a.key?('__content__') && a['__content__'].strip.blank?
    #             nil
    #           elsif a.is_a?(Hash) && a.key?('__content__')
    #             { 'name' => a['__content__'] }
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
    #           'name' => a['name'] || a['__content__'] }


def crossref_related_item(reference: Optional[dict]) -> Optional[dict]:
    """Get related_item from Crossref reference"""
    if reference is None or not isinstance(reference, dict):
        return None
    doi = reference.get("doi", None)
    if isinstance(doi, dict):
        doi = doi.get("#text", None)
    metadata = {
        "key": reference.get("@key", None),
        "relationType": "References",
        "relatedItemType": None,
    }
    if doi is not None:
        metadata = metadata | {
            "relatedItemIdentifier": normalize_doi(doi),
            "relatedItemIdentifierType": "DOI",
        }
    else:
        metadata = metadata | {
            "creator": reference.get("author", None),
            "title": reference.get("article_title", None),
            "publisher": reference.get("publisher", None),
            "publicationYear": reference.get("cYear", None),
            "volume": reference.get("volume", None),
            "issue": reference.get("issue", None),
            "firstPage": reference.get("first_page", None),
            "lastPage": reference.get("last_page", None),
            "containerTitle": reference.get("journal_title", None),
            "edition": None,
            "contributor": None,
            "unstructured": reference.get("unstructured", None),
        }
    return compact(metadata)


def crossref_funding(funding_references: list) -> list:
    """Get funding references from Crossref"""

    def format_element(element):
        """Format element"""
        pid = py_.get(element, "fr:assertion.fr:assertion.#text")
        doi = doi_as_url("10.13039/" + pid) if pid and pid.startswith("5011") else None
        return compact(
            {
                "funderName": py_.get(element, "fr:assertion.#text"),
                "funderIdentifier": doi,
                "funderIdentifierType": "Crossref Funder ID" if doi else None,
            }
        )

    return [format_element(i) for i in funding_references]

    # )
    # if (
    #     funding.get("name", None) is not None
    #     and funding.get("award", None) is not None
    # ):
    #     for award in wrap(funding["award"]):
    #         fund_ref = funding_reference.copy()
    #         fund_ref["awardNumber"] = award
    #         formatted_funding_references.append(fund_ref)
    # elif funding_reference != {}:
    #     formatted_funding_references.append(funding_reference)


def crossref_rights(program_metadata):
    """Get rights from Crossref"""
    def format_element(element):
        """Format element"""
        rights_uri = element.get("#text", None)
        rights_uri = normalize_cc_url(rights_uri)
        return dict_to_spdx({"rightsUri": rights_uri})

    return [format_element(i) for i in wrap(program_metadata.get('ai:license_ref', None)) if i.get('@applies_to', None) == 'vor']
