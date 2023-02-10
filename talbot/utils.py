"""Utils module for Talbot."""
import os
import html
import json
import re
from urllib.parse import urlparse
import bleach
from pydash import py_

from .doi_utils import normalize_doi, doi_from_url, get_doi_ra, validate_doi
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


def wrap(item):
    """Turn None, dict, or list into list"""
    if item is None:
        return []
    if isinstance(item, list):
        return item
    return [item]


def unwrap(list):
    """Turn list into dict or None, depending on list size"""
    if len(list) == 0:
        return None
    if len(list) == 1:
        return list[0]
    return list


def presence(item):
    """Turn empty list, dict or str into None"""
    return None if item is None or len(item) == 0 else item


def compact(dict_or_list):
    """Remove None from dict or list"""
    if type(dict_or_list) in [None, str]:
        return dict_or_list
    if isinstance(dict_or_list, dict):
        return {k: v for k, v in dict_or_list.items() if v is not None}
    if isinstance(dict_or_list, list):
        arr = list(map(lambda x: compact(x), dict_or_list))
        return None if len(arr) == 0 else arr


def parse_attributes(element, **kwargs):
    """extract attributes from a string, dict or list"""
    content = kwargs.get("content", "__content__")

    if isinstance(element, str) and kwargs.get("content", None) is None:
        return html.unescape(element)
    if isinstance(element, dict):
        return element.get(html.unescape(content), None)
    if isinstance(element, list):
        arr = list(
            map(
                lambda x: x.get(html.unescape(content), None)
                if isinstance(x, dict)
                else x,
                element,
            )
        )
        arr = arr[0] if kwargs.get("first") else unwrap(arr)
        return arr


def normalize_id(pid, **kwargs):
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


def crossref_api_url(doi):
    """Return the Crossref API URL for a given DOI"""
    return "https://api.crossref.org/works/" + doi


def datacite_api_url(doi, **kwargs):
    """Return the DataCite API URL for a given DOI"""
    match = re.match(
        r"\A(?:(http|https):/(/)?handle\.stage\.datacite\.org)", doi, re.IGNORECASE
    )
    if match is not None or kwargs.get("sandbox", False):
        return f"https://api.stage.datacite.org/dois/{doi_from_url(doi)}?include=media,client"
    else:
        return f"https://api.datacite.org/dois/{doi_from_url(doi)}?include=media,client"


def normalize_url(url, secure=False):
    """Normalize URL"""
    if url is None:
        return None
    if url.endswith("/"):
        url = url.strip("/")
    if secure is True and url.startswith(HTTP_SCHEME):
        url = url.replace(HTTP_SCHEME, HTTPS_SCHEME)
    return url.lower()


def normalize_cc_url(url):
    """Normalize Creative Commons URL"""
    if url is None:
        return None
    url = normalize_url(url, secure=True)
    return NORMALIZED_LICENSES.get(url, url)


def normalize_orcid(orcid):
    """Normalize ORCID"""
    orcid = validate_orcid(orcid)
    if orcid is None:
        return None
    return "https://orcid.org/" + orcid


def validate_orcid(orcid):
    """Validate ORCID"""
    if orcid is None:
        return None
    match = re.search(
        r"\A(?:(?:http|https)://(?:(?:www|sandbox)?\.)?orcid\.org/)?(\d{4}[ -]\d{4}[ -]\d{4}[ -]\d{3}[0-9X]+)\Z",
        orcid,
    )
    if match is None:
        return None
    orcid = match.group(1).replace(" ", "-")
    return orcid


