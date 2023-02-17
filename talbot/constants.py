"""Constants for the Talbot project"""
from typing import Optional, Union, TypedDict, List
from os import path


class TalbotMeta(TypedDict):
    """TypedDict for TalbotMeta"""
    pid: str
    doi: str
    url: str
    creators: List[dict]
    titles: List[dict]
    publisher: str
    publication_year: int
    types: dict
    subjects: Optional[List[dict]]
    contributors: Optional[List[dict]]
    dates: Optional[List[dict]]
    language: Optional[str]
    alternate_identifiers: Optional[List[dict]]
    sizes: Optional[List[dict]]
    formats: Optional[List[dict]]
    version: Optional[str]
    rights: Optional[List[dict]]
    descriptions: Optional[List[dict]]
    geo_locations: Optional[List[dict]]
    funding_references: Optional[List[dict]]
    related_items: Optional[List[dict]]
    container: Optional[dict]
    date_created: Optional[str]
    date_registered: Optional[str]
    date_published: Optional[str]
    date_updated: Optional[str]
    content_url: Optional[List[dict]]
    agency: Optional[str]
    state: str
    schema_version: Optional[str]


CR_TO_BIB_TRANSLATIONS = {
    "Proceedings": "proceedings",
    "ReferenceBook": "book",
    "JournalIssue": None,
    "ProceedingsArticle": "inproceedings",
    "Other": None,
    "Dissertation": "phdthesis",
    "Dataset": None,
    "EditedBook": "book",
    "JournalArticle": "article",
    "Journal": None,
    "Report": "techreport",
    "BookSeries": None,
    "ReportSeries": None,
    "BookTrack": None,
    "Standard": None,
    "BookSection": "inbook",
    "BookPart": None,
    "Book": "book",
    "BookChapter": "inbook",
    "StandardSeries": None,
    "Monograph": "book",
    "Component": None,
    "ReferenceEntry": None,
    "JournalVolume": None,
    "BookSet": None,
    "PostedContent": "article",
}

CR_TO_CP_TRANSLATIONS = {
    "Proceedings": None,
    "ReferenceBook": None,
    "JournalIssue": "article-journal",
    "ProceedingsArticle": "paper-conference",
    "Other": None,
    "Dissertation": "thesis",
    "Dataset": "dataset",
    "EditedBook": "book",
    "PostedContent": "article-journal",
    "JournalArticle": "article-journal",
    "Journal": None,
    "Report": "report",
    "BookSeries": None,
    "ReportSeries": None,
    "BookTrack": None,
    "Standard": None,
    "BookSection": "chapter",
    "BookPart": None,
    "Book": "book",
    "BookChapter": "chapter",
    "StandardSeries": None,
    "Monograph": "book",
    "Component": None,
    "ReferenceEntry": "entry-dictionary",
    "JournalVolume": None,
    "BookSet": None,
}

CR_TO_DC_TRANSLATIONS = {
    "Proceedings": None,
    "ReferenceBook": None,
    "JournalIssue": "Text",
    "ProceedingsArticle": "ConferencePaper",
    "Other": "Other",
    "Dissertation": "Dissertation",
    "Dataset": "Dataset",
    "EditedBook": "Book",
    "JournalArticle": "JournalArticle",
    "Journal": "Journal",
    "Report": "Report",
    "BookSeries": None,
    "ReportSeries": None,
    "BookTrack": None,
    "Standard": "Standard",
    "BookSection": "BookChapter",
    "BookPart": None,
    "Book": "Book",
    "BookChapter": "BookChapter",
    "SaComponent": "Text",
    "StandardSeries": "Standard",
    "Monograph": "Book",
    "Component": None,
    "ReferenceEntry": None,
    "JournalVolume": None,
    "BookSet": None,
    "PostedContent": "Preprint",
    "PeerReview": "PeerReview",
}

CR_TO_RIS_TRANSLATIONS = {
    "Proceedings": "CONF",
    "PostedContent": "JOUR",
    "ReferenceBook": "BOOK",
    "JournalIssue": "JOUR",
    "ProceedingsArticle": "CPAPER",
    "Other": "GEN",
    "Dissertation": "THES",
    "Dataset": "DATA",
    "EditedBook": "BOOK",
    "JournalArticle": "JOUR",
    "Journal": None,
    "Report": "RPRT",
    "BookSeries": None,
    "ReportSeries": None,
    "BookTrack": None,
    "Standard": "STAND",
    "BookSection": "CHAP",
    "BookPart": "CHAP",
    "Book": "BOOK",
    "BookChapter": "CHAP",
    "StandardSeries": None,
    "Monograph": "BOOK",
    "Component": None,
    "ReferenceEntry": "DICT",
    "JournalVolume": None,
    "BookSet": None,
}

