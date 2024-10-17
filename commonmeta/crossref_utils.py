"""Crossref utils module for commonmeta-py"""

from lxml import etree
from typing import Optional
from datetime import datetime
from dateutil.parser import parse
import uuid
import pydash as py_
from furl import furl

from .constants import Commonmeta, ROR_TO_CROSSREF_FUNDER_ID_TRANSLATIONS
from .utils import wrap, compact, normalize_orcid, normalize_id, validate_url
from .doi_utils import doi_from_url, validate_doi


def generate_crossref_xml(metadata: Commonmeta) -> Optional[str]:
    """Generate Crossref XML. First checks for write errors (JSON schema validation)"""
    xml = crossref_root()
    head = etree.SubElement(xml, "head")
    # we use a uuid as batch_id
    etree.SubElement(head, "doi_batch_id").text = str(uuid.uuid4())
    etree.SubElement(head, "timestamp").text = datetime.now().strftime("%Y%m%d%H%M%S")
    depositor = etree.SubElement(head, "depositor")
    etree.SubElement(depositor, "depositor_name").text = metadata.depositor
    etree.SubElement(depositor, "email_address").text = metadata.email
    etree.SubElement(head, "registrant").text = metadata.registrant

    body = etree.SubElement(xml, "body")
    body = insert_crossref_work(metadata, body)
    return etree.tostring(
        xml,
        doctype='<?xml version="1.0" encoding="UTF-8"?>',
        pretty_print=True,
    )


def insert_crossref_work(metadata, xml):
    """Insert crossref work"""
    if metadata.type not in ["JournalArticle", "Article"]:
        return xml
    if doi_from_url(metadata.id) is None or metadata.url is None:
        return xml
    if metadata.type == "JournalArticle":
        xml = insert_journal(metadata, xml)
    elif metadata.type == "Article":
        xml = insert_posted_content(metadata, xml)


def insert_journal(metadata, xml):
    """Insert journal"""
    journal = etree.SubElement(xml, "journal")
    if metadata.language is not None:
        journal_metadata = etree.SubElement(
            journal, "journal_metadata", {"language": metadata.language[:2]}
        )
    else:
        journal_metadata = etree.SubElement(journal, "journal_metadata")
    if (
        metadata.container is not None
        and metadata.container.get("title", None) is not None
    ):
        etree.SubElement(journal_metadata, "full_title").text = metadata.container.get(
            "title"
        )
    journal_metadata = insert_group_title(metadata, journal_metadata)
    journal_article = etree.SubElement(
        journal, "journal_article", {"publication_type": "full_text"}
    )
    journal_article = insert_crossref_titles(metadata, journal_article)
    journal_article = insert_crossref_contributors(metadata, journal_article)
    journal_article = insert_crossref_publication_date(metadata, journal_article)
    journal_article = insert_crossref_abstract(metadata, journal_article)
    journal_article = insert_crossref_issn(metadata, journal_article)
    journal_article = insert_item_number(metadata, journal_article)
    journal_article = insert_funding_references(metadata, journal_article)
    journal_article = insert_crossref_access_indicators(metadata, journal_article)
    journal_article = insert_crossref_relations(metadata, journal_article)
    journal_article = insert_archive_locations(metadata, journal_article)
    journal_article = insert_doi_data(metadata, journal_article)
    journal_article = insert_citation_list(metadata, journal_article)

    return journal


def insert_posted_content(metadata, xml):
    """Insert posted content"""
    if metadata.language is not None:
        posted_content = etree.SubElement(
            xml, "posted_content", {"type": "other", "language": metadata.language[:2]}
        )
    else:
        posted_content = etree.SubElement(xml, "posted_content", {"type": "other"})

    posted_content = insert_group_title(metadata, posted_content)
    posted_content = insert_crossref_contributors(metadata, posted_content)
    posted_content = insert_crossref_titles(metadata, posted_content)
    posted_content = insert_posted_date(metadata, posted_content)
    posted_content = insert_institution(metadata, posted_content)
    posted_content = insert_item_number(metadata, posted_content)
    posted_content = insert_crossref_abstract(metadata, posted_content)
    posted_content = insert_funding_references(metadata, posted_content)
    posted_content = insert_crossref_access_indicators(metadata, posted_content)
    posted_content = insert_crossref_relations(metadata, posted_content)
    posted_content = insert_archive_locations(metadata, posted_content)
    posted_content = insert_doi_data(metadata, posted_content)
    posted_content = insert_citation_list(metadata, posted_content)

    return xml