def dict_to_spdx(dict):
    """Convert a dict to SPDX"""
    dict.update({"rightsURI": normalize_cc_url(dict.get("rightsURI", None))})
    file_path = os.path.join(os.path.dirname(
        __file__), "resources/spdx/licenses.json")
    with open(file_path, encoding="utf-8") as json_file:
        spdx = json.load(json_file).get("licenses")
    license_ = next(
        (
            l
            for l in spdx
            if l["licenseId"].lower() == dict.get("rightsIdentifier", None)
            or l["seeAlso"][0] == dict.get("rightsURI", None)
        ),
        None,
    )
    if license_ is None:
        return dict
    #   license = spdx.find do |l|
    #     l['licenseId'].casecmp?(hsh['rightsIdentifier']) || l['seeAlso'].first == normalize_cc_url(hsh['rightsURI']) || l['name'] == hsh['rights'] || l['seeAlso'].first == normalize_cc_url(hsh['rights'])
    #   end
    return compact(
        {
            "rights": license_["name"],
            "rightsURI": license_["seeAlso"][0],
            "rightsIdentifier": license_["licenseId"].lower(),
            "rightsIdentifierScheme": "SPDX",
            "schemeUri": "https://spdx.org/licenses/",
            "lang": dict.get("lang", None),
        }
    )

    #   else
    #     {
    #       'rights': hsh['__content__'] || hsh['rights'],
    #       'rightsUri': hsh['rightsURI'] || hsh['rightsUri'],
    #       'rightsIdentifier': hsh['rightsIdentifier'].present? ? hsh['rightsIdentifier'].downcase : None,
    #       'rightsIdentifierScheme': hsh['rightsIdentifierScheme'],
    #       'schemeUri': hsh['schemeUri'],
    #       'lang': hsh['lang']
    #     }.compact
    #   end
    # end


def from_citeproc(element):
    """Convert a citeproc element to CSL"""
    formatted_element = []
    for elem in wrap(element):
        el = {}
        if elem.get("literal", None) is not None:
            el["@type"] = "Organization"
            el["name"] = elem["literal"]
        elif elem.get("name", None) is not None:
            el["@type"] = "Organization"
            el["name"] = elem.get("name")
        else:
            el["@type"] = "Person"
            el["name"] = " ".join(
                compact([elem.get("given", None), elem.get("family", None)])
            )
        el["givenName"] = elem.get("given", None)
        el["familyName"] = elem.get("family", None)
        el["affiliation"] = elem.get("affiliation", None)
        formatted_element.append(compact(el))
    return formatted_element


def to_citeproc(element):
    """Convert a CSL element to citeproc"""
    formatted_element = []
    for elem in wrap(element):
        el = {}
        el["family"] = elem.get("familyName", None)
        el["given"] = elem.get("givenName", None)
        el["literal"] = (
            elem.get("name", None) if elem.get(
                "familyName", None) is None else None
        )
        formatted_element.append(compact(el))
    return formatted_element


def to_ris(element):
    """Convert a CSL element to RIS"""
    formatted_element = []
    for elem in wrap(element):
        el = {}
        if elem.get("familyName", None) is not None:
            el = ", ".join([elem["familyName"], elem.get("givenName", None)])
        else:
            el = elem.get('name', None)
        formatted_element.append(compact(el))
    return formatted_element


def to_schema_org(element):
    """Convert a CSL element to Schema.org"""
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


def to_schema_org_container(element, **kwargs):
    """Convert CSL container to Schema.org container"""
    if element is None:
        return None
    if isinstance(element, dict) or kwargs.get("container_title", None) is None:
        return None

    return compact(
        {
            "@id": element.get("identifier", None),
            "@type": "DataCatalog"
            if kwargs.get("type", None) == "Dataset"
            else "Periodical",
            "name": element["title"] or kwargs.get("container_title", None),
        }
    )


def to_schema_org_identifiers(element, **kwargs):
    """Convert CSL identifiers to Schema.org identifiers"""
    formatted_element = []
    for elem in wrap(element):
        el = {}
        el["@type"] = "PropertyValue"
        el["propertyID"] = elem.get("identifierType", None)
        el["value"] = elem.get("identifier", None)
        formatted_element.append(compact(el))
    return unwrap(formatted_element)