CR_TO_SO_TRANSLATIONS = {
    "Proceedings": None,
    "ReferenceBook": "Book",
    "JournalIssue": "PublicationIssue",
    "ProceedingsArticle": None,
    "Other": "CreativeWork",
    "Dissertation": "Thesis",
    "Dataset": "Dataset",
    "EditedBook": "Book",
    "JournalArticle": "ScholarlyArticle",
    "Journal": None,
    "Report": "Report",
    "BookSeries": None,
    "ReportSeries": None,
    "BookTrack": None,
    "Standard": None,
    "BookSection": None,
    "BookPart": None,
    "Book": "Book",
    "BookChapter": "Chapter",
    "StandardSeries": None,
    "Monograph": "Book",
    "Component": "CreativeWork",
    "ReferenceEntry": None,
    "JournalVolume": "PublicationVolume",
    "BookSet": None,
    "PostedContent": "ScholarlyArticle",
    "PeerReview": "Review",
}

DC_TO_RIS_TRANSLATIONS = {
    "Audiovisual": "MPCT",
    "Book": "BOOK",
    "BookChapter": "CHAP",
    "Collection": None,
    "ComputationalNotebook": "COMP",
    "ConferencePaper": "CPAPER",
    "ConferenceProceeding": "CONF",
    "DataPaper": None,
    "Dataset": "DATA",
    "Dissertation": "THES",
    "Event": None,
    "Image": "FIGURE",
    "InteractiveResource": None,
    "Journal": None,
    "JournalArticle": "JOUR",
    "Model": None,
    "OutputManagementPlan": None,
    "PeerReview": None,
    "PhysicalObject": None,
    "Preprint": "RPRT",
    "Report": "RRPT",
    "Service": None,
    "Software": "COMP",
    "Sound": "SOUND",
    "Standard": None,
    "Text": "RPRT",
    "Workflow": None,
    "Other": None,
}

DC_TO_SO_TRANSLATIONS = {
    "Audiovisual": "MediaObject",
    "Book": "Book",
    "BookChapter": "Chapter",
    "Collection": "Collection",
    "ComputationalNotebook": "SoftwareSourceCode",
    "ConferencePaper": "Article",
    "ConferenceProceeding": "Periodical",
    "DataPaper": "Article",
    "Dataset": "Dataset",
    "Dissertation": "Thesis",
    "Event": "Event",
    "Image": "ImageObject",
    "InteractiveResource": None,
    "Journal": "Periodical",
    "JournalArticle": "ScholarlyArticle",
    "Model": None,
    "OutputManagementPlan": None,
    "PeerReview": "Review",
    "PhysicalObject": None,
    "Preprint": None,
    "Report": "Report",
    "Service": "Service",
    "Software": "SoftwareSourceCode",
    "Sound": "AudioObject",
    "Standard": None,
    "Text": "ScholarlyArticle",
    "Workflow": None,
    "Other": "CreativeWork",
    # not part of DataCite schema, but used internally
    "Periodical": "Periodical",
    "DataCatalog": "DataCatalog",
}

RIS_TO_BIB_TRANSLATIONS = {
    "JOUR": "article",
    "BOOK": "book",
    "CHAP": "inbook",
    "CPAPER": "inproceedings",
    "GEN": "misc",
    "THES": "phdthesis",
    "CONF": "proceedings",
    "RPRT": "techreport",
    "UNPD": "unpublished",
}

RIS_TO_CP_TRANSLATIONS = {"JOUR": "article-journal"}

RIS_TO_DC_TRANSLATIONS = {
    "BLOG": "Text",
    "GEN": "Text",
    "CTLG": "Collection",
    "DATA": "Dataset",
    "FIGURE": "Image",
    "THES": "Dissertation",
    "MPCT": "Audiovisual",
    "JOUR": "JournalArticle",
    "COMP": "Software",
    "VIDEO": "Audiovisual",
    "ELEC": "Text",
}

