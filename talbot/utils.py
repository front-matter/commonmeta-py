"""Utils module for Talbot."""
import os
import json
import re
from typing import Optional, Union
from urllib.parse import urlparse
from pydash import py_

from .base_utils import wrap, unwrap, compact, sanitize
from .doi_utils import normalize_doi, doi_from_url, get_doi_ra, validate_doi, crossref_api_url, datacite_api_url
from .constants import DC_TO_SO_TRANSLATIONS, SO_TO_DC_TRANSLATIONS

NORMALIZED_LICENSES = {
    "https://creativecommons.org/licenses/by/1.0": "https://creativecommons.org/licenses/by/1.0/legalcode",
    "https://creativecommons.org/licenses/by/2.0": "https://creativecommons.org/licenses/by/2.0/legalcode",
    "https://creativecommons.org/licenses/by/2.5": "https://creativecommons.org/licenses/by/2.5/legalcode",
    "https://creativecommons.org/licenses/by/3.0": "https://creativecommons.org/licenses/by/3.0/legalcode",
    "https://creativecommons.org/licenses/by/3.0/us": "https://creativecommons.org/licenses/by/3.0/legalcode",
    "https://creativecommons.org/licenses/by/4.0": "https://creativecommons.org/licenses/by/4.0/legalcode",
    "https://creativecommons.org/licenses/by-nc/1.0": "https://creativecommons.org/licenses/by-nc/1.0/legalcode",
    "https://creativecommons.org/licenses/by-nc/2.0": "https://creativecommons.org/licenses/by-nc/2.0/legalcode",
    "https://creativecommons.org/licenses/by-nc/2.5": "https://creativecommons.org/licenses/by-nc/2.5/legalcode",
    "https://creativecommons.org/licenses/by-nc/3.0": "https://creativecommons.org/licenses/by-nc/3.0/legalcode",
    "https://creativecommons.org/licenses/by-nc/4.0": "https://creativecommons.org/licenses/by-nc/4.0/legalcode",
    "https://creativecommons.org/licenses/by-nd-nc/1.0": "https://creativecommons.org/licenses/by-nd-nc/1.0/legalcode",
    "https://creativecommons.org/licenses/by-nd-nc/2.0": "https://creativecommons.org/licenses/by-nd-nc/2.0/legalcode",
    "https://creativecommons.org/licenses/by-nd-nc/2.5": "https://creativecommons.org/licenses/by-nd-nc/2.5/legalcode",
    "https://creativecommons.org/licenses/by-nd-nc/3.0": "https://creativecommons.org/licenses/by-nd-nc/3.0/legalcode",
    "https://creativecommons.org/licenses/by-nd-nc/4.0": "https://creativecommons.org/licenses/by-nd-nc/4.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-sa/1.0": "https://creativecommons.org/licenses/by-nc-sa/1.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-sa/2.0": "https://creativecommons.org/licenses/by-nc-sa/2.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-sa/2.5": "https://creativecommons.org/licenses/by-nc-sa/2.5/legalcode",
    "https://creativecommons.org/licenses/by-nc-sa/3.0": "https://creativecommons.org/licenses/by-nc-sa/3.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-sa/4.0": "https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode",
    "https://creativecommons.org/licenses/by-nd/1.0": "https://creativecommons.org/licenses/by-nd/1.0/legalcode",
    "https://creativecommons.org/licenses/by-nd/2.0": "https://creativecommons.org/licenses/by-nd/2.0/legalcode",
    "https://creativecommons.org/licenses/by-nd/2.5": "https://creativecommons.org/licenses/by-nd/2.5/legalcode",
    "https://creativecommons.org/licenses/by-nd/3.0": "https://creativecommons.org/licenses/by-nd/3.0/legalcode",
    "https://creativecommons.org/licenses/by-nd/4.0": "https://creativecommons.org/licenses/by-nd/2.0/legalcode",
    "https://creativecommons.org/licenses/by-sa/1.0": "https://creativecommons.org/licenses/by-sa/1.0/legalcode",
    "https://creativecommons.org/licenses/by-sa/2.0": "https://creativecommons.org/licenses/by-sa/2.0/legalcode",
    "https://creativecommons.org/licenses/by-sa/2.5": "https://creativecommons.org/licenses/by-sa/2.5/legalcode",
    "https://creativecommons.org/licenses/by-sa/3.0": "https://creativecommons.org/licenses/by-sa/3.0/legalcode",
    "https://creativecommons.org/licenses/by-sa/4.0": "https://creativecommons.org/licenses/by-sa/4.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-nd/1.0": "https://creativecommons.org/licenses/by-nc-nd/1.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-nd/2.0": "https://creativecommons.org/licenses/by-nc-nd/2.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-nd/2.5": "https://creativecommons.org/licenses/by-nc-nd/2.5/legalcode",
    "https://creativecommons.org/licenses/by-nc-nd/3.0": "https://creativecommons.org/licenses/by-nc-nd/3.0/legalcode",
    "https://creativecommons.org/licenses/by-nc-nd/4.0": "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode",
    "https://creativecommons.org/licenses/publicdomain": "https://creativecommons.org/licenses/publicdomain/",
    "https://creativecommons.org/publicdomain/zero/1.0": "https://creativecommons.org/publicdomain/zero/1.0/legalcode",
}

