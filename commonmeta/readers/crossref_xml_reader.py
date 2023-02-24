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
from ..base_utils import (
    compact,
    wrap,
    presence,
    sanitize,
    parse_attributes,
    parse_xmldict,
)
from ..date_utils import (
    get_date_from_parts,
    get_date_from_crossref_parts,
    get_datetime_from_time,
)
from ..doi_utils import doi_as_url, get_doi_ra, crossref_xml_api_url, normalize_doi
from ..constants import (
    Commonmeta,
    CrossrefXml,
    CR_TO_DC_TRANSLATIONS,
    CR_TO_SO_TRANSLATIONS,
    CR_TO_CP_TRANSLATIONS,
    CR_TO_BIB_TRANSLATIONS,
    CR_TO_RIS_TRANSLATIONS,
    CROSSREF_CONTAINER_TYPES,
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

    # remove namespaces from xml
    namespaces = {
        "http://www.crossref.org/qrschema/3.0": None,
        "http://www.crossref.org/xschema/1.0": None,
        "http://www.crossref.org/xschema/1.1": None,
        "http://www.crossref.org/AccessIndicators.xsd": None,
        "http://www.crossref.org/fundref.xsd": None,
        "http://www.ncbi.nlm.nih.gov/JATS1": None,
    }
    data = xmltodict.parse(
        response.text, process_namespaces=True, namespaces=namespaces
    )
    # workaround for eval, used to clean up xmltodict output
    null = None
    data = eval(json.dumps(data))
    # remove namespaces from dict
    # data = {k:v for k,v in data.items() if k != "@xmlns"}

    return data


def read_crossref_xml(data: CrossrefXml, **kwargs) -> Commonmeta:
    """read_crossref_xml"""
    if data is None:
        return {"state": "not_found"}
    meta = py_.get(
        data, "crossref_result.query_result.body.query.doi_record.crossref", {}
    )

    # query contains information from outside metadata schema, e.g. publisher name
    query = py_.get(data, "crossref_result.query_result.body.query", {})

    # read_options = ActiveSupport::HashWithIndifferentAccess.
    # new(options.except(:doi, :id, :url,
    # :sandbox, :validate, :ra))
    read_options = kwargs or {}

    publisher = next(
        (
            i
            for i in wrap(query.get("crm-item", None))
            if i.get("@name", None) == "publisher-name"
        ),
        {},
    ).get("#text", None)

    # fetch metadata depending of Crossref type
    if py_.get(meta, "journal.journal_article", None):
        bibmeta = py_.get(meta, "journal.journal_article", {})
        resource_type = "JournalArticle"
    elif py_.get(meta, "journal.journal_issue", None):
        bibmeta = py_.get(meta, "journal.journal_issue", {})
        resource_type = "JournalIssue"
    elif py_.get(meta, "journal", None):
        bibmeta = py_.get(meta, "journal", {})
        resource_type = "Journal"
    elif py_.get(meta, "posted_content", None):
        bibmeta = meta.get("posted_content", {})
        if publisher is None:
            publisher = py_.get(bibmeta, "institution.institution_name", None)
        resource_type = "PostedContent"
    elif py_.get(meta, "book.content_item"):
        bibmeta = py_.get(meta, "book.content_item")
        resource_type = "BookChapter"
    elif py_.get(meta, "book.book_series_metadata"):
        bibmeta = py_.get(meta, "book.book_series_metadata")
        resource_type = "BookSeries"
    elif py_.get(meta, "book.book_set_metadata"):
        bibmeta = py_.get(meta, "book.book_set_metadata")
        resource_type = "BookSet"
    elif py_.get(meta, "book.book_metadata"):
        bibmeta = py_.get(meta, "book.book_metadata")
        resource_type = "Book"
    elif py_.get(meta, "conference", None):
        bibmeta = py_.get(meta, "conference.conference_paper", {})
        resource_type = "ConferencePaper"
    elif py_.get(meta, "sa_component", None):
        bibmeta = py_.get(meta, "sa_component.component_list.component", {})
        resource_type = "Component"
    elif py_.get(meta, "database", None):
        bibmeta = py_.get(meta, "database.dataset", {})
        resource_type = "Dataset"
    elif py_.get(meta, "report_paper", None):
        bibmeta = py_.get(meta, "report_paper.report_paper_metadata", {})
        resource_type = "Report"
    elif py_.get(meta, "peer_review", None):
        bibmeta = py_.get(meta, "peer_review", {})
        resource_type = "PeerReview"
    elif py_.get(meta, "dissertation", None):
        bibmeta = py_.get(meta, "dissertation", {})
        resource_type = "Dissertation"
    else:
        bibmeta = {}
        resource_type = ""

    pid = normalize_doi(
        kwargs.get("doi", None)
        or kwargs.get("pid", None)
        or py_.get(bibmeta, "doi_data.doi")
    )
    if pid:
        doi = doi_from_url(pid)
    else:
        doi = None

    url = parse_xmldict(
        py_.get(bibmeta, "doi_data.resource"), ignored_attributes="@content_version"
    )
    url = normalize_url(url)

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

    titles = crossref_titles(bibmeta)

    date_created = next(
        (
            i
            for i in wrap(query.get("crm-item", None))
            if i.get("@name", None) == "created"
        ),
        {},
    ).get("#text", None)
    date_registered = next(
        (
            i
            for i in wrap(query.get("crm-item", None))
            if i.get("@name", None) == "deposit-timestamp"
        ),
        {},
    )
    date_registered = get_datetime_from_time(date_registered.get("#text", None))
    date_issued = get_date_from_crossref_parts(bibmeta.get("publication_date", {}))
    date_reviewed = get_date_from_crossref_parts(bibmeta.get("review_date", {}))
    date_published = date_issued or date_reviewed or date_created

    # convert to date, as timestamp is fluctuating (servers in different timezones)
    date_published = date_published[:10] if date_published else None

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

    descriptions = crossref_description(bibmeta)
    program = py_.get(bibmeta, "program") or py_.get(
        bibmeta, "crossmark.custom_metadata.program"
    )
    funding = (
        py_.get(bibmeta, "program.assertion")
        or py_.get(bibmeta, "program.0.assertion")
        or py_.get(bibmeta, "crossmark.custom_metadata.program.assertion")
        or py_.get(bibmeta, "crossmark.custom_metadata.program.0.assertion")
    )
    funding_references = crossref_funding(wrap(funding))

    rights_list = (
        py_.get(bibmeta, "program.license_ref")
        or py_.get(bibmeta, "crossmark.custom_metadata.program.license_ref")
        or py_.get(bibmeta, "crossmark.custom_metadata.program.1.license_ref")
    )
    rights = crossref_rights(wrap(rights_list))

    # By using book_metadata, we can account for where resource_type is `BookChapter` and not assume its a whole book
    # if book_metadata:
    #     #   identifiers = crossref_alternate_identifiers(book_metadata)
    #     container = compact(
    #         {
    #             "type": "Book",
    #             "title": py_.get(book_metadata, "titles.title"),
    #             "firstPage": py_.get(bibmeta, "pages.first_page"),
    #             "lastPage": py_.get(bibmeta, "pages.last_page"),
    #             #'identifiers' => identifiers
    #         }
    #     )

    # elif book_series_metadata.get("series_metadata", None):
    #     issn = normalize_issn(
    #         py_.get(book_series_metadata, "series_metadata.issn.0.#text")
    #     )
    #     container = compact(
    #         {
    #             "type": "Book Series",
    #             "identifier": issn,
    #             "identifierType": "ISSN" if issn else None,
    #             "title": py_.get(book_series_metadata, "series_metadata.titles.title"),
    #             "volume": bibmeta.get("volume", None),
    #         }
    #     )
    # else:
    #     container = None
    container = crossref_container(meta, resource_type=resource_type)
    references = [
        crossref_reference(i) for i in wrap(py_.get(bibmeta, "citation_list.citation"))
    ]
    language = py_.get(meta, "journal.journal_metadata.@language")
    agency = bibmeta.get("@reg-agency", None) or get_doi_ra(pid)
    state = "findable" if meta or read_options else "not_found"

    return {
        # required properties
        "pid": pid,
        "doi": doi,
        "url": url,
        "creators": wrap(crossref_people(bibmeta, "author")),
        "titles": presence(titles),
        "types": types,
        "publisher": publisher,
        "publication_year": publication_year,
        # recommended and optional properties
        "subjects": presence(None),
        "contributors": crossref_people(bibmeta, "editor"),
        "dates": dates,
        "language": language,
        "alternate_identifiers": None,
        "sizes": None,
        "formats": None,
        "version": None,
        "rights": presence(rights),
        "descriptions": presence(descriptions),
        "geo_locations": None,
        "funding_references": presence(funding_references),
        "references": references,
        # other properties
        "date_created": None,
        "date_registered": None,
        "date_published": None,
        "date_updated": None,
        "content_url": presence(meta.get("contentUrl", None)),
        "container": presence(container),
        "agency": agency.capitalize() if agency else None,
        "state": state,
        "schema_version": None,
    } | read_options


def crossref_titles(bibmeta):
    """Title information from Crossref metadata."""

    def format_element(element):
        """Format element"""
        if element is None or (
            element.get("title", None) is None
            and element.get("original_language_title", None) is None
        ):
            return None
        if isinstance(element.get("title", None), str):
            return {"title": sanitize(element.get("title", ""))}
        if element.get("original_language_title", None):
            return {
                "title": sanitize(py_.get(element, "original_language_title.#text")),
                "lang": py_.get(element, "original_language_title.language"),
            }

    return [format_element(i) for i in wrap(bibmeta.get("titles", None))]


def crossref_description(bibmeta):
    """Description information from Crossref metadata."""

    def format_abstract(element):
        """Format abstract"""
        if isinstance(element.get("p", None), list):
            element["p"] = element["p"][0]
        if isinstance(element.get("p", None), dict):
            element["p"] = element["p"]["#text"]
        description_type = (
            "Abstract" if element.get("@abstract-type", None) == "abstract" else "Other"
        )
        return compact(
            {
                "descriptionType": description_type,
                "description": sanitize(
                    parse_attributes(element, content="p", first=True)
                ),
            }
        )

    return [format_abstract(i) for i in wrap(bibmeta.get("abstract", None))]


def crossref_people(bibmeta, contributor_role="author"):
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
            orcid = parse_xmldict(
                element.get("ORCID"), ignored_attributes="@authenticated"
            )
            element["nameIdentifiers"] = [
                {
                    "nameIdentifier": normalize_orcid(orcid),
                    "nameIdentifierScheme": "ORCID",
                    "schemeUri": "https://orcid.org",
                }
            ]
        element = py_.omit(
            element,
            "@contributor_role",
            "@sequence",
            "given_name",
            "surname",
            "ORCID",
            "@xmlns",
        )
        return compact(element)

    def format_organization(element):
        """Format organization"""
        return compact({element})

    person = py_.get(bibmeta, "contributors.person_name") or bibmeta.get(
        "person_name", None
    )
    organization = wrap(py_.get(bibmeta, "contributors.organization"))
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
    doi = parse_xmldict(reference.get("doi", None), ignored_attributes="@provider")
    unstructured = reference.get("unstructured_citation", None)
    if isinstance(unstructured, dict):
        url = unstructured.get("u", None)
        text = unstructured.get("font", None) or unstructured.get("#text", None)
    else:
        url = reference.get("url", None)
        text = reference.get("unstructured_citation", None)
    metadata = {
        "key": reference.get("@key", None),
        "doi": normalize_doi(doi) if doi else None,
        "url": normalize_url(url) if url else None,
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
        "unstructured": sanitize(text) if text and doi is None else None,
    }
    return compact(metadata)


def crossref_container(meta: dict, resource_type: str = "JournalArticle") -> dict:
    """Get container from Crossref"""
    container_type = CROSSREF_CONTAINER_TYPES.get(resource_type, None)
    issn = parse_xmldict(
        next(
            (
                i
                for i in wrap(
                    py_.get(meta, f"{container_type}.{container_type}_metadata.issn")
                )
                + wrap(
                    py_.get(
                        meta,
                        f"{container_type}.{container_type}_series_metadata.series_metadata.issn",
                    )
                )
                if i.get("@media_type", None) == "electronic"
            ),
            {},
        ),
        ignored_attributes=["@media_type", "@xmlns"],
    ) or parse_xmldict(
        next(
            (
                i
                for i in wrap(
                    py_.get(meta, f"{container_type}.{container_type}_metadata.issn")
                )
                + wrap(
                    py_.get(
                        meta,
                        f"{container_type}.{container_type}_series_metadata.series_metadata.issn",
                    )
                )
                if i.get("@media_type", None) == "print"
            ),
            {},
        ),
        ignored_attributes=["@media_type", "@xmlns"],
    )
    issn = normalize_issn(issn) if issn else None
    container_title = (
        py_.get(meta, f"{container_type}.{container_type}_metadata.full_title")
        or py_.get(meta, f"{container_type}.{container_type}_metadata.titles.title")
        or py_.get(
            meta,
            f"{container_type}.{container_type}_series_metadata.series_metadata.titles.title",
        )
    )
    volume = py_.get(
        meta,
        f"{container_type}.{container_type}_issue.{container_type}_volume.volume",
    )
    issue = py_.get(meta, f"{container_type}.{container_type}_issue.issue")
    return compact(
        {
            "type": py_.pascal_case(container_type) if container_type else None,
            "identifier": issn,
            "identifierType": "ISSN" if issn else None,
            "title": container_title,
            "volume": volume,
            "issue": issue,
            "firstPage": py_.get(
                meta, f"{container_type}.{container_type}_article.pages.first_page"
            )
            or py_.get(meta, f"{container_type}.content_item.pages.first_page"),
            "lastPage": py_.get(
                meta, f"{container_type}.{container_type}_article.pages.last_page"
            )
            or py_.get(meta, f"{container_type}.content_item.pages.last_page"),
        }
    )


def crossref_funding(funding_references: list) -> list:
    """Get funding references from Crossref"""
    formatted_funding_references = []
    for funding in funding_references:
        funding_dict = parse_xmldict(funding, ignored_attributes=["@xmlns"])
        if isinstance(funding_dict, dict) and isinstance(
            funding_dict.get("fundgroup", None), list
        ):
            path = "fundgroup.0"
        else:
            path = "fundgroup"
        funder_name = py_.get(funding_dict, f"{path}.funder_name")
        funder_identifier = py_.get(funding_dict, f"{path}.funder_identifier")
        if funder_identifier and funder_identifier.startswith("5011"):
            funder_identifier = doi_as_url("10.13039/" + funder_identifier)
        funding_reference = compact(
            {
                "funderName": funder_name,
                "funderIdentifier": normalize_doi(funder_identifier)
                if funder_identifier
                else None,
                "funderIdentifierType": "Crossref Funder ID"
                if funder_identifier
                else None,
            }
        )
        for award in wrap(py_.get(funding_dict, "fundgroup")):
            if award.get("award_number", None):
                fund_ref = funding_reference.copy()
                fund_ref["awardNumber"] = award.get("award_number")
                formatted_funding_references.append(fund_ref)
        if funding_reference != {} and len(wrap(py_.get(funding_dict, "fundgroup"))) == 1:
            formatted_funding_references.append(funding_reference)
             
    return formatted_funding_references


def crossref_rights(rights_list: list) -> list:
    """Get rights from Crossref"""

    def map_element(element):
        """Format element"""
        rights_uri = parse_xmldict(
            element, ignored_attributes=["@applies_to", "@start_date", "@end_date"]
        )
        rights_uri = normalize_cc_url(rights_uri)
        return dict_to_spdx({"rightsUri": rights_uri})

    # return only the first license found
    return wrap(next((map_element(i) for i in rights_list), None))