RIS_TO_SO_TRANSLATIONS = {
    "BLOG": "BlogPosting",
    "GEN": "CreativeWork",
    "CTLG": "DataCatalog",
    "DATA": "Dataset",
    "FIGURE": "ImageObject",
    "THES": "Thesis",
    "MPCT": "Movie",
    "JOUR": "ScholarlyArticle",
    "COMP": "SoftwareSourceCode",
    "VIDEO": "VideoObject",
    "ELEC": "WebPage",
}

SO_TO_BIB_TRANSLATIONS = {
    "Article": "article",
    "AudioObject": "misc",
    "Thesis": "phdthesis",
    "Blog": "misc",
    "BlogPosting": "article",
    "Collection": "misc",
    "CreativeWork": "misc",
    "DataCatalog": "misc",
    "Dataset": "misc",
    "Event": "misc",
    "ImageObject": "misc",
    "Movie": "misc",
    "PublicationIssue": "misc",
    "ScholarlyArticle": "article",
    "Service": "misc",
    "SoftwareSourceCode": "misc",
    "VideoObject": "misc",
    "WebPage": "misc",
    "WebSite": "misc",
}

SO_TO_CP_TRANSLATIONS = {
    "Article": "article-newspaper",
    "AudioObject": "song",
    "Blog": "report",
    "BlogPosting": "post-weblog",
    "Collection": None,
    "CreativeWork": None,
    "DataCatalog": "dataset",
    "Dataset": "dataset",
    "Event": None,
    "ImageObject": "graphic",
    "Movie": "motion_picture",
    "PublicationIssue": None,
    "Report": "report",
    "ScholarlyArticle": "article-journal",
    "Service": None,
    "Thesis": "thesis",
    "VideoObject": "broadcast",
    "WebPage": "webpage",
    "WebSite": "webpage",
}

SO_TO_DC_TRANSLATIONS = {
    "Article": "Preprint",
    "AudioObject": "Sound",
    "Blog": "Text",
    "BlogPosting": "Preprint",
    "Book": "Book",
    "Chapter": "BookChapter",
    "Collection": "Collection",
    "CreativeWork": "Text",
    "DataCatalog": "Dataset",
    "Dataset": "Dataset",
    "Event": "Event",
    "ImageObject": "Image",
    "Movie": "Audiovisual",
    "PublicationIssue": "Text",
    "Report": "Report",
    "ScholarlyArticle": "Text",
    "Thesis": "Text",
    "Service": "Service",
    "Review": "PeerReview",
    "SoftwareSourceCode": "Software",
    "VideoObject": "Audiovisual",
    "WebPage": "Text",
    "WebSite": "Text",
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

SO_TO_RIS_TRANSLATIONS = {
    "Article": "GEN",
    "AudioObject": None,
    "Blog": None,
    "BlogPosting": "BLOG",
    "Collection": None,
    "CreativeWork": "GEN",
    "DataCatalog": "CTLG",
    "Dataset": "DATA",
    "Event": None,
    "ImageObject": "FIGURE",
    "Movie": "MPCT",
    "Report": "RPRT",
    "PublicationIssue": None,
    "ScholarlyArticle": "JOUR",
    "Service": None,
    "SoftwareSourceCode": "COMP",
    "VideoObject": "VIDEO",
    "WebPage": "ELEC",
    "WebSite": None,
}

CP_TO_SO_TRANSLATIONS = {
    'song': 'AudioObject',
    'post-weblog': 'BlogPosting',
    'dataset': 'Dataset',
    'graphic': 'ImageObject',
    'motion_picture': 'Movie',
    'article-journal': 'ScholarlyArticle',
    'broadcast': 'VideoObject',
    'webpage': 'WebPage'
}

CP_TO_RIS_TRANSLATIONS = {
    'post-weblog': 'BLOG',
    'dataset': 'DATA',
    'graphic': 'FIGURE',
    'book': 'BOOK',
    'motion_picture': 'MPCT',
    'article-journal': 'JOUR',
    'broadcast': 'MPCT',
    'webpage': 'ELEC'
}

CP_TO_DC_TRANSLATIONS = {
    'song': 'Audiovisual',
    'post-weblog': 'Text',
    'dataset': 'Dataset',
    'graphic': 'Image',
    'motion_picture': 'Audiovisual',
    'article-journal': 'JournalArticle',
    'broadcast': 'Audiovisual',
    'webpage': 'Text'
}