def to_schema_org_relation(related_identifiers=None, relation_type=None):
    """Convert CSL related identifiers to Schema.org relations"""
    if related_identifiers is None or relation_type is None:
        return None

    # consolidate different relation types
    if relation_type == "References":
        relation_type = ["References", "Cites"]
    else:
        relation_type = [relation_type]

    related_identifiers = py_.filter(
        wrap(
            related_identifiers), lambda ri: ri["relationType"] in relation_type
    )

    formatted_identifiers = []
    for rel in related_identifiers:
        if rel["relatedIdentifierType"] == "ISSN" and rel["relationType"] == "IsPartOf":
            formatted_identifiers.append(
                compact({"@type": "Periodical",
                        "issn": rel["relatedIdentifier"]})
            )
        else:
            formatted_identifiers.append(
                compact(
                    {
                        "@id": normalize_id(rel["relatedIdentifier"]),
                        "@type": DC_TO_SO_TRANSLATIONS.get(
                            rel["resourceTypeGeneral"], "CreativeWork"
                        ),
                    }
                )
            )
    return unwrap(formatted_identifiers)


def find_from_format(id=None, string=None, ext=None, filename=None):
    """Find reader from format"""
    if id is not None:
        return find_from_format_by_id(id)
    if string is not None and ext is not None:
        return find_from_format_by_ext(string, ext=ext)
    if string is not None:
        return find_from_format_by_string(string)
    if filename is not None:
        return find_from_format_by_filename(filename)
    return "datacite"


def find_from_format_by_id(id):
    """Find reader from format by id"""
    doi = validate_doi(id)
    if doi and (ra := get_doi_ra(doi)) is not None:
        return ra.lower()
    if (
        re.match(
            r"\A(?:(http|https):/(/)?orcid\.org/)?(\d{4}-\d{4}-\d{4}-\d{3}[0-9X]+)\Z",
            id,
        )
        is not None
    ):
        return "orcid"
    if re.match(r"\A(http|https):/(/)?github\.com/(.+)/package.json\Z", id) is not None:
        return "npm"
    if (
        re.match(r"\A(http|https):/(/)?github\.com/(.+)/codemeta.json\Z", id)
        is not None
    ):
        return "codemeta"
    if re.match(r"\A(http|https):/(/)?github\.com/(.+)/CITATION.cff\Z", id) is not None:
        return "cff"
    if re.match(r"\A(http|https):/(/)?github\.com/(.+)\Z", id) is not None:
        return "cff"
    return "schema_org"


def find_from_format_by_ext(string, ext=None):
    """Find reader from format by ext"""


def find_from_format_by_string(string):
    """Find reader from format by string"""
    try:
        if json.loads(string).get("@context", None) == "http://schema.org":
            return "schema_org"
        if (
            json.loads(string)
            .get("schema-version", "")
            .beginswith("http://datacite.org/schema/kernel")
        ):
            return "datacite_json"
        if json.loads(string).get("source", None) == "Crossref":
            return "crossref_json"
        if py_.get(json.loads(string), "issued.date-parts", None) is not None:
            return "citeproc"
        if string.startswith("TY  - "):
            return "ris"
        return "datacite"
    except NameError:
        return "datacite"
    # if Maremma.from_xml(string).to_h.dig('crossref_result', 'query_result', 'body', 'query',
    #                                        'doi_record', 'crossref').present?
    #     'crossref'
    #   elsif Nokogiri::XML(string, None, 'UTF-8', &:noblanks).collect_namespaces.find do |_k, v|
    #           v.start_with?('http://datacite.org/schema/kernel')
    # #         end
    #     'datacite'
    #   elsif URI(Maremma.from_json(string).to_h.fetch('@context', '')).host == 'schema.org'
    #     'schema_org'
    #   elsif Maremma.from_json(string).to_h.dig('@context') == ('https://raw.githubusercontent.com/codemeta/codemeta/master/codemeta.jsonld')
    #     'codemeta'
    #   elsif Maremma.from_json(string).to_h.dig('schema-version').to_s.start_with?('http://datacite.org/schema/kernel')
    #     'datacite_json'
    #   elsif Maremma.from_json(string).to_h.dig('source') == ('Crossref')
    #     'crossref_json'
    #   elsif Maremma.from_json(string).to_h.dig('types').present? && Maremma.from_json(string).to_h.dig('publication_year').present?
    #     'crosscite'
    #   elsif Maremma.from_json(string).to_h.dig('issued', 'date-parts').present?
    #     'citeproc'

    #   elsif YAML.load(string).to_h.fetch('cff-version', None).present?
    #     'cff'


