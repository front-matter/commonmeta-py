"""Constants for commonmeta-py"""
from typing import Optional, TypedDict, List


class Commonmeta(TypedDict):
    """TypedDict for Commonmeta"""

    id: str
    type: str
    url: str
    creators: List[dict]
    titles: List[dict]
    publisher: dict
    date: dict
    additional_type: Optional[str]
    subjects: Optional[List[dict]]
    contributors: Optional[List[dict]]
    language: Optional[str]
    alternate_identifiers: Optional[List[dict]]
    sizes: Optional[List[dict]]
    formats: Optional[List[dict]]
    version: Optional[str]
    license: Optional[dict]
    descriptions: Optional[List[dict]]
    geo_locations: Optional[List[dict]]
    funding_references: Optional[List[dict]]
    references: Optional[List[dict]]
    container: Optional[dict]
    content_url: Optional[List[dict]]
    agency: Optional[str]
    state: str
    schema_version: Optional[str]


# source: https://www.bibtex.com/e/entry-types/
BIB_TO_CM_TRANSLATIONS = {
    "article": "JournalArticle",
    "book": "Book",
    "booklet": "Book",
    "inbook": "BookChapter",
    "inproceedings": "ProceedingsArticle",
    "manual": "Report",
    "mastersthesis": "Dissertation",
    "misc": "Other",
    "phdthesis": "Dissertation",
    "proceedings": "Proceedings",
    "techreport": "Report",
    "unpublished": "Manuscript",
}

CM_TO_BIB_TRANSLATIONS = {
    "Article": "article",
    "Book": "book",
    "BookChapter": "inbook",
    "Dissertation": "phdthesis",
    "JournalArticle": "article",
    "Manuscript": "unpublished",
    "Other": "misc",
    "Proceedings": "proceedings",
    "ProceedingsArticle": "inproceedings",
    "Report": "techreport",
}

# source: https://docs.citationstyles.org/en/stable/specification.html?highlight=book#appendix-iii-types
CSL_TO_CM_TRANSLATIONS = {
    "article": "Article",
    "article-journal": "JournalArticle",
    "article-magazine": "Article",
    "article-newspaper": "Article",
    "bill": "LegalDocument",
    "book": "Book",
    "broadcast": "Audiovisual",
    "chapter": "BookChapter",
    "classic": "Book",
    "collection": "Collection",
    "dataset": "Dataset",
    "document": "Document",
    "entry": "Entry",
    "entry-dictionary": "Entry",
    "entry-encyclopedia": "Entry",
    "event": "Event",
    "figure": "Figure",
    "graphic": "Image",
    "hearing": "LegalDocument",
    "interview": "Document",
    "legal_case": "LegalDocument",
    "legislation": "LegalDocument",
    "manuscript": "Manuscript",
    "map": "Map",
    "motion_picture": "Audiovisual",
    "musical_score": "Document",
    "pamphlet": "Document",
    "paper-conference": "ProceedingsArticle",
    "patent": "Patent",
    "performance": "Performance",
    "periodical": "Journal",
    "personal_communication": "PersonalCommunication",
    "post": "Post",
    "post-weblog": "Article",
    "regulation": "LegalDocument",
    "report": "Report",
    "review": "Review",
    "review-book": "Review",
    "software": "Software",
    "song": "Audiovisual",
    "speech": "Speech",
    "standard": "Standard",
    "thesis": "Dissertation",
    "treaty": "LegalDocument",
    "webpage": "WebPage",
}

CM_TO_CSL_TRANSLATIONS = {
    "Article": "article",
    "JournalArticle": "article-journal",
    "Book": "book",
    "BookChapter": "chapter",
    "Collection": "collection",
    "Dataset": "dataset",
    "Document": "document",
    "Entry": "entry",
    "Event": "event",
    "Figure": "figure",
    "Image": "graphic",
    "LegalDocument": "legal_case",
    "Manuscript": "manuscript",
    "Map": "map",
    "Audiovisual": "motion_picture",
    "Patent": "patent",
    "Performance": "performance",
    "Journal": "periodical",
    "PersonalCommunication": "personal_communication",
    "Post": "post",
    "Report": "report",
    "Review": "review",
    "Software": "software",
    "Speech": "speech",
    "Standard": "standard",
    "Dissertation": "thesis",
    "WebPage": "webpage",
}