UNKNOWN_INFORMATION = {
    ":unac": "temporarily inaccessible",
    ":unal": "unallowed, suppressed intentionally",
    ":unap": "not applicable, makes no sense",
    ":unas": "value unassigned (e.g., Untitled)",
    ":unav": "value unavailable, possibly unknown",
    ":unkn": "known to be unknown (e.g., Anonymous, Inconnue)",
    ":none": "never had a value, never will",
    ":null": "explicitly and meaningfully empty",
    ":tba": "to be assigned or announced later",
    ":etal": "too numerous to list (et alia)",
}

HTTP_SCHEME = "http://"
HTTPS_SCHEME = "https://"


def normalize_id(pid: Optional[str], **kwargs) -> Optional[str]:
    """Check for valid DOI or HTTP(S) URL"""
    if pid is None:
        return None

    # check if pid is a bytes object
    if isinstance(pid, (bytes, bytearray)):
        pid = pid.decode()

    # check for valid DOI
    doi = normalize_doi(pid, **kwargs)
    if doi is not None:
        return doi

    # check for valid HTTP uri and ensure https
    uri = urlparse(pid)
    if not uri.netloc or uri.scheme not in ["http", "https"]:
        return None
    if uri.scheme == "http":
        pid = pid.replace(HTTP_SCHEME, HTTPS_SCHEME)

    # make pid lowercase and remove trailing slash
    pid = pid.lower()
    if pid.endswith("/"):
        pid = pid.strip("/")

    return pid


def normalize_ids(ids=None, relation_type=None):
    """Normalize identifiers"""
    formatted_ids = []
    for idx in wrap(ids):
        if idx.get("@id", None) is not None:
            idn = normalize_id(idx["@id"])
            related_identifier_type = "DOI" if doi_from_url(
                idn) is not None else "URL"
            idn = doi_from_url(idn) or idn
            type_ = (
                idx.get("@type")
                if isinstance(idx.get("@type", None), str)
                else wrap(idx.get("@type", None))[0]
            )
            formatted_ids.append(
                compact(
                    {
                        "relatedIdentifier": idn,
                        "relationType": relation_type,
                        "relatedIdentifierType": related_identifier_type,
                        "resourceTypeGeneral": SO_TO_DC_TRANSLATIONS.get(type_, None),
                    }
                )
            )
    return formatted_ids