def insert_group_title(metadata, xml):
    """Insert group title"""
    if metadata.subjects is None or len(metadata.subjects) == 0:
        return xml
    group_title = metadata.subjects[0].get("subject", None)
    # strip optional FOS (Field of Science) prefix
    if group_title.startswith("FOS: "):
        group_title = group_title[5:]
    etree.SubElement(xml, "group_title").text = group_title
    return xml


def insert_crossref_contributors(metadata, xml):
    """Insert crossref contributors"""
    if metadata.contributors is None or len(metadata.contributors) == 0:
        return xml
    contributors = etree.SubElement(xml, "contributors")
    con = [
        c
        for c in metadata.contributors
        if c.get("contributorRoles", None) == ["Author"]
        or c.get("contributorRoles", None) == ["Editor"]
    ]
    for num, contributor in enumerate(con):
        contributor_role = (
            "author" if "Author" in contributor.get("contributorRoles") else None
        )
        if contributor_role is None:
            contributor_role = (
                "editor" if "Editor" in contributor.get("contributorRoles") else None
            )
        sequence = "first" if num == 0 else "additional"
        if (
            contributor.get("type", None) == "Organization"
            and contributor.get("name", None) is not None
        ):
            etree.SubElement(
                contributors,
                "organization",
                {"contributor_role": contributor_role, "sequence": sequence},
            ).text = contributor.get("name")
        elif (
            contributor.get("givenName", None) is not None
            or contributor.get("familyName", None) is not None
        ):
            person_name = etree.SubElement(
                contributors,
                "person_name",
                {"contributor_role": contributor_role, "sequence": sequence},
            )
            person_name = insert_crossref_person(contributor, person_name)
        elif contributor.get("affiliations", None) is not None:
            anonymous = etree.SubElement(
                contributors,
                "anonymous",
                {"contributor_role": contributor_role, "sequence": sequence},
            )
            anonymous = insert_crossref_anonymous(contributor, anonymous)
        else:
            etree.SubElement(
                contributors,
                "anonymous",
                {"contributor_role": contributor_role, "sequence": sequence},
            )
    return xml


def insert_crossref_person(contributor, xml):
    """Insert crossref person"""
    if contributor.get("givenName", None) is not None:
        etree.SubElement(xml, "given_name").text = contributor.get("givenName")
    if contributor.get("familyName", None) is not None:
        etree.SubElement(xml, "surname").text = contributor.get("familyName")

    if contributor.get("affiliations", None) is not None:
        affiliations = etree.SubElement(xml, "affiliations")
        institution = etree.SubElement(affiliations, "institution")
        if py_.get(contributor, "affiliations.0.name") is not None:
            etree.SubElement(institution, "institution_name").text = py_.get(
                contributor, "affiliations.0.name"
            )
        if py_.get(contributor, "affiliations.0.id") is not None:
            etree.SubElement(
                institution, "institution_id", {"type": "ror"}
            ).text = py_.get(contributor, "affiliations.0.id")
    orcid = normalize_orcid(contributor.get("id", None))
    if orcid is not None:
        etree.SubElement(xml, "ORCID").text = orcid
    return xml


def insert_crossref_anonymous(contributor, xml):
    """Insert crossref anonymous"""
    if contributor.get("affiliations", None) is None:
        return xml
    affiliations = etree.SubElement(xml, "affiliations")
    institution = etree.SubElement(affiliations, "institution")
    if py_.get(contributor, "affiliations.0.name") is not None:
        etree.SubElement(institution, "institution_name").text = py_.get(
            contributor, "affiliations.0.name"
        )
    return xml