def find_from_format_by_filename(filename):
    """Find reader from format by filename"""
    if filename == "package.json":
        return "npm"
    if filename == "CITATION.cff":
        return "cff"
    return None


def camel_case(text):
    """Convert text to camel case"""
    if text is None:
        return None
    string = text.replace("-", " ").replace("_", " ")
    string = string.split()
    if len(text) == 0:
        return text
    return string[0] + "".join(i.capitalize() for i in string[1:])


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
                "__content__": py_.get(elem, "affiliation.name", None),
                "affiliationIdentifier": py_.get(elem, "affiliation.@id", None),
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
                "__content__": py_.get(elem, "affiliation.name", None),
                "affiliationIdentifier": py_.get(elem, "affiliation.@id", None),
                "affiliationIdentifierScheme": affiliation_identifier_scheme,
                "schemeUri": scheme_uri,
            }
        )
        formatted_element.append(py_.omit(elem, "@id", "@type", "name"))
    return formatted_element


def pages_as_string(container, page_range_separator="-"):
    """Parse pages for BibTeX"""
    if container is None:
        return None
    if container.get("firstPage", None) is None:
        return None
    if container.get("lastPage", None) is None:
        return container.get("firstPage", None)

    return page_range_separator.join(
        compact([container.get("firstPage"), container.get("lastPage", None)])
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


def name_to_fos(name):
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
    return [{"subject": name.lower()}]


def sanitize(text, **kwargs):
    """Sanitize text"""
    tags = kwargs.get("tags", None) or frozenset(
        {"b", "br", "code", "em", "i", "sub", "sup", "strong"}
    )
    content = kwargs.get("content", None) or "__content__"
    first = kwargs.get("first", True)
    strip = kwargs.get("strip", True)

    if isinstance(text, str):
        string = bleach.clean(text, tags=tags, strip=strip)
        # remove excessive internal whitespace
        return " ".join(re.split(r"\s+", string, flags=re.UNICODE))
        # return re.sub(r'\\s\\s+', ' ', string)
    if isinstance(text, dict):
        return sanitize(text.get(content, None))
    if isinstance(text, list):
        if len(text) == 0:
            return None

        lst = []
        for elem in text:
            lst.append(
                sanitize(elem.get(content, None)) if isinstance(
                    elem, dict) else sanitize(elem)
            )  # uniq
        return lst[0] if first else unwrap(lst)


def get_geolocation_point(geo_location):
    """Get geolocation point"""
    if geo_location is None or not isinstance(geo_location, dict):
        return None
    return {'geoLocationPoint': {"pointLongitude": py_.get(geo_location, "geo.longitude", None),
                                 "pointLatitude": py_.get(geo_location, "geo.latitude", None)}}


def get_geolocation_box(geo_location):
    """Get geolocation box"""
    if geo_location is None or not isinstance(geo_location, dict):
        return None
    return compact({"boxLongitude": py_.get(geo_location, "geo.longitude", None),
                    "boxLatitude": py_.get(geo_location, "geo.latitude", None),
                    "boxNorthBoundLatitude": py_.get(geo_location, "geo.north", None),
                    "boxSouthBoundLatitude": py_.get(geo_location, "geo.south", None),
                    "boxEastBoundLongitude": py_.get(geo_location, "geo.east", None),
                    "boxWestBoundLongitude": py_.get(geo_location, "geo.west", None)})