def normalize_url(url: Optional[str], secure=False) -> Optional[str]:
    """Normalize URL"""
    if url is None or not isinstance(url, str):
        return None
    if url.endswith("/"):
        url = url.strip("/")
    if secure is True and url.startswith(HTTP_SCHEME):
        url = url.replace(HTTP_SCHEME, HTTPS_SCHEME)
    return url.lower()


def normalize_cc_url(url: Optional[str]):
    """Normalize Creative Commons URL"""
    if url is None or not isinstance(url, str):
        return None
    url = normalize_url(url, secure=True)
    return NORMALIZED_LICENSES.get(url, url)


def normalize_orcid(orcid: Optional[str]) -> Optional[str]:
    """Normalize ORCID"""
    if orcid is None or not isinstance(orcid, str):
        return None
    orcid = validate_orcid(orcid)
    if orcid is None:
        return None
    return "https://orcid.org/" + orcid


def validate_orcid(orcid: Optional[str]) -> Optional[str]:
    """Validate ORCID"""
    if orcid is None or not isinstance(orcid, str):
        return None
    match = re.search(
        r"\A(?:(?:http|https)://(?:(?:www|sandbox)?\.)?orcid\.org/)?(\d{4}[ -]\d{4}[ -]\d{4}[ -]\d{3}[0-9X]+)\Z",
        orcid,
    )
    if match is None:
        return None
    orcid = match.group(1).replace(" ", "-")
    return orcid


def dict_to_spdx(dct: dict) -> dict:
    """Convert a dict to SPDX"""
    dct.update({"rightsUri": normalize_cc_url(dct.get("rightsUri", None))})
    file_path = os.path.join(os.path.dirname(
        __file__), "resources/spdx/licenses.json")
    with open(file_path, encoding="utf-8") as json_file:
        spdx = json.load(json_file).get("licenses")
    license_ = next(
        (
            l
            for l in spdx
            if l["licenseId"].lower() == dct.get("rightsIdentifier", None)
            or l["seeAlso"][0] == dct.get("rightsUri", None)
        ),
        None,
    )
    if license_ is None:
        return dct
    #   license = spdx.find do |l|
    #     l['licenseId'].casecmp?(hsh['rightsIdentifier']) || l['seeAlso'].first == normalize_cc_url(hsh['rightsUri']) || l['name'] == hsh['rights'] || l['seeAlso'].first == normalize_cc_url(hsh['rights'])
    #   end
    return compact(
        {
            "rights": license_["name"],
            "rightsUri": license_["seeAlso"][0],
            "rightsIdentifier": license_["licenseId"].lower(),
            "rightsIdentifierScheme": "SPDX",
            "schemeUri": "https://spdx.org/licenses/",
            "lang": dct.get("lang", None),
        }
    )

    #   else
    #     {
    #       'rights': hsh['__content__'] || hsh['rights'],
    #       'rightsUri': hsh['rightsUri'] || hsh['rightsUri'],
    #       'rightsIdentifier': hsh['rightsIdentifier'].present? ? hsh['rightsIdentifier'].downcase : None,
    #       'rightsIdentifierScheme': hsh['rightsIdentifierScheme'],
    #       'schemeUri': hsh['schemeUri'],
    #       'lang': hsh['lang']
    #     }.compact
    #   end
    # end


def from_citeproc(element: Optional[Union[dict, list]]) -> list:
    """Convert a citeproc element to CSL"""
    formatted_element = []
    for elem in wrap(element):
        if elem.get("literal", None) is not None:
            elem["@type"] = "Organization"
            elem["name"] = elem["literal"]
        elif elem.get("name", None) is not None:
            elem["@type"] = "Organization"
            elem["name"] = elem.get("name")
        else:
            elem["@type"] = "Person"
            elem["name"] = " ".join(
                [elem.get("given", None), elem.get("family", None)]
            )
        elem["givenName"] = elem.get("given", None)
        elem["familyName"] = elem.get("family", None)
        elem["affiliation"] = elem.get("affiliation", None)
        for key in ["literal", "given", "family", "literal", "sequence"]:
            if key in elem:
                del elem[key]
        formatted_element.append(compact(elem))
    return formatted_element