def insert_crossref_titles(metadata, xml):
    """Insert crossref titles"""
    titles = etree.SubElement(xml, "titles")
    for title in wrap(metadata.titles):
        if isinstance(title, dict):
            etree.SubElement(titles, "title").text = title.get("title", None)
        else:
            etree.SubElement(titles, "title").text = title
    return xml


def insert_citation_list(metadata, xml):
    """Insert citation list"""
    if metadata.references is None or len(metadata.references) == 0:
        return xml

    citation_list = etree.SubElement(xml, "citation_list")
    for ref in metadata.references:
        if ref.get("id", None) is None:
            continue
        citation = etree.SubElement(
            citation_list, "citation", {"key": ref.get("key", None)}
        )
        if ref.get("journal_title", None) is not None:
            etree.SubElement(citation, "journal_article").text = ref.get(
                "journal_title"
            )
        if ref.get("author", None) is not None:
            etree.SubElement(citation, "author").text = ref.get("author")
        if ref.get("volume", None) is not None:
            etree.SubElement(citation, "volume").text = ref.get("volume")
        if ref.get("first_page", None) is not None:
            etree.SubElement(citation, "first_page").text = ref.get("first_page")
        if ref.get("publicationYear", None) is not None:
            etree.SubElement(citation, "cYear").text = ref.get("publicationYear")
        if ref.get("title", None) is not None:
            etree.SubElement(citation, "article_title").text = ref.get("title")
        if ref.get("id", None) is not None:
            etree.SubElement(citation, "doi").text = doi_from_url(ref.get("id"))
        if ref.get("unstructured", None) is not None:
            etree.SubElement(citation, "unstructured_citation").text = ref.get(
                "unstructured"
            )
    return xml


def insert_crossref_access_indicators(metadata, xml):
    """Insert crossref access indicators"""
    rights_uri = (
        metadata.license.get("url", None) if metadata.license is not None else None
    )
    if rights_uri is None:
        return xml
    program = etree.SubElement(
        xml,
        "program",
        {
            "xmlns": "http://www.crossref.org/AccessIndicators.xsd",
            "name": "AccessIndicators",
        },
    )
    etree.SubElement(program, "license_ref", {"applies_to": "vor"}).text = rights_uri
    etree.SubElement(program, "license_ref", {"applies_to": "tdm"}).text = rights_uri
    return xml


def insert_crossref_relations(metadata, xml):
    """Insert crossref relations"""
    if metadata.relations is None or len(metadata.relations) == 0:
        return xml
    program = etree.SubElement(
        xml,
        "program",
        {
            "xmlns": "http://www.crossref.org/relations.xsd",
            "name": "relations",
        },
    )
    for relation in metadata.relations:
        if relation.get("type", None) in [
            "IsPartOf",
            "HasPart",
            "IsReviewOf",
            "HasReview",
            "IsRelatedMaterial",
            "HasRelatedMaterial",
        ]:
            group = "inter_work_relation"
        elif relation.get("type", None) in [
            "IsIdenticalTo",
            "IsPreprintOf",
            "HasPreprint",
            "IsTranslationOf",
            "HasTranslation",
            "IsVersionOf",
            "HasVersion",
        ]:
            group = "intra_work_relation"
        else:
            continue

        related_item = etree.SubElement(program, "related_item")
        f = furl(relation.get("id", None))
        if validate_doi(relation.get("id", None)):
            identifier_type = "doi"
            _id = doi_from_url(relation.get("id", None))
        elif f.host == "portal.issn.org":
            identifier_type = "issn"
            _id = f.path.segments[-1]
        elif validate_url(relation.get("id", None)) == "URL":
            identifier_type = "uri"
            _id = relation.get("id", None)
        else:
            identifier_type = "other"
            _id = relation.get("id", None)

        etree.SubElement(
            related_item,
            group,
            {
                "relationship-type": py_.lower_first(relation.get("type"))
                if relation.get("type", None) is not None
                else None,
                "identifier-type": identifier_type,
            },
        ).text = _id

    return xml