# source: http://api.crossref.org/types
CR_TO_CM_TRANSLATIONS = {
    "BookChapter": "BookChapter",
    "BookPart": "BookPart",
    "BookSection": "BookSection",
    "BookSeries": "BookSeries",
    "BookSet": "BookSet",
    "BookTrack": "BookTrack",
    "Book": "Book",
    "Component": "Component",
    "Database": "Database",
    "Dataset": "Dataset",
    "Dissertation": "Dissertation",
    "EditedBook": "EditedBook",
    "Grant": "Grant",
    "JournalArticle": "JournalArticle",
    "JournalIssue": "JournalIssue",
    "JournalVolume": "JournalVolume",
    "Journal": "Journal",
    "Monograph": "Book",
    "Other": "Other",
    "PeerReview": "Review",
    "PostedContent": "Article",
    "ProceedingsArticle": "ProceedingsArticle",
    "ProceedingsSeries": "ProceedingsSeries",
    "Proceedings": "Proceedings",
    "ReferenceBook": "ReferenceBook",
    "ReferenceEntry": "Entry",
    "ReportComponent": "ReportComponent",
    "ReportSeries": "ReportSeries",
    "Report": "Report",
    "Standard": "Standard",
}

CM_TO_CR_TRANSLATIONS = {
    "Article": "PostedContent",
    "BookChapter": "BookChapter",
    "BookSeries": "BookSeries",
    "Book": "Book",
    "Component": "Component",
    "Dataset": "Dataset",
    "Dissertation": "Dissertation",
    "Grant": "Grant",
    "JournalArticle": "JournalArticle",
    "JournalIssue": "JournalIssue",
    "JournalVolume": "JournalVolume",
    "Journal": "Journal",
    "ProceedingsArticle": "ProceedingsArticle",
    "ProceedingsSeries": "ProceedingsSeries",
    "Proceedings": "Proceedings",
    "ReportComponent": "ReportComponent",
    "ReportSeries": "ReportSeries",
    "Report": "Report",
    "Review": "PeerReview",
    "Other": "Other",
}

# source: https://github.com/datacite/schema/blob/master/source/meta/kernel-4/include/datacite-resourceType-v4.xsd
DC_TO_CM_TRANSLATIONS = {
    "Audiovisual": "Audiovisual",
    "BlogPosting": "Article",
    "Book": "Book",
    "BookChapter": "BookChapter",
    "Collection": "Collection",
    "ComputationalNotebook": "ComputationalNotebook",
    "ConferencePaper": "ProceedingsArticle",
    "ConferenceProceeding": "Proceedings",
    "DataPaper": "JournalArticle",
    "Dataset": "Dataset",
    "Dissertation": "Dissertation",
    "Event": "Event",
    "Image": "Image",
    "InteractiveResource": "InteractiveResource",
    "Journal": "Journal",
    "JournalArticle": "JournalArticle",
    "Model": "Model",
    "OutputManagementPlan": "OutputManagementPlan",
    "PeerReview": "PeerReview",
    "PhysicalObject": "PhysicalObject",
    "Poster": "Speech",
    "Preprint": "Article",
    "Report": "Report",
    "Service": "Service",
    "Software": "Software",
    "Sound": "Sound",
    "Standard": "Standard",
    "Text": "Document",
    "Thesis": "Dissertation",
    "Workflow": "Workflow",
    "Other": "Other",
}

CM_TO_DC_TRANSLATIONS = {
    "Article": "Preprint",
    "Audiovisual": "Audiovisual",
    "Book": "Book",
    "BookChapter": "BookChapter",
    "Collection": "Collection",
    "Dataset": "Dataset",
    "Document": "Text",
    "Entry": "Text",
    "Event": "Event",
    "Figure": "Image",
    "Image": "Image",
    "JournalArticle": "JournalArticle",
    "LegalDocument": "Text",
    "Manuscript": "Text",
    "Map": "Image",
    "Patent": "Text",
    "Performance": "Audiovisual",
    "PersonalCommunication": "Text",
    "Post": "Text",
    "ProceedingsArticle": "ConferencePaper",
    "Proceedings": "ConferenceProceeding",
    "Report": "Report",
    "Review": "PeerReview",
    "Software": "Software",
    "Sound": "Sound",
    "Standard": "Standard",
    "WebPage": "Text",
}