def to_citeproc(element: Optional[Union[dict, list]]) -> list:
    """Convert a CSL element to citeproc"""
    formatted_element = []
    for elem in wrap(element):
        ele = {}
        ele["family"] = elem.get("familyName", None)
        ele["given"] = elem.get("givenName", None)
        ele["literal"] = (
            elem.get("name", None) if elem.get(
                "familyName", None) is None else None
        )
        formatted_element.append(compact(ele))
    return formatted_element


def to_ris(element: Optional[Union[dict, list]]) -> list:
    """Convert a CSL element to RIS"""
    formatted_element = []
    for elem in wrap(element):
        ele = ''
        if elem.get("familyName", None) is not None:
            ele = ", ".join([elem["familyName"], elem.get("givenName", None)])
        else:
            ele = elem.get('name', None)
        formatted_element.append(ele)
    return formatted_element


def to_schema_org(element: Optional[dict]) -> Optional[dict]:
    """Convert a metadata element to Schema.org"""
    if not isinstance(element, dict):
        return None
    mapping = {"type": "@type", "id": "@id", "title": "name"}
    for key, value in mapping.items():
        if element.get(key, None) is not None:
            element[value] = element.pop(key)
    return element


def to_schema_org_creators(element):
    """Convert CSL creators to Schema.org creators"""
    formatted_element = []
    for elem in wrap(element):
        el = {}
        # el['affiliation'] = wrap(element['affiliation']).map do |a|
        #   if a.is_a?(String)
        #     name = a
        #     affiliation_identifier = nil
        #   else
        #     name = a['name']
        #     affiliation_identifier = a['affiliationIdentifier']
        #   end

        #   { '@type': 'Organization', '@id': affiliation_identifier, 'name': name }.compact
        # end.unwrap
        el["@type"] = elem["nameType"][0:-
                                       3] if elem.get("nameType", None) else None
        # el['@id']= vwrap(c['nameIdentifiers']).first.to_h.fetch('nameIdentifier', nil)
        el["name"] = (
            " ".join([elem["givenName"], elem["familyName"]])
            if elem["familyName"]
            else elem.get("name", None)
        )
        # c.except('nameIdentifiers', 'nameType').compact
        formatted_element.append(compact(el))
    return unwrap(formatted_element)


def to_schema_org_contributors(element):
    """Convert CSL contributors to Schema.org contributors"""
    formatted_element = []
    for elem in wrap(element):
        el = {}
        # c['affiliation'] = Array.wrap(c['affiliation']).map do |a|
        #   if a.is_a?(String)
        #     name = a
        #     affiliation_identifier = nil
        #   else
        #     name = a['name']
        #     affiliation_identifier = a['affiliationIdentifier']
        #   end

        #   { '@type': 'Organization', '@id': affiliation_identifier, 'name': name }.compact
        # end.unwrap
        el["@type"] = elem["nameType"][0:-
                                       3] if elem.get("nameType", None) else None
        # el['@id']=# vwrap(c['nameIdentifiers']).first.to_h.fetch('nameIdentifier', nil)
        el["name"] = (
            " ".join([elem["givenName"], elem["familyName"]])
            if elem["familyName"]
            else elem.get("name", None)
        )
        # c.except('nameIdentifiers', 'nameType').compact
        formatted_element.append(compact(el))
    return unwrap(formatted_element)


def to_schema_org_container(element: Optional[dict], **kwargs) -> Optional[dict]:
    """Convert CSL container to Schema.org container"""
    if element is None and kwargs.get("container_title", None) is None:
        return None
    if not isinstance(element, dict):
        return None

    return compact(
        {
            "@id": element.get("identifier", None),
            "@type": "DataCatalog"
            if kwargs.get("type", None) == "DataRepository"
            else "Periodical",
            "name": element.get("title", None) or kwargs.get("container_title", None),
        }
    )