def insert_funding_references(metadata, xml):
    """Insert funding references"""
    if metadata.funding_references is None or len(metadata.funding_references) == 0:
        return xml
    program = etree.SubElement(
        xml,
        "program",
        {
            "xmlns": "http://www.crossref.org/fundref.xsd",
            "name": "fundref",
        },
    )
    for funding_reference in metadata.funding_references:
        assertion = etree.SubElement(program, "assertion", {"name": "fundgroup"})
        funder_name = etree.SubElement(
            assertion,
            "assertion",
            {"name": "funder_name"},
        )
        if funding_reference.get("funderIdentifier", None) is not None:
            funder_identifier = funding_reference.get("funderIdentifier", None)

            # translate ROR to Crossref funder ID until Crossref supports ROR
            funder_identifier = ROR_TO_CROSSREF_FUNDER_ID_TRANSLATIONS.get(
                funder_identifier, funder_identifier
            )

            etree.SubElement(
                funder_name,
                "assertion",
                {"name": "funder_identifier"},
            ).text = funder_identifier
        if funding_reference.get("awardNumber", None) is not None:
            etree.SubElement(
                assertion,
                "assertion",
                {"name": "award_number"},
            ).text = funding_reference.get("awardNumber", None)
        funder_name.text = funding_reference.get("funderName", None)
    return xml


def insert_crossref_subjects(metadata, xml):
    """Insert crossref subjects"""
    if metadata.subjects is None:
        return xml
    subjects = etree.SubElement(xml, "subjects")
    for subject in metadata.subjects:
        if isinstance(subject, dict):
            etree.SubElement(subjects, "subject").text = subject.get("subject", None)
        else:
            etree.SubElement(subjects, "subject").text = subject
    return xml


def insert_crossref_language(metadata, xml):
    """Insert crossref language"""
    if metadata.language is None:
        return xml
    etree.SubElement(xml, "language").text = metadata.language
    return xml


def insert_crossref_publication_date(metadata, xml):
    """Insert crossref publication date"""
    pub_date = parse(metadata.date.get("published", None))
    if pub_date is None:
        return xml

    publication_date = etree.SubElement(
        xml, "publication_date", {"media_type": "online"}
    )
    etree.SubElement(publication_date, "month").text = f"{pub_date.month:d}"
    etree.SubElement(publication_date, "day").text = f"{pub_date.day:d}"
    etree.SubElement(publication_date, "year").text = str(pub_date.year)
    return xml


def insert_posted_date(metadata, xml):
    """Insert posted date"""
    pub_date = parse(metadata.date.get("published", None))
    if pub_date is None:
        return xml

    posted_date = etree.SubElement(xml, "posted_date", {"media_type": "online"})
    etree.SubElement(posted_date, "month").text = f"{pub_date.month:d}"
    etree.SubElement(posted_date, "day").text = f"{pub_date.day:d}"
    etree.SubElement(posted_date, "year").text = str(pub_date.year)
    return xml


def insert_institution(metadata, xml):
    """Insert institution"""
    if metadata.publisher.get("name", None) is None:
        return xml
    institution = etree.SubElement(xml, "institution")
    etree.SubElement(institution, "institution_name").text = metadata.publisher.get(
        "name"
    )
    return xml


def insert_item_number(metadata, xml):
    """Insert item number"""
    if metadata.identifiers is None:
        return xml
    for identifier in metadata.identifiers:
        if identifier.get("identifierType", None) == "UUID":
            # strip hyphen from UUIDs, as item_number can only be 32 characters long (UUIDv4 is 36 characters long)
            if identifier.get("identifierType", None) == "UUID":
                identifier["identifier"] = identifier.get("identifier", "").replace(
                    "-", ""
                )
            etree.SubElement(
                xml,
                "item_number",
                {"item_number_type": identifier.get("identifierType", "").lower()},
            ).text = identifier.get("identifier", None)
        else:
            continue
    return xml


def insert_archive_locations(metadata, xml):
    """Insert archive locations"""
    if metadata.archive_locations is None:
        return xml
    archive_locations = etree.SubElement(xml, "archive_locations")
    for archive_location in metadata.archive_locations:
        etree.SubElement(archive_locations, "archive", {"name": archive_location})
    return xml