RIS_TO_CM_TRANSLATIONS = {
    "ABST": "Text",
    "ADVS": "Text",
    "AGGR": "Text",
    "ANCIENT": "Text",
    "ART": "Text",
    "BILL": "Text",
    "BLOG": "Text",
    "BOOK": "Book",
    "CASE": "Text",
    "CHAP": "BookChapter",
    "CHART": "Text",
    "CLSWK": "Text",
    "CTLG": "Collection",
    "COMP": "Software",
    "DATA": "Dataset",
    "DBASE": "Database",
    "DICT": "Dictionary",
    "EBOOK": "Book",
    "ECHAP": "BookChapter",
    "EDBOOK": "Book",
    "EJOUR": "JournalArticle",
    "ELEC": "Text",
    "ENCYC": "Encyclopedia",
    "EQUA": "Equation",
    "FIGURE": "Image",
    "GEN": "CreativeWork",
    "GOVDOC": "GovernmentDocument",
    "GRANT": "Grant",
    "HEAR": "Hearing",
    "ICOMM": "Text",
    "INPR": "Text",
    "JFULL": "JournalArticle",
    "JOUR": "JournalArticle",
    "LEGAL": "LegalRuleOrRegulation",
    "MANSCPT": "Text",
    "MAP": "Map",
    "MGZN": "MagazineArticle",
    "MPCT": "Audiovisual",
    "MULTI": "Audiovisual",
    "MUSIC": "MusicScore",
    "NEWS": "NewspaperArticle",
    "PAMP": "Pamphlet",
    "PAT": "Patent",
    "PCOMM": "PersonalCommunication",
    "RPRT": "Report",
    "SER": "SerialPublication",
    "SLIDE": "Slide",
    "SOUND": "SoundRecording",
    "STAND": "Standard",
    "THES": "Dissertation",
    "UNBILL": "UnenactedBill",
    "UNPB": "UnpublishedWork",
    "VIDEO": "Audiovisual",
    "WEB": "WebPage",
}

CM_TO_RIS_TRANSLATIONS = {
    "Article": "JOUR",
    "Audiovisual": "VIDEO",
    "Book": "BOOK",
    "BookChapter": "CHAP",
    "Collection": "CTLG",
    "Dataset": "DATA",
    "Dissertation": "THES",
    "Document": "GEN",
    "Entry": "DICT",
    "Event": "GEN",
    "Figure": "FIGURE",
    "Image": "FIGURE",
    "JournalArticle": "JOUR",
    "LegalDocument": "GEN",
    "Manuscript": "GEN",
    "Map": "MAP",
    "Patent": "PAT",
    "Performance": "GEN",
    "PersonalCommunication": "PCOMM",
    "Post": "GEN",
    "ProceedingsArticle": "CPAPER",
    "Proceedings": "CONF",
    "Report": "RPRT",
    "Review": "GEN",
    "Software": "COMP",
    "Sound": "SOUND",
    "Standard": "STAND",
    "WebPage": "WEB",
}

SO_TO_CM_TRANSLATIONS = {
    "Article": "Article",
    "BlogPosting": "Article",
    "Book": "Book",
    "BookChapter": "BookChapter",
    "CreativeWork": "Other",
    "Dataset": "Dataset",
    "Dissertation": "Dissertation",
    "NewsArticle": "Article",
    "Legislation": "LegalDocument",
    "ScholarlyArticle": "JournalArticle",
    "SoftwareSourceCode": "Software",
}

CM_TO_SO_TRANSLATIONS = {
    "Article": "Article",
    "Book": "Book",
    "BookChapter": "BookChapter",
    "Dataset": "Dataset",
    "Dissertation": "Dissertation",
    "LegalDocument": "Legislation",
    "JournalArticle": "ScholarlyArticle",
    "Software": "SoftwareSourceCode",
}

SO_TO_DC_RELATION_TYPES = {
    "citation": "References",
    "isBasedOn": "IsSupplementedBy",
    "sameAs": "IsIdenticalTo",
    "isPartOf": "IsPartOf",
    "hasPart": "HasPart",
    "isPredecessor": "IsPreviousVersionOf",
    "isSuccessor": "IsNewVersionOf",
}

SO_TO_DC_REVERSE_RELATION_TYPES = {
    "citation": "IsReferencedBy",
    "isBasedOn": "IsSupplementTo",
    "sameAs": "IsIdenticalTo",
    "isPartOf": "HasPart",
    "hasPart": "IsPartOf",
    "isPredecessor": "IsNewVersionOf",
    "isSuccessor": "IsPreviousVersionOf",
}

CROSSREF_CONTAINER_TYPES = {
    "BookChapter": "book",
    "Dataset": "database",
    "JournalArticle": "journal",
    "JournalIssue": "journal",
    "Monograph": "book-series",
    "ProceedingsArticle": "proceedings",
}