def to_schema_org_identifiers(element):
    """Convert CSL identifiers to Schema.org identifiers"""
    formatted_element = []
    for elem in wrap(element):
        el = {}
        el["@type"] = "PropertyValue"
        el["propertyID"] = elem.get("identifierType", None)
        el["value"] = elem.get("identifier", None)
        formatted_element.append(compact(el))
    return unwrap(formatted_element)


def to_schema_org_relation(related_items=None, relation_type=None):
    """Convert related:items to Schema.org relations"""
    if related_items is None or relation_type is None:
        return None

    # consolidate different relation types
    if relation_type == "References":
        relation_type = ["References", "Cites"]
    else:
        relation_type = [relation_type]

    related_items = py_.filter(
        wrap(
            related_items), lambda ri: ri["relationType"] in relation_type
    )

    formatted_items = []
    for rel in related_items:
        if rel["relatedItemIdentifierType"] == "ISSN" and rel["relationType"] == "IsPartOf":
            formatted_items.append(
                compact({"@type": "Periodical",
                        "issn": rel["relatedItemIdentifier"]})
            )
        else:
            formatted_items.append(
                compact(
                    {
                        "@id": normalize_id(rel["relatedIdentifier"]),
                        "@type": DC_TO_SO_TRANSLATIONS.get(
                            rel["resourceTypeGeneral"], "CreativeWork"
                        ),
                    }
                )
            )
    return unwrap(formatted_items)


def find_from_format(pid=None, string=None, ext=None, filename=None):
    """Find reader from format"""
    if pid is not None:
        return find_from_format_by_id(pid)
    if string is not None and ext is not None:
        return find_from_format_by_ext(string, ext=ext)
    if string is not None:
        return find_from_format_by_string(string)
    if filename is not None:
        return find_from_format_by_filename(filename)
    return "datacite"


def find_from_format_by_id(pid: str) -> Optional[str]:
    """Find reader from format by id"""
    doi = validate_doi(pid)
    if doi and (registration_agency := get_doi_ra(doi)) is not None:
        return registration_agency.lower()
    # if (
    #     re.match(r"\A(http|https):/(/)?github\.com/(.+)/codemeta.json\Z", id)
    #     is not None
    # ):
    #     return "codemeta"
    # if re.match(r"\A(http|https):/(/)?github\.com/(.+)/CITATION.cff\Z", id) is not None:
    #     return "cff"
    # if re.match(r"\A(http|https):/(/)?github\.com/(.+)\Z", id) is not None:
    #     return "cff"
    return "schema_org"


def find_from_format_by_ext(string, ext=None):
    """Find reader from format by ext"""


def find_from_format_by_string(string):
    """Find reader from format by string"""
    if string is None:
        return None
    dictionary = json.loads(string)
    print(dictionary)
    if dictionary.get("@context", None) == "http://schema.org":
        return "schema_org"
    if dictionary.get("@context", None) in ['https://raw.githubusercontent.com/codemeta/codemeta/master/codemeta.jsonld']:
        return "codemeta"
    if dictionary.get("schemaVersion", '').startswith("http://datacite.org/schema/kernel"):
        return "datacite"
    if dictionary.get("source", None) == "Crossref":
        return "crossref"
    if py_.get(dictionary, "issued.date-parts") is not None:
        return "citeproc"

    # no format found
    return None

    # if Maremma.from_xml(string).to_h.dig('crossref_result', 'query_result', 'body', 'query',
    #                                        'doi_record', 'crossref').present?
    #     'crossref_xml'
    #   elsif Nokogiri::XML(string, None, 'UTF-8', &:noblanks).collect_namespaces.find do |_k, v|
    #           v.start_with?('http://datacite.org/schema/kernel')
    # #         end
    #     'datacite_xml'

    #   elsif YAML.load(string).to_h.fetch('cff-version', None).present?
    #     'cff'