def insert_doi_data(metadata, xml):
    """Insert doi data"""
    if doi_from_url(metadata.id) is None or metadata.url is None:
        return xml
    doi_data = etree.SubElement(xml, "doi_data")
    etree.SubElement(doi_data, "doi").text = doi_from_url(metadata.id)
    etree.SubElement(doi_data, "resource").text = metadata.url
    collection = etree.SubElement(doi_data, "collection", {"property": "text-mining"})
    item = etree.SubElement(collection, "item")
    etree.SubElement(item, "resource", {"mime_type": "text/html"}).text = metadata.url
    if metadata.files is None:
        return xml
    for file in metadata.files:
        # Crossref schema currently doesn't support text/markdown
        if file.get("mimeType", None) == "text/markdown":
            file["mimeType"] = "text/plain"
        item = etree.SubElement(collection, "item")
        etree.SubElement(
            item, "resource", {"mime_type": file.get("mimeType", "")}
        ).text = file.get("url", None)
    return xml


def insert_crossref_license(metadata, xml):
    """Insert crossref license"""
    if metadata.license is None:
        return xml
    license_ = etree.SubElement(xml, "license")
    if isinstance(metadata.license, dict):
        r = metadata.license
    else:
        r = {}
        r["rights"] = metadata.license
        r["rightsUri"] = normalize_id(metadata.license)
    attributes = compact(
        {
            "rightsURI": r.get("rightsUri", None),
            "rightsIdentifier": r.get("rightsIdentifier", None),
            "rightsIdentifierScheme": r.get("rightsIdentifierScheme"),
            "schemeURI": r.get("schemeUri", None),
            "xml:lang": r.get("lang", None),
        }
    )
    etree.SubElement(license_, "rights", attributes).text = r.get("rights", None)
    return xml


def insert_crossref_issn(metadata, xml):
    """Insert crossref issn"""
    if (
        metadata.container is None
        or metadata.container.get("identifierType", None) != "ISSN"
    ):
        return xml
    etree.SubElement(xml, "issn").text = metadata.container.get("identifier", None)
    return xml


def insert_crossref_abstract(metadata, xml):
    """Insert crossref abstrac"""
    if metadata.descriptions is None:
        return xml
    if isinstance(metadata.descriptions[0], dict):
        d = metadata.descriptions[0]
    else:
        d = {}
        d["description"] = metadata.descriptions[0]
    abstract = etree.SubElement(
        xml, "abstract", {"xmlns": "http://www.ncbi.nlm.nih.gov/JATS1"}
    )
    etree.SubElement(abstract, "p").text = d.get("description", None)
    return xml


def crossref_root():
    """Crossref root with namespaces"""
    doi_batch = """<doi_batch xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.crossref.org/schema/5.3.1" xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" xmlns:fr="http://www.crossref.org/fundref.xsd" xmlns:mml="http://www.w3.org/1998/Math/MathML" xsi:schemaLocation="http://www.crossref.org/schema/5.3.1 https://www.crossref.org/schemas/crossref5.3.1.xsd" version="5.3.1"></doi_batch>"""
    return etree.fromstring(doi_batch)


def generate_crossref_xml_list(metalist) -> Optional[str]:
    """Generate Crossref XML list."""
    if not metalist.is_valid:
        return None
    xml = crossref_root()
    head = etree.SubElement(xml, "head")
    # we use a uuid as batch_id
    etree.SubElement(head, "doi_batch_id").text = str(uuid.uuid4())
    etree.SubElement(head, "timestamp").text = datetime.now().strftime("%Y%m%d%H%M%S")
    depositor = etree.SubElement(head, "depositor")
    etree.SubElement(depositor, "depositor_name").text = metalist.depositor or "test"
    etree.SubElement(depositor, "email_address").text = (
        metalist.email or "info@example.org"
    )
    etree.SubElement(head, "registrant").text = metalist.registrant or "test"

    body = etree.SubElement(xml, "body")
    body = [insert_crossref_work(item, body) for item in metalist.items]
    return etree.tostring(
        xml,
        doctype='<?xml version="1.0" encoding="UTF-8"?>',
        pretty_print=True,
    )