def find_from_format_by_filename(filename):
    """Find reader from format by filename"""
    # if filename == "package.json":
    #   return "npm"
    if filename == "CITATION.cff":
        return "cff"
    return None


def from_schema_org(element):
    """Convert schema.org to DataCite"""
    if element is None:
        return None
    element["type"] = element.get("@type", None)
    element["id"] = element.get("@id", None)
    return compact(py_.omit(element, ["@type", "@id"]))


def from_schema_org_creators(element):
    """Convert schema.org creators to DataCite"""
    formatted_element = []
    for elem in wrap(element):
        if isinstance(elem.get("affiliation", None), str):
            elem["affiliation"] = {"name": elem["affiliation"]}
            affiliation_identifier_scheme = None
            scheme_uri = None
        elif py_.get(elem, "affiliation.@id", "").startswith("https://ror.org"):
            affiliation_identifier_scheme = "ROR"
            scheme_uri = "https://ror.org/"
        elif elem.get("affiliation.@id", "").startswith("https://isni.org"):
            affiliation_identifier_scheme = "ISNI"
            scheme_uri = "https://isni.org/isni/"
        else:
            affiliation_identifier_scheme = None
            scheme_uri = None

        # alternatively find the nameIdentifier in the identifer attribute
        # if elem.get('identifier', None) is not None and elem.get('@id', None) is not None:
        #    elem['@id'] = elem['identifier']
        # alternatively find the nameIdentifier in the sameAs attribute
        # elem['@id'] = py_.find(wrap(elem.get('sameAs', None)), lambda x: x == 'orcid.org')

        if elem.get("@id", None) is not None:
            # elem['@id'] = normalize_orcid(elem.get('@id'))
            # identifier_scheme = "ORCID"
            scheme_uri = "https://orcid.org/"
        elem["nameIdentifier"] = [
            {
                "__content__": elem.get("@id", None),
                "nameIdentifierScheme": "ORCID",
                "schemeUri": "https://orcid.org",
            }
        ]

        if isinstance(elem.get("@type", None), list):
            elem["@type"] = py_.find(
                elem["@type"], lambda x: x in ["Person", "Organization"]
            )
        elem["creatorName"] = compact(
            {
                "nameType": elem["@type"].title() + "al"
                if elem.get("@type", None) is not None
                else None,
                "__content__": elem["name"],
            }
        )
        elem["affiliation"] = compact(
            {
                "__content__": py_.get(elem, "affiliation.name"),
                "affiliationIdentifier": py_.get(elem, "affiliation.@id"),
                "affiliationIdentifierScheme": affiliation_identifier_scheme,
                "schemeUri": scheme_uri,
            }
        )
        formatted_element.append(py_.omit(elem, "@id", "@type", "name"))
    return formatted_element


def from_schema_org_contributors(element):
    """Parse contributors from schema.org"""
    formatted_element = []
    for elem in wrap(element):
        if isinstance(elem.get("affiliation", None), str):
            elem["affiliation"] = {"name": elem["affiliation"]}
            affiliation_identifier_scheme = None
            scheme_uri = None
        elif py_.get(elem, "affiliation.@id", "").startswith("https://ror.org"):
            affiliation_identifier_scheme = "ROR"
            scheme_uri = "https://ror.org/"
        elif py_.get(elem, "affiliation.@id", "").startswith("https://isni.org"):
            affiliation_identifier_scheme = "ISNI"
            scheme_uri = "https://isni.org/isni/"
        else:
            affiliation_identifier_scheme = None
            scheme_uri = None

        if normalize_orcid(elem.get("@id", None)) is not None:
            elem["nameIdentifier"] = [
                {
                    "__content__": elem["@id"],
                    "nameIdentifierScheme": "ORCID",
                    "schemeUri": "https://orcid.org",
                }
            ]
        elem["contributorName"] = compact(
            {
                "nameType": elem["@type"].titleize + "al"
                if elem.get("@type", None) is not None
                else None,
                "__content__": elem["name"],
            }
        )
        elem["affiliation"] = compact(
            {
                "__content__": py_.get(elem, "affiliation.name"),
                "affiliationIdentifier": py_.get(elem, "affiliation.@id"),
                "affiliationIdentifierScheme": affiliation_identifier_scheme,
                "schemeUri": scheme_uri,
            }
        )
        formatted_element.append(py_.omit(elem, "@id", "@type", "name"))
    return formatted_element


def pages_as_string(container: Optional[dict], page_range_separator="-") -> Optional[str]:
    """Parse pages for BibTeX"""
    if container is None:
        return None
    if container.get("firstPage", None) is None:
        return None
    if container.get("lastPage", None) is None:
        return container.get("firstPage", None)

    return page_range_separator.join(
        [container.get("firstPage"), container.get("lastPage", None)]
    )


def subjects_as_string(subjects):
    """convert subject list to string, e.g. for bibtex"""
    if subjects is None:
        return None

    keywords = []
    for subject in wrap(subjects):
        keywords.append(subject.get("subject", None))
    return ", ".join(keywords)


# def reverse():
#       return { 'citation': wrap(related_identifiers).select do |ri|
#                         ri['relationType'] == 'IsReferencedBy'
#                       end.map do |r|
#                         { '@id': normalize_doi(r['relatedIdentifier']),
#                           '@type': r['resourceTypeGeneral'] validate_orcid 'ScholarlyArticle',
#                           'identifier': r['relatedIdentifierType'] == 'DOI' ? nil : to_identifier(r) }.compact
#                       end.unwrap,
#         'isBasedOn': wrap(related_identifiers).select do |ri|
#                          ri['relationType'] == 'IsSupplementTo'
#                        end.map do |r|
#                          { '@id': normalize_doi(r['relatedIdentifier']),
#                            '@type': r['resourceTypeGeneral'] or 'ScholarlyArticle',
#                            'identifier': r['relatedIdentifierType'] == 'DOI' ? nil : to_identifier(r) }.compact
#                        end.unwrap }.compact


def name_to_fos(name: str) -> Optional[dict]:
    """Convert name to Fields of Science (OECD) subject"""
    #   # first find subject in Fields of Science (OECD)
    #   fos = JSON.load(File.read(File.expand_path('../../resources/oecd/fos-mappings.json',
    #                                              __dir__))).fetch('fosFields')

    #   subject = fos.find { |l| l['fosLabel'] == name || 'FOS: ' + l['fosLabel'] == name }

    #   if subject
    #     return [{
    #       'subject': sanitize(name).downcase
    #     },
    #             {
    #               'subject': 'FOS: ' + subject['fosLabel'],
    #               'subjectScheme': 'Fields of Science and Technology (FOS)',
    #               'schemeUri': 'http://www.oecd.org/science/inno/38235147.pdf'
    #             }]
    #   end

    #   # if not found, look in Fields of Research (Australian and New Zealand Standard Research Classification)
    #   # and map to Fields of Science. Add an extra entry for the latter
    #   fores = JSON.load(File.read(File.expand_path('../../resources/oecd/for-mappings.json',
    #                                                __dir__)))
    #   for_fields = fores.fetch('forFields')
    #   for_disciplines = fores.fetch('forDisciplines')

    #   subject = for_fields.find { |l| l['forLabel'] == name } ||
    #             for_disciplines.find { |l| l['forLabel'] == name }

    #   if subject
    #     [{
    #       'subject': sanitize(name).downcase
    #     },
    #      {
    #        'subject': 'FOS: ' + subject['fosLabel'],
    #        'subjectScheme': 'Fields of Science and Technology (FOS)',
    #        'schemeUri': 'http://www.oecd.org/science/inno/38235147.pdf'
    #      }]
    #   else
        
    return {"subject": name.lower()}
