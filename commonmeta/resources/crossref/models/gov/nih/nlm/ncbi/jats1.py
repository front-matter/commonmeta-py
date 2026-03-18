from dataclasses import dataclass, field
from enum import Enum
from typing import ForwardRef, Optional, Union

from .....mathml3 import Math
from .....org.niso.schemas.ali.mod_1 import (
    FreeToRead,
    LicenseRef,
)
from .....xlink import (
    ActuateType,
    ShowType,
    TypeType,
)
from .....xml import (
    LangValue,
    SpaceValue,
)

__NAMESPACE__ = "http://www.ncbi.nlm.nih.gov/JATS1"


@dataclass
class AccessDate:
    """
    <div> <h3>Access Date For Cited Work</h3> </div>
    """

    class Meta:
        name = "access-date"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    calendar: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    iso_8601_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "iso-8601-date",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


class ArrayOrientation(Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"


class ArticleIdPubIdType(Enum):
    ACCESSION = "accession"
    ARCHIVE = "archive"
    ARK = "ark"
    ART_ACCESS_ID = "art-access-id"
    ARXIV = "arxiv"
    CODEN = "coden"
    CUSTOM = "custom"
    DOAJ = "doaj"
    DOI = "doi"
    HANDLE = "handle"
    INDEX = "index"
    ISBN = "isbn"
    MANUSCRIPT = "manuscript"
    MEDLINE = "medline"
    MR = "mr"
    OTHER = "other"
    PII = "pii"
    PMCID = "pmcid"
    PMID = "pmid"
    PUBLISHER_ID = "publisher-id"
    SICI = "sici"
    STD_DESIGNATION = "std-designation"
    ZBL = "zbl"


class ArticleDtdVersion(Enum):
    VALUE_0_4 = "0.4"
    VALUE_1_0 = "1.0"
    VALUE_1_1 = "1.1"
    VALUE_1_1D1 = "1.1d1"
    VALUE_1_1D2 = "1.1d2"
    VALUE_1_1D3 = "1.1d3"
    VALUE_1_2 = "1.2"
    VALUE_1_2D1 = "1.2d1"
    VALUE_1_2D2 = "1.2d2"
    VALUE_1_3D1 = "1.3d1"
    VALUE_1_3D2 = "1.3d2"
    VALUE_3_0 = "3.0"


class BoldToggle(Enum):
    NO = "no"
    YES = "yes"


class BoxedTextOrientation(Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"


class BoxedTextPosition(Enum):
    ANCHOR = "anchor"
    BACKGROUND = "background"
    FLOAT = "float"
    MARGIN = "margin"


@dataclass
class Break:
    """
    <div> <h3>Line Break</h3> </div>
    """

    class Meta:
        name = "break"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


class ChemStructWrapOrientation(Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"


class ChemStructWrapPosition(Enum):
    ANCHOR = "anchor"
    BACKGROUND = "background"
    FLOAT = "float"
    MARGIN = "margin"


class CodeExecutable(Enum):
    NO = "no"
    YES = "yes"


class CodeOrientation(Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"


class CodePosition(Enum):
    ANCHOR = "anchor"
    BACKGROUND = "background"
    FLOAT = "float"
    MARGIN = "margin"


class ColAlign(Enum):
    CENTER = "center"
    CHAR = "char"
    JUSTIFY = "justify"
    LEFT = "left"
    RIGHT = "right"


class ColValign(Enum):
    BASELINE = "baseline"
    BOTTOM = "bottom"
    MIDDLE = "middle"
    TOP = "top"


class ColgroupAlign(Enum):
    CENTER = "center"
    CHAR = "char"
    JUSTIFY = "justify"
    LEFT = "left"
    RIGHT = "right"


class ColgroupValign(Enum):
    BASELINE = "baseline"
    BOTTOM = "bottom"
    MIDDLE = "middle"
    TOP = "top"


@dataclass
class CompoundKwd:
    """
    <div> <h3>Compound Keyword</h3> </div>
    """

    class Meta:
        name = "compound-kwd"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    compound_kwd_part: list["CompoundKwdPart"] = field(
        default_factory=list,
        metadata={
            "name": "compound-kwd-part",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    vocab_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term",
            "type": "Attribute",
        },
    )
    vocab_term_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term-identifier",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class CompoundSubject:
    """
    <div> <h3>Compound Subject Name</h3> </div>
    """

    class Meta:
        name = "compound-subject"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    compound_subject_part: list["CompoundSubjectPart"] = field(
        default_factory=list,
        metadata={
            "name": "compound-subject-part",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    vocab_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term",
            "type": "Attribute",
        },
    )
    vocab_term_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term-identifier",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


class ContribIdAuthenticated(Enum):
    FALSE = "false"
    TRUE = "true"


class ContribCorresp(Enum):
    NO = "no"
    YES = "yes"


class ContribDeceased(Enum):
    NO = "no"
    YES = "yes"


class ContribEqualContrib(Enum):
    NO = "no"
    YES = "yes"


@dataclass
class CopyrightYear:
    """
    <div> <h3>Copyright Year</h3> </div>
    """

    class Meta:
        name = "copyright-year"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Count:
    """
    <div> <h3>Count</h3> </div>
    """

    class Meta:
        name = "count"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    count: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    count_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "count-type",
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class ElocationId:
    """
    <div> <h3>Electronic Location Identifier</h3> </div>
    """

    class Meta:
        name = "elocation-id"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    seq: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class EquationCount:
    """
    <div> <h3>Equation Count</h3> </div>
    """

    class Meta:
        name = "equation-count"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    count: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Fax:
    """
    <div> <h3>Fax Number: in an Address</h3> </div>
    """

    class Meta:
        name = "fax"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class FigCount:
    """
    <div> <h3>Figure Count</h3> </div>
    """

    class Meta:
        name = "fig-count"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    count: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


class FigGroupOrientation(Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"


class FigGroupPosition(Enum):
    ANCHOR = "anchor"
    BACKGROUND = "background"
    FLOAT = "float"
    MARGIN = "margin"


class FigOrientation(Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"


class FigPosition(Enum):
    ANCHOR = "anchor"
    BACKGROUND = "background"
    FLOAT = "float"
    MARGIN = "margin"


class FnFnType(Enum):
    ABBR = "abbr"
    COI_STATEMENT = "coi-statement"
    COM = "com"
    CON = "con"
    CONFLICT = "conflict"
    CORRESP = "corresp"
    CURRENT_AFF = "current-aff"
    CUSTOM = "custom"
    DECEASED = "deceased"
    EDITED_BY = "edited-by"
    EQUAL = "equal"
    FINANCIAL_DISCLOSURE = "financial-disclosure"
    ON_LEAVE = "on-leave"
    OTHER = "other"
    PARTICIPATING_RESEARCHERS = "participating-researchers"
    PRESENT_ADDRESS = "present-address"
    PRESENTED_AT = "presented-at"
    PRESENTED_BY = "presented-by"
    PREVIOUSLY_AT = "previously-at"
    STUDY_GROUP_MEMBERS = "study-group-members"
    SUPPLEMENTARY_MATERIAL = "supplementary-material"
    SUPPORTED_BY = "supported-by"


@dataclass
class GivenNames:
    """
    <div> <h3>Given (First) Names</h3> </div>
    """

    class Meta:
        name = "given-names"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    initials: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class GlyphRef:
    """
    <div> <h3>Glyph Reference For a Private Character</h3> </div>
    """

    class Meta:
        name = "glyph-ref"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    glyph_data: Optional[str] = field(
        default=None,
        metadata={
            "name": "glyph-data",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


class GraphicOrientation(Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"


class GraphicPosition(Enum):
    ANCHOR = "anchor"
    BACKGROUND = "background"
    FLOAT = "float"
    MARGIN = "margin"


@dataclass
class Hr:
    """
    <div> <h3>Horizontal Rule</h3> </div>
    """

    class Meta:
        name = "hr"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class IndexTermRangeEnd:
    """
    <div> <h3>Index Term Range End</h3> </div>
    """

    class Meta:
        name = "index-term-range-end"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Isbn:
    """
    <div> <h3>Isbn</h3> </div>
    """

    class Meta:
        name = "isbn"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    publication_format: Optional[str] = field(
        default=None,
        metadata={
            "name": "publication-format",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Issn:
    """
    <div> <h3>Issn</h3> </div>
    """

    class Meta:
        name = "issn"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    pub_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "pub-type",
            "type": "Attribute",
        },
    )
    publication_format: Optional[str] = field(
        default=None,
        metadata={
            "name": "publication-format",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class IssnL:
    """
    <div> <h3>Issn Linking</h3> </div>
    """

    class Meta:
        name = "issn-l"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


class ItalicToggle(Enum):
    NO = "no"
    YES = "yes"


class MediaOrientation(Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"


class MediaPosition(Enum):
    ANCHOR = "anchor"
    BACKGROUND = "background"
    FLOAT = "float"
    MARGIN = "margin"


@dataclass
class MetaName:
    """
    <div> <h3>Metadata Data Name For Custom Metadata</h3> </div>
    """

    class Meta:
        name = "meta-name"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


class MonospaceToggle(Enum):
    NO = "no"
    YES = "yes"


class NameNameStyle(Enum):
    EASTERN = "eastern"
    GIVEN_ONLY = "given-only"
    ISLENSK = "islensk"
    WESTERN = "western"


@dataclass
class ObjectId:
    """
    <div> <h3>Object Identifier</h3> </div>
    """

    class Meta:
        name = "object-id"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    pub_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "pub-id-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


class OptionCorrect(Enum):
    NO = "no"
    YES = "yes"


@dataclass
class OverlineEnd:
    """
    <div> <h3>Overline End</h3> </div>
    """

    class Meta:
        name = "overline-end"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class OverlineStart:
    """
    <div> <h3>Overline Start</h3> </div>
    """

    class Meta:
        name = "overline-start"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


class OverlineToggle(Enum):
    NO = "no"
    YES = "yes"


@dataclass
class PageCount:
    """
    <div> <h3>Page Count</h3> </div>
    """

    class Meta:
        name = "page-count"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    count: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


class PersonGroupPersonGroupType(Enum):
    ALLAUTHORS = "allauthors"
    ASSIGNEE = "assignee"
    AUTHOR = "author"
    COMPILER = "compiler"
    CURATOR = "curator"
    CUSTOM = "custom"
    DIRECTOR = "director"
    EDITOR = "editor"
    GUEST_EDITOR = "guest-editor"
    ILLUSTRATOR = "illustrator"
    INVENTOR = "inventor"
    RESEARCH_ASSISTANT = "research-assistant"
    TRANSED = "transed"
    TRANSLATOR = "translator"


@dataclass
class Phone:
    """
    <div> <h3>Phone Number: in an Address</h3> </div>
    """

    class Meta:
        name = "phone"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


class PreformatOrientation(Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"


class PreformatPosition(Enum):
    ANCHOR = "anchor"
    BACKGROUND = "background"
    FLOAT = "float"
    MARGIN = "margin"


class ProcessingMetaBaseTagset(Enum):
    ARCHIVING = "archiving"
    AUTHORING = "authoring"
    PUBLISHING = "publishing"


class ProcessingMetaMathmlVersion(Enum):
    VALUE_2_0 = "2.0"
    VALUE_3_0 = "3.0"


class ProcessingMetaTableModel(Enum):
    BOTH = "both"
    NONE = "none"
    OASIS = "oasis"
    XHTML = "xhtml"


class ProcessingMetaTagsetFamily(Enum):
    BITS = "bits"
    JATS = "jats"
    STS = "sts"


@dataclass
class PubDateNotAvailable:
    """
    <div> <h3>Date Not Available Flag</h3> </div>
    """

    class Meta:
        name = "pub-date-not-available"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


class PubIdPubIdType(Enum):
    ACCESSION = "accession"
    ARCHIVE = "archive"
    ARK = "ark"
    ART_ACCESS_ID = "art-access-id"
    ARXIV = "arxiv"
    CODEN = "coden"
    CUSTOM = "custom"
    DOAJ = "doaj"
    DOI = "doi"
    HANDLE = "handle"
    INDEX = "index"
    ISBN = "isbn"
    MANUSCRIPT = "manuscript"
    MEDLINE = "medline"
    MR = "mr"
    OTHER = "other"
    PII = "pii"
    PMCID = "pmcid"
    PMID = "pmid"
    PUBLISHER_ID = "publisher-id"
    SICI = "sici"
    STD_DESIGNATION = "std-designation"
    ZBL = "zbl"


class QuestionQuestionResponseType(Enum):
    ESSAY = "essay"
    FILL_IN_THE_BLANK = "fill-in-the-blank"
    MULTI_SELECT = "multi-select"
    MULTIPLE_CHOICE = "multiple-choice"
    SHORT_ANSWER = "short-answer"
    TRUE_FALSE = "true-false"


@dataclass
class RefCount:
    """
    <div> <h3>Reference Count</h3> </div>
    """

    class Meta:
        name = "ref-count"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    count: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


class RomanToggle(Enum):
    NO = "no"
    YES = "yes"


@dataclass
class Rp:
    """
    <div> <h3>Ruby Parenthesis</h3> </div>
    """

    class Meta:
        name = "rp"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


class SansSerifToggle(Enum):
    NO = "no"
    YES = "yes"


class ScToggle(Enum):
    NO = "no"
    YES = "yes"


class StrikeToggle(Enum):
    NO = "no"
    YES = "yes"


class StringNameNameStyle(Enum):
    EASTERN = "eastern"
    GIVEN_ONLY = "given-only"
    ISLENSK = "islensk"
    WESTERN = "western"


class StyledContentToggle(Enum):
    NO = "no"
    YES = "yes"


class SubArrange(Enum):
    STACK = "stack"
    STAGGER = "stagger"


class SupArrange(Enum):
    STACK = "stack"
    STAGGER = "stagger"


class SupplementaryMaterialOrientation(Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"


class SupplementaryMaterialPosition(Enum):
    ANCHOR = "anchor"
    BACKGROUND = "background"
    FLOAT = "float"
    MARGIN = "margin"


@dataclass
class Surname:
    """
    <div> <h3>Surname</h3> </div>
    """

    class Meta:
        name = "surname"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    initials: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class TableCount:
    """
    <div> <h3>Table Count</h3> </div>
    """

    class Meta:
        name = "table-count"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    count: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


class TableWrapGroupOrientation(Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"


class TableWrapGroupPosition(Enum):
    ANCHOR = "anchor"
    BACKGROUND = "background"
    FLOAT = "float"
    MARGIN = "margin"


class TableWrapOrientation(Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"


class TableWrapPosition(Enum):
    ANCHOR = "anchor"
    BACKGROUND = "background"
    FLOAT = "float"
    MARGIN = "margin"


class TableFrame(Enum):
    ABOVE = "above"
    BELOW = "below"
    BORDER = "border"
    BOX = "box"
    HSIDES = "hsides"
    LHS = "lhs"
    RHS = "rhs"
    VOID = "void"
    VSIDES = "vsides"


class TableRules(Enum):
    ALL = "all"
    COLS = "cols"
    GROUPS = "groups"
    NONE = "none"
    ROWS = "rows"


class TbodyAlign(Enum):
    CENTER = "center"
    CHAR = "char"
    JUSTIFY = "justify"
    LEFT = "left"
    RIGHT = "right"


class TbodyValign(Enum):
    BASELINE = "baseline"
    BOTTOM = "bottom"
    MIDDLE = "middle"
    TOP = "top"


class TdAlign(Enum):
    CENTER = "center"
    CHAR = "char"
    JUSTIFY = "justify"
    LEFT = "left"
    RIGHT = "right"


class TdScope(Enum):
    COL = "col"
    COLGROUP = "colgroup"
    ROW = "row"
    ROWGROUP = "rowgroup"


class TdValign(Enum):
    BASELINE = "baseline"
    BOTTOM = "bottom"
    MIDDLE = "middle"
    TOP = "top"


class TexMathNotation(Enum):
    LA_TE_X = "LaTeX"
    TEX = "TEX"
    TE_X_1 = "TeX"
    TEX_2 = "tex"


class TfootAlign(Enum):
    CENTER = "center"
    CHAR = "char"
    JUSTIFY = "justify"
    LEFT = "left"
    RIGHT = "right"


class TfootValign(Enum):
    BASELINE = "baseline"
    BOTTOM = "bottom"
    MIDDLE = "middle"
    TOP = "top"


class ThAlign(Enum):
    CENTER = "center"
    CHAR = "char"
    JUSTIFY = "justify"
    LEFT = "left"
    RIGHT = "right"


class ThScope(Enum):
    COL = "col"
    COLGROUP = "colgroup"
    ROW = "row"
    ROWGROUP = "rowgroup"


class ThValign(Enum):
    BASELINE = "baseline"
    BOTTOM = "bottom"
    MIDDLE = "middle"
    TOP = "top"


class TheadAlign(Enum):
    CENTER = "center"
    CHAR = "char"
    JUSTIFY = "justify"
    LEFT = "left"
    RIGHT = "right"


class TheadValign(Enum):
    BASELINE = "baseline"
    BOTTOM = "bottom"
    MIDDLE = "middle"
    TOP = "top"


@dataclass
class TimeStamp:
    """
    <div> <h3>Time Stamp For Cited Work</h3> </div>
    """

    class Meta:
        name = "time-stamp"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


class TrAlign(Enum):
    CENTER = "center"
    CHAR = "char"
    JUSTIFY = "justify"
    LEFT = "left"
    RIGHT = "right"


class TrValign(Enum):
    BASELINE = "baseline"
    BOTTOM = "bottom"
    MIDDLE = "middle"
    TOP = "top"


@dataclass
class UnderlineEnd:
    """
    <div> <h3>Underline End</h3> </div>
    """

    class Meta:
        name = "underline-end"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class UnderlineStart:
    """
    <div> <h3>Underline Start</h3> </div>
    """

    class Meta:
        name = "underline-start"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


class UnderlineToggle(Enum):
    NO = "no"
    YES = "yes"


@dataclass
class WordCount:
    """
    <div> <h3>Word Count</h3> </div>
    """

    class Meta:
        name = "word-count"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    count: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


class XrefRefType(Enum):
    AFF = "aff"
    APP = "app"
    AUTHOR_NOTES = "author-notes"
    AWARD = "award"
    BIBR = "bibr"
    BIO = "bio"
    BOXED_TEXT = "boxed-text"
    CHEM = "chem"
    COLLAB = "collab"
    CONTRIB = "contrib"
    CORRESP = "corresp"
    CUSTOM = "custom"
    DISP_FORMULA = "disp-formula"
    FIG = "fig"
    FN = "fn"
    KWD = "kwd"
    LIST = "list"
    OTHER = "other"
    PLATE = "plate"
    SCHEME = "scheme"
    SEC = "sec"
    STATEMENT = "statement"
    SUPPLEMENTARY_MATERIAL = "supplementary-material"
    TABLE = "table"
    TABLE_FN = "table-fn"


@dataclass
class Abbrev:
    """
    <div> <h3>Abbreviation or Acronym</h3> </div>
    """

    class Meta:
        name = "abbrev"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    alt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "def",
                    "type": ForwardRef("Def"),
                },
            ),
        },
    )


@dataclass
class AbbrevJournalTitle:
    """
    <div> <h3>Abbreviated Journal Title</h3> </div>
    """

    class Meta:
        name = "abbrev-journal-title"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    abbrev_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "abbrev-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Abstract:
    """
    <div> <h3>Abstract</h3> </div>
    """

    class Meta:
        name = "abstract"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: Optional["Label"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    sec: list["Sec"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    abstract_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "abstract-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class AltText:
    """
    <div> <h3>Alternate Title Text For a Figure, Etc.</h3> </div>
    """

    class Meta:
        name = "alt-text"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Annotation:
    """
    <div> <h3>Annotation in a Citation</h3> </div>
    """

    class Meta:
        name = "annotation"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Anonymous:
    """
    <div> <h3>Anonymous</h3> </div>
    """

    class Meta:
        name = "anonymous"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class ArticleId:
    """
    <div> <h3>Article Identifier</h3> </div>
    """

    class Meta:
        name = "article-id"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    custom_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "custom-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    pub_id_type: Optional[ArticleIdPubIdType] = field(
        default=None,
        metadata={
            "name": "pub-id-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class ArticleVersion:
    """
    <div> <h3>Article Version</h3> </div>
    """

    class Meta:
        name = "article-version"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    article_version_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "article-version-type",
            "type": "Attribute",
        },
    )
    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    designator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    iso_8601_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "iso-8601-date",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    vocab_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term",
            "type": "Attribute",
        },
    )
    vocab_term_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term-identifier",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class AuthorComment:
    """
    <div> <h3>Author Comment</h3> </div>
    """

    class Meta:
        name = "author-comment"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class AwardDesc:
    """
    <div> <h3>Award Description</h3> </div>
    """

    class Meta:
        name = "award-desc"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class AwardName:
    """
    <div> <h3>Award Name</h3> </div>
    """

    class Meta:
        name = "award-name"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class BlockAlternatives:
    """
    <div> <h3>Block-Level Alternatives For Processing</h3> </div>
    """

    class Meta:
        name = "block-alternatives"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    boxed_text: list["BoxedText"] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    fig: list["Fig"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list["FigGroup"] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    table_wrap: list["TableWrap"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list["TableWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Caption:
    """
    <div> <h3>Caption of a Figure, Table, Etc.</h3> </div>
    """

    class Meta:
        name = "caption"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class CitationAlternatives:
    """
    <div> <h3>Citation Alternatives</h3> </div>
    """

    class Meta:
        name = "citation-alternatives"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    element_citation: list["ElementCitation"] = field(
        default_factory=list,
        metadata={
            "name": "element-citation",
            "type": "Element",
        },
    )
    mixed_citation: list["MixedCitation"] = field(
        default_factory=list,
        metadata={
            "name": "mixed-citation",
            "type": "Element",
        },
    )
    nlm_citation: list["NlmCitation"] = field(
        default_factory=list,
        metadata={
            "name": "nlm-citation",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class City:
    """
    <div> <h3>City: in an Address</h3> </div>
    """

    class Meta:
        name = "city"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Col:
    class Meta:
        name = "col"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    align: Optional[ColAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    span: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    valign: Optional[ColValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class ConfAcronym:
    """
    <div> <h3>Conference Acronym</h3> </div>
    """

    class Meta:
        name = "conf-acronym"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class ConfDate:
    """
    <div> <h3>Conference Date</h3> </div>
    """

    class Meta:
        name = "conf-date"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    calendar: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    iso_8601_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "iso-8601-date",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class ConfName:
    """
    <div> <h3>Conference Name</h3> </div>
    """

    class Meta:
        name = "conf-name"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class ConfNum:
    """
    <div> <h3>Conference Number</h3> </div>
    """

    class Meta:
        name = "conf-num"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class ConfSponsor:
    """
    <div> <h3>Conference Sponsor</h3> </div>
    """

    class Meta:
        name = "conf-sponsor"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "institution",
                    "type": ForwardRef("Institution"),
                },
                {
                    "name": "institution-wrap",
                    "type": ForwardRef("InstitutionWrap"),
                },
            ),
        },
    )


@dataclass
class ContribId:
    """
    <div> <h3>Contributor Identifier</h3> </div>
    """

    class Meta:
        name = "contrib-id"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    authenticated: ContribIdAuthenticated = field(
        default=ContribIdAuthenticated.FALSE,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    contrib_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "contrib-id-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class CopyrightHolder:
    """
    <div> <h3>Copyright Holder</h3> </div>
    """

    class Meta:
        name = "copyright-holder"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "institution",
                    "type": ForwardRef("Institution"),
                },
                {
                    "name": "institution-wrap",
                    "type": ForwardRef("InstitutionWrap"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class Country:
    """
    <div> <h3>Country: in an Address</h3> </div>
    """

    class Meta:
        name = "country"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    country: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Counts:
    """
    <div> <h3>Counts</h3> </div>
    """

    class Meta:
        name = "counts"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    count: list[Count] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_count: Optional[FigCount] = field(
        default=None,
        metadata={
            "name": "fig-count",
            "type": "Element",
        },
    )
    table_count: Optional[TableCount] = field(
        default=None,
        metadata={
            "name": "table-count",
            "type": "Element",
        },
    )
    equation_count: Optional[EquationCount] = field(
        default=None,
        metadata={
            "name": "equation-count",
            "type": "Element",
        },
    )
    ref_count: Optional[RefCount] = field(
        default=None,
        metadata={
            "name": "ref-count",
            "type": "Element",
        },
    )
    page_count: Optional[PageCount] = field(
        default=None,
        metadata={
            "name": "page-count",
            "type": "Element",
        },
    )
    word_count: Optional[WordCount] = field(
        default=None,
        metadata={
            "name": "word-count",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Day:
    """
    <div> <h3>Day</h3> </div>
    """

    class Meta:
        name = "day"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Def:
    """
    <div> <h3>Definition List: Definition</h3> </div>
    """

    class Meta:
        name = "def"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Degrees:
    """
    <div> <h3>Degree(s)</h3> </div>
    """

    class Meta:
        name = "degrees"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Edition:
    """
    <div> <h3>Edition Statement, Cited</h3> </div>
    """

    class Meta:
        name = "edition"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    designator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class Email:
    """
    <div> <h3>Email Address</h3> </div>
    """

    class Meta:
        name = "email"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Era:
    """
    <div> <h3>Era</h3> </div>
    """

    class Meta:
        name = "era"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Etal:
    """
    <div> <h3>Et Al</h3> </div>
    """

    class Meta:
        name = "etal"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class ExtendedBy:
    """
    <div> <h3>Extended-by Model</h3> </div>
    """

    class Meta:
        name = "extended-by"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    designator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    vocab_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term",
            "type": "Attribute",
        },
    )
    vocab_term_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term-identifier",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Fn:
    """
    <div> <h3>Footnote</h3> </div>
    """

    class Meta:
        name = "fn"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    label: Optional["Label"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    custom_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "custom-type",
            "type": "Attribute",
        },
    )
    fn_type: Optional[FnFnType] = field(
        default=None,
        metadata={
            "name": "fn-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    symbol: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Fpage:
    """
    <div> <h3>First Page</h3> </div>
    """

    class Meta:
        name = "fpage"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    seq: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class GlyphData:
    """
    <div> <h3>Glyph Data For a Private Character</h3> </div>
    """

    class Meta:
        name = "glyph-data"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    fontchar: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    fontname: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    format: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    resolution: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    x_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "x-size",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: SpaceValue = field(
        init=False,
        default=SpaceValue.PRESERVE,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    y_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "y-size",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class IndexTerm:
    """
    <div> <h3>Index Term</h3> </div>
    """

    class Meta:
        name = "index-term"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    term: Optional["Term"] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    index_term: Optional["IndexTerm"] = field(
        default=None,
        metadata={
            "name": "index-term",
            "type": "Element",
        },
    )
    see: list["See"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    see_also: list["SeeAlso"] = field(
        default_factory=list,
        metadata={
            "name": "see-also",
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    index_type: list[str] = field(
        default_factory=list,
        metadata={
            "name": "index-type",
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    vocab_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term",
            "type": "Attribute",
        },
    )
    vocab_term_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term-identifier",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Institution:
    """
    <div> <h3>Institution Name: in an Address</h3> </div>
    """

    class Meta:
        name = "institution"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class InstitutionId:
    """
    <div> <h3>Institution Identifier</h3> </div>
    """

    class Meta:
        name = "institution-id"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    institution_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "institution-id-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Issue:
    """
    <div> <h3>Issue Number</h3> </div>
    """

    class Meta:
        name = "issue"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    seq: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class IssueId:
    """
    <div> <h3>Issue Identifier</h3> </div>
    """

    class Meta:
        name = "issue-id"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    pub_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "pub-id-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class IssuePart:
    """
    <div> <h3>Issue Part</h3> </div>
    """

    class Meta:
        name = "issue-part"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class IssueSponsor:
    """
    <div> <h3>Issue Title</h3> </div>
    """

    class Meta:
        name = "issue-sponsor"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class IssueSubtitle:
    """
    <div> <h3>Issue Subtitle</h3> </div>
    """

    class Meta:
        name = "issue-subtitle"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class IssueTitle:
    """
    <div> <h3>Issue Title</h3> </div>
    """

    class Meta:
        name = "issue-title"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class JournalId:
    """
    <div> <h3>Journal Identifier</h3> </div>
    """

    class Meta:
        name = "journal-id"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    journal_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "journal-id-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class JournalSubtitle:
    """
    <div> <h3>Journal Subtitle</h3> </div>
    """

    class Meta:
        name = "journal-subtitle"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class JournalTitle:
    """
    <div> <h3>Journal Title (Full)</h3> </div>
    """

    class Meta:
        name = "journal-title"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class License:
    """
    <div> <h3>License Information</h3> </div>
    """

    class Meta:
        name = "license"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    license_ref: list[LicenseRef] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.niso.org/schemas/ali/1.0/",
        },
    )
    license_p: list["LicenseP"] = field(
        default_factory=list,
        metadata={
            "name": "license-p",
            "type": "Element",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    license_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "license-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class LongDesc:
    """
    <div> <h3>Long Description</h3> </div>
    """

    class Meta:
        name = "long-desc"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Lpage:
    """
    <div> <h3>Last Page</h3> </div>
    """

    class Meta:
        name = "lpage"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class MilestoneEnd:
    """
    <div> <h3>Milestone End</h3> </div>
    """

    class Meta:
        name = "milestone-end"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rationale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class MilestoneStart:
    """
    <div> <h3>Milestone Start</h3> </div>
    """

    class Meta:
        name = "milestone-start"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rationale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Month:
    """
    <div> <h3>Month</h3> </div>
    """

    class Meta:
        name = "month"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class OpenAccess:
    """
    <div> <h3>Open Access</h3> </div>
    """

    class Meta:
        name = "open-access"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class PageRange:
    """
    <div> <h3>Page Ranges</h3> </div>
    """

    class Meta:
        name = "page-range"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Patent:
    """
    <div> <h3>Patent Number, Cited</h3> </div>
    """

    class Meta:
        name = "patent"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    country: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class PostalCode:
    """
    <div> <h3>Postal Code: in an Address</h3> </div>
    """

    class Meta:
        name = "postal-code"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Prefix:
    """
    <div> <h3>Prefix</h3> </div>
    """

    class Meta:
        name = "prefix"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class PubId:
    """
    <div> <h3>Publication Identifier For a Cited Publication</h3> </div>
    """

    class Meta:
        name = "pub-id"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    custom_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "custom-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    pub_id_type: Optional[PubIdPubIdType] = field(
        default=None,
        metadata={
            "name": "pub-id-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class ResourceId:
    """
    <div> <h3>Resource Identifier</h3> </div>
    """

    class Meta:
        name = "resource-id"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    resource_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "resource-id-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class RestrictedBy:
    """
    <div> <h3>Restricted-by Model</h3> </div>
    """

    class Meta:
        name = "restricted-by"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    designator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    vocab_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term",
            "type": "Attribute",
        },
    )
    vocab_term_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term-identifier",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Rt:
    """
    <div> <h3>Ruby Textual Annotation</h3> </div>
    """

    class Meta:
        name = "rt"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Season:
    """
    <div> <h3>Season</h3> </div>
    """

    class Meta:
        name = "season"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class SelfUri:
    """
    <div> <h3>Uri For This Same Article Online</h3> </div>
    """

    class Meta:
        name = "self-uri"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Size:
    """
    <div> <h3>Size</h3> </div>
    """

    class Meta:
        name = "size"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    units: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class State:
    """
    <div> <h3>State or Province: in an Address</h3> </div>
    """

    class Meta:
        name = "state"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Suffix:
    """
    <div> <h3>Suffix</h3> </div>
    """

    class Meta:
        name = "suffix"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class TexMath:
    """
    <div> <h3>Tex Math Equation</h3> </div>
    """

    class Meta:
        name = "tex-math"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    notation: Optional[TexMathNotation] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class UnstructuredKwdGroup:
    """
    <div> <h3>Unstructured Keyword Group</h3> </div>
    """

    class Meta:
        name = "unstructured-kwd-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    kwd_group_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "kwd-group-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Uri:
    """
    <div> <h3>Uri</h3> </div>
    """

    class Meta:
        name = "uri"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Volume:
    """
    <div> <h3>Volume Number</h3> </div>
    """

    class Meta:
        name = "volume"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    seq: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class VolumeId:
    """
    <div> <h3>Volume Identifier</h3> </div>
    """

    class Meta:
        name = "volume-id"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    pub_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "pub-id-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class VolumeSeries:
    """
    <div> <h3>Volume Series</h3> </div>
    """

    class Meta:
        name = "volume-series"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class X:
    """<div>
    <h3>X - Generated Text and Punctuation</h3>
    </div>"""

    class Meta:
        name = "x"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: SpaceValue = field(
        init=False,
        default=SpaceValue.PRESERVE,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Year:
    """
    <div> <h3>Year</h3> </div>
    """

    class Meta:
        name = "year"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    calendar: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    iso_8601_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "iso-8601-date",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class ArticleVersionAlternatives:
    """
    <div> <h3>Article Version Alternatives</h3> </div>
    """

    class Meta:
        name = "article-version-alternatives"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    article_version: list[ArticleVersion] = field(
        default_factory=list,
        metadata={
            "name": "article-version",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Colgroup:
    class Meta:
        name = "colgroup"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    col: list[Col] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    align: Optional[ColgroupAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    span: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    valign: Optional[ColgroupValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Date:
    """
    <div> <h3>Date</h3> </div>
    """

    class Meta:
        name = "date"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    day: Optional[Day] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    month: Optional[Month] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    season: Optional[Season] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    year: Optional[Year] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    era: Optional[Era] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    calendar: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    date_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "date-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    iso_8601_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "iso-8601-date",
            "type": "Attribute",
        },
    )
    publication_format: Optional[str] = field(
        default=None,
        metadata={
            "name": "publication-format",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class DateInCitation:
    """
    <div> <h3>Date Inside Citation</h3> </div>
    """

    class Meta:
        name = "date-in-citation"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    calendar: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    iso_8601_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "iso-8601-date",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "day",
                    "type": Day,
                },
                {
                    "name": "era",
                    "type": Era,
                },
                {
                    "name": "month",
                    "type": Month,
                },
                {
                    "name": "season",
                    "type": Season,
                },
                {
                    "name": "year",
                    "type": Year,
                },
            ),
        },
    )


@dataclass
class DefItem:
    """
    <div> <h3>Definition List: Definition Item</h3> </div>
    """

    class Meta:
        name = "def-item"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    term: Optional["Term"] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    def_value: list[Def] = field(
        default_factory=list,
        metadata={
            "name": "def",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class FnGroup:
    """
    <div> <h3>Footnote Group</h3> </div>
    """

    class Meta:
        name = "fn-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    label: Optional["Label"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    fn: list[Fn] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class InlineGraphic:
    """
    <div> <h3>Inline Graphic</h3> </div>
    """

    class Meta:
        name = "inline-graphic"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    alt_text: list[AltText] = field(
        default_factory=list,
        metadata={
            "name": "alt-text",
            "type": "Element",
        },
    )
    long_desc: list[LongDesc] = field(
        default_factory=list,
        metadata={
            "name": "long-desc",
            "type": "Element",
        },
    )
    baseline_shift: Optional[str] = field(
        default=None,
        metadata={
            "name": "baseline-shift",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    mime_subtype: Optional[str] = field(
        default=None,
        metadata={
            "name": "mime-subtype",
            "type": "Attribute",
        },
    )
    mimetype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "required": True,
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class InstitutionWrap:
    """
    <div> <h3>Institution Wrapper</h3> </div>
    """

    class Meta:
        name = "institution-wrap"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    institution: list[Institution] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    institution_id: list[InstitutionId] = field(
        default_factory=list,
        metadata={
            "name": "institution-id",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Name:
    """
    <div> <h3>Name of Person (Structured)</h3> </div>
    """

    class Meta:
        name = "name"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    surname: Optional[Surname] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    given_names: list[GivenNames] = field(
        default_factory=list,
        metadata={
            "name": "given-names",
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    prefix: Optional[Prefix] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    suffix: Optional[Suffix] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name_style: NameNameStyle = field(
        default=NameNameStyle.WESTERN,
        metadata={
            "name": "name-style",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class PubDate:
    """
    <div> <h3>Publication Date</h3> </div>
    """

    class Meta:
        name = "pub-date"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    day: Optional[Day] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    month: Optional[Month] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    season: Optional[Season] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    year: Optional[Year] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    era: Optional[Era] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    calendar: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    date_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "date-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    iso_8601_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "iso-8601-date",
            "type": "Attribute",
        },
    )
    pub_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "pub-type",
            "type": "Attribute",
        },
    )
    publication_format: Optional[str] = field(
        default=None,
        metadata={
            "name": "publication-format",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Speaker:
    """
    <div> <h3>Speaker</h3> </div>
    """

    class Meta:
        name = "speaker"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "degrees",
                    "type": Degrees,
                },
                {
                    "name": "given-names",
                    "type": GivenNames,
                },
                {
                    "name": "prefix",
                    "type": Prefix,
                },
                {
                    "name": "surname",
                    "type": Surname,
                },
                {
                    "name": "suffix",
                    "type": Suffix,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
            ),
        },
    )


@dataclass
class StringDate:
    """
    <div> <h3>Date As a String</h3> </div>
    """

    class Meta:
        name = "string-date"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    calendar: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    iso_8601_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "iso-8601-date",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "day",
                    "type": Day,
                },
                {
                    "name": "era",
                    "type": Era,
                },
                {
                    "name": "month",
                    "type": Month,
                },
                {
                    "name": "season",
                    "type": Season,
                },
                {
                    "name": "year",
                    "type": Year,
                },
            ),
        },
    )


@dataclass
class StringName:
    """
    <div> <h3>Name of Person (Unstructured)</h3> </div>
    """

    class Meta:
        name = "string-name"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name_style: StringNameNameStyle = field(
        default=StringNameNameStyle.WESTERN,
        metadata={
            "name": "name-style",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "degrees",
                    "type": Degrees,
                },
                {
                    "name": "given-names",
                    "type": GivenNames,
                },
                {
                    "name": "prefix",
                    "type": Prefix,
                },
                {
                    "name": "surname",
                    "type": Surname,
                },
                {
                    "name": "suffix",
                    "type": Suffix,
                },
            ),
        },
    )


@dataclass
class History:
    """
    <div> <h3>History: Document History</h3> </div>
    """

    class Meta:
        name = "history"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    date: list[Date] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class NameAlternatives:
    """
    <div> <h3>Name Alternatives</h3> </div>
    """

    class Meta:
        name = "name-alternatives"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    name: list[Name] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    string_name: list[StringName] = field(
        default_factory=list,
        metadata={
            "name": "string-name",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class PrivateChar:
    """
    <div> <h3>Private Character (Custom or Unicode)</h3> </div>
    """

    class Meta:
        name = "private-char"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    glyph_data: Optional[GlyphData] = field(
        default=None,
        metadata={
            "name": "glyph-data",
            "type": "Element",
        },
    )
    glyph_ref: Optional[GlyphRef] = field(
        default=None,
        metadata={
            "name": "glyph-ref",
            "type": "Element",
        },
    )
    inline_graphic: list[InlineGraphic] = field(
        default_factory=list,
        metadata={
            "name": "inline-graphic",
            "type": "Element",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class PublisherName:
    """
    <div> <h3>Publisher's Name</h3> </div>
    """

    class Meta:
        name = "publisher-name"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "institution",
                    "type": Institution,
                },
                {
                    "name": "institution-wrap",
                    "type": InstitutionWrap,
                },
            ),
        },
    )


@dataclass
class AddrLine:
    """
    <div> <h3>Address Line</h3> </div>
    """

    class Meta:
        name = "addr-line"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": ForwardRef("Bold"),
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": ForwardRef("Alternatives"),
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ForwardRef("ChemStruct"),
                },
                {
                    "name": "inline-formula",
                    "type": ForwardRef("InlineFormula"),
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": ForwardRef("IndexTerm"),
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
                {
                    "name": "city",
                    "type": City,
                },
                {
                    "name": "country",
                    "type": Country,
                },
                {
                    "name": "fax",
                    "type": Fax,
                },
                {
                    "name": "institution",
                    "type": ForwardRef("Institution"),
                },
                {
                    "name": "institution-wrap",
                    "type": ForwardRef("InstitutionWrap"),
                },
                {
                    "name": "phone",
                    "type": Phone,
                },
                {
                    "name": "postal-code",
                    "type": PostalCode,
                },
                {
                    "name": "state",
                    "type": State,
                },
            ),
        },
    )


@dataclass
class AltTitle:
    """
    <div> <h3>Alternate Title</h3> </div>
    """

    class Meta:
        name = "alt-title"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    alt_title_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "alt-title-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ForwardRef("ExtLink"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": ForwardRef("InlineSupplementaryMaterial"),
                },
                {
                    "name": "related-article",
                    "type": ForwardRef("RelatedArticle"),
                },
                {
                    "name": "related-object",
                    "type": ForwardRef("RelatedObject"),
                },
                {
                    "name": "bold",
                    "type": ForwardRef("Bold"),
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": ForwardRef("Alternatives"),
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ForwardRef("ChemStruct"),
                },
                {
                    "name": "inline-formula",
                    "type": ForwardRef("InlineFormula"),
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": ForwardRef("IndexTerm"),
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": ForwardRef("Fn"),
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
                {
                    "name": "break",
                    "type": Break,
                },
            ),
        },
    )


@dataclass
class Alternatives:
    """
    <div> <h3>Alternatives For Processing</h3> </div>
    """

    class Meta:
        name = "alternatives"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    array: list["Array"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    chem_struct: list["ChemStruct"] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct",
            "type": "Element",
        },
    )
    code: list["Code"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    graphic: list["Graphic"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    inline_graphic: list[InlineGraphic] = field(
        default_factory=list,
        metadata={
            "name": "inline-graphic",
            "type": "Element",
        },
    )
    inline_media: list["InlineMedia"] = field(
        default_factory=list,
        metadata={
            "name": "inline-media",
            "type": "Element",
        },
    )
    inline_supplementary_material: list["InlineSupplementaryMaterial"] = field(
        default_factory=list,
        metadata={
            "name": "inline-supplementary-material",
            "type": "Element",
        },
    )
    media: list["Media"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list["Preformat"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    private_char: list[PrivateChar] = field(
        default_factory=list,
        metadata={
            "name": "private-char",
            "type": "Element",
        },
    )
    supplementary_material: list["SupplementaryMaterial"] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table: list["Table"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    textual_form: list["TextualForm"] = field(
        default_factory=list,
        metadata={
            "name": "textual-form",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class PrincipalAwardRecipient:
    """
    <div> <h3>Principal Award Recipient</h3> </div>
    """

    class Meta:
        name = "principal-award-recipient"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "contrib-id",
                    "type": ContribId,
                },
                {
                    "name": "name",
                    "type": Name,
                },
                {
                    "name": "name-alternatives",
                    "type": NameAlternatives,
                },
                {
                    "name": "institution",
                    "type": Institution,
                },
                {
                    "name": "institution-wrap",
                    "type": InstitutionWrap,
                },
                {
                    "name": "string-name",
                    "type": StringName,
                },
            ),
        },
    )


@dataclass
class PrincipalInvestigator:
    """
    <div> <h3>Principal Investigator Recipient</h3> </div>
    """

    class Meta:
        name = "principal-investigator"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "contrib-id",
                    "type": ContribId,
                },
                {
                    "name": "name",
                    "type": Name,
                },
                {
                    "name": "name-alternatives",
                    "type": NameAlternatives,
                },
                {
                    "name": "string-name",
                    "type": StringName,
                },
            ),
        },
    )


@dataclass
class Address:
    """
    <div> <h3>Address/Contact Information</h3> </div>
    """

    class Meta:
        name = "address"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    addr_line: list[AddrLine] = field(
        default_factory=list,
        metadata={
            "name": "addr-line",
            "type": "Element",
        },
    )
    city: list[City] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    country: list[Country] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fax: list[Fax] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    institution: list["Institution"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    institution_wrap: list["InstitutionWrap"] = field(
        default_factory=list,
        metadata={
            "name": "institution-wrap",
            "type": "Element",
        },
    )
    phone: list[Phone] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    postal_code: list[PostalCode] = field(
        default_factory=list,
        metadata={
            "name": "postal-code",
            "type": "Element",
        },
    )
    state: list[State] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list["ExtLink"] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Aff:
    """
    <div> <h3>Affiliation</h3> </div>
    """

    class Meta:
        name = "aff"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "addr-line",
                    "type": AddrLine,
                },
                {
                    "name": "city",
                    "type": City,
                },
                {
                    "name": "country",
                    "type": Country,
                },
                {
                    "name": "fax",
                    "type": Fax,
                },
                {
                    "name": "institution",
                    "type": ForwardRef("Institution"),
                },
                {
                    "name": "institution-wrap",
                    "type": ForwardRef("InstitutionWrap"),
                },
                {
                    "name": "phone",
                    "type": Phone,
                },
                {
                    "name": "postal-code",
                    "type": PostalCode,
                },
                {
                    "name": "state",
                    "type": State,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ForwardRef("ExtLink"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": ForwardRef("InlineSupplementaryMaterial"),
                },
                {
                    "name": "related-article",
                    "type": ForwardRef("RelatedArticle"),
                },
                {
                    "name": "related-object",
                    "type": ForwardRef("RelatedObject"),
                },
                {
                    "name": "break",
                    "type": Break,
                },
                {
                    "name": "bold",
                    "type": ForwardRef("Bold"),
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "label",
                    "type": ForwardRef("Label"),
                },
                {
                    "name": "fn",
                    "type": ForwardRef("Fn"),
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class Array:
    """
    <div> <h3>Array (Simple Tabular Array)</h3> </div>
    """

    class Meta:
        name = "array"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    alt_text: list[AltText] = field(
        default_factory=list,
        metadata={
            "name": "alt-text",
            "type": "Element",
        },
    )
    long_desc: list[LongDesc] = field(
        default_factory=list,
        metadata={
            "name": "long-desc",
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list["ExtLink"] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    graphic: list["Graphic"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list["Media"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    tbody: Optional["Tbody"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    attrib: list["Attrib"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    permissions: list["Permissions"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    orientation: ArrayOrientation = field(
        default=ArrayOrientation.PORTRAIT,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class ArticleTitle:
    """
    <div> <h3>Article Title</h3> </div>
    """

    class Meta:
        name = "article-title"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ForwardRef("ExtLink"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": ForwardRef("InlineSupplementaryMaterial"),
                },
                {
                    "name": "related-article",
                    "type": ForwardRef("RelatedArticle"),
                },
                {
                    "name": "related-object",
                    "type": ForwardRef("RelatedObject"),
                },
                {
                    "name": "bold",
                    "type": ForwardRef("Bold"),
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ForwardRef("ChemStruct"),
                },
                {
                    "name": "inline-formula",
                    "type": ForwardRef("InlineFormula"),
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": ForwardRef("IndexTerm"),
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": ForwardRef("Fn"),
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
                {
                    "name": "break",
                    "type": Break,
                },
            ),
        },
    )


@dataclass
class Attrib:
    """
    <div> <h3>Attribution</h3> </div>
    """

    class Meta:
        name = "attrib"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ForwardRef("ExtLink"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": ForwardRef("InlineSupplementaryMaterial"),
                },
                {
                    "name": "related-article",
                    "type": ForwardRef("RelatedArticle"),
                },
                {
                    "name": "related-object",
                    "type": ForwardRef("RelatedObject"),
                },
                {
                    "name": "bold",
                    "type": ForwardRef("Bold"),
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ForwardRef("ChemStruct"),
                },
                {
                    "name": "inline-formula",
                    "type": ForwardRef("InlineFormula"),
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": ForwardRef("IndexTerm"),
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": ForwardRef("Fn"),
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class AwardId:
    """
    <div> <h3>Award Identifier</h3> </div>
    """

    class Meta:
        name = "award-id"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    award_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "award-id-type",
            "type": "Attribute",
        },
    )
    award_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "award-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": ForwardRef("Bold"),
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ForwardRef("ChemStruct"),
                },
                {
                    "name": "inline-formula",
                    "type": ForwardRef("InlineFormula"),
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": ForwardRef("IndexTerm"),
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class Bold:
    """
    <div> <h3>Bold</h3> </div>
    """

    class Meta:
        name = "bold"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    toggle: Optional[BoldToggle] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ForwardRef("ExtLink"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": ForwardRef("InlineSupplementaryMaterial"),
                },
                {
                    "name": "related-article",
                    "type": ForwardRef("RelatedArticle"),
                },
                {
                    "name": "related-object",
                    "type": ForwardRef("RelatedObject"),
                },
                {
                    "name": "bold",
                    "type": ForwardRef("Bold"),
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ForwardRef("ChemStruct"),
                },
                {
                    "name": "inline-formula",
                    "type": ForwardRef("InlineFormula"),
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": ForwardRef("IndexTerm"),
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": ForwardRef("Fn"),
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class ConfLoc:
    """
    <div> <h3>Conference Location</h3> </div>
    """

    class Meta:
        name = "conf-loc"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "addr-line",
                    "type": AddrLine,
                },
                {
                    "name": "city",
                    "type": City,
                },
                {
                    "name": "country",
                    "type": Country,
                },
                {
                    "name": "fax",
                    "type": Fax,
                },
                {
                    "name": "institution",
                    "type": ForwardRef("Institution"),
                },
                {
                    "name": "institution-wrap",
                    "type": ForwardRef("InstitutionWrap"),
                },
                {
                    "name": "phone",
                    "type": Phone,
                },
                {
                    "name": "postal-code",
                    "type": PostalCode,
                },
                {
                    "name": "state",
                    "type": State,
                },
            ),
        },
    )


@dataclass
class AffAlternatives:
    """
    <div> <h3>Affiliation Alternatives</h3> </div>
    """

    class Meta:
        name = "aff-alternatives"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    aff: list[Aff] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Answer:
    """
    <div> <h3>Answer Elements</h3> </div>
    """

    class Meta:
        name = "answer"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: Optional["Label"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    subtitle: list["Subtitle"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alt_title: list[AltTitle] = field(
        default_factory=list,
        metadata={
            "name": "alt-title",
            "type": "Element",
        },
    )
    sec: list["Sec"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer: list["Answer"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer_set: list["AnswerSet"] = field(
        default_factory=list,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    array: list["Array"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list["BlockAlternatives"] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list["BoxedText"] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list["ChemStructWrap"] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list["Code"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list["Fig"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list["FigGroup"] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list["Graphic"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list["Media"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list["Preformat"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question: list["Question"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question_wrap: list["QuestionWrap"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
        },
    )
    question_wrap_group: list["QuestionWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap-group",
            "type": "Element",
        },
    )
    supplementary_material: list["SupplementaryMaterial"] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list["TableWrap"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list["TableWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    disp_formula: list["DispFormula"] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list["DispFormulaGroup"] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    def_list: list["DefList"] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list["List"] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    related_article: list["RelatedArticle"] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list["RelatedObject"] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    disp_quote: list["DispQuote"] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list["Speech"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list["Statement"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list["VerseGroup"] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    fn_group: list["FnGroup"] = field(
        default_factory=list,
        metadata={
            "name": "fn-group",
            "type": "Element",
        },
    )
    glossary: list["Glossary"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ref_list: list["RefList"] = field(
        default_factory=list,
        metadata={
            "name": "ref-list",
            "type": "Element",
        },
    )
    explanation: list["Explanation"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    pointer_to_question: list[str] = field(
        default_factory=list,
        metadata={
            "name": "pointer-to-question",
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class ChapterTitle:
    """
    <div> <h3>Chapter Title in a Citation</h3> </div>
    """

    class Meta:
        name = "chapter-title"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ForwardRef("ExtLink"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ForwardRef("ChemStruct"),
                },
                {
                    "name": "inline-formula",
                    "type": ForwardRef("InlineFormula"),
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": ForwardRef("Fn"),
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class ChemStruct:
    """
    <div> <h3>Chemical Structure (Display)</h3> </div>
    """

    class Meta:
        name = "chem-struct"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "alt-text",
                    "type": AltText,
                },
                {
                    "name": "long-desc",
                    "type": LongDesc,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ForwardRef("ExtLink"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "break",
                    "type": Break,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "label",
                    "type": ForwardRef("Label"),
                },
                {
                    "name": "def-list",
                    "type": ForwardRef("DefList"),
                },
                {
                    "name": "list",
                    "type": ForwardRef("List"),
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "array",
                    "type": Array,
                },
                {
                    "name": "code",
                    "type": ForwardRef("Code"),
                },
                {
                    "name": "graphic",
                    "type": ForwardRef("Graphic"),
                },
                {
                    "name": "media",
                    "type": ForwardRef("Media"),
                },
                {
                    "name": "preformat",
                    "type": ForwardRef("Preformat"),
                },
                {
                    "name": "fn",
                    "type": ForwardRef("Fn"),
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class Code:
    """
    <div> <h3>Code Text</h3> </div>
    """

    class Meta:
        name = "code"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    code_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "code-type",
            "type": "Attribute",
        },
    )
    code_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "code-version",
            "type": "Attribute",
        },
    )
    executable: Optional[CodeExecutable] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    language: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    language_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "language-version",
            "type": "Attribute",
        },
    )
    orientation: CodeOrientation = field(
        default=CodeOrientation.PORTRAIT,
        metadata={
            "type": "Attribute",
        },
    )
    platforms: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    position: CodePosition = field(
        default=CodePosition.FLOAT,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: SpaceValue = field(
        init=False,
        default=SpaceValue.PRESERVE,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ForwardRef("ExtLink"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": ForwardRef("IndexTerm"),
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": ForwardRef("Fn"),
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class CopyrightStatement:
    """
    <div> <h3>Copyright Statement</h3> </div>
    """

    class Meta:
        name = "copyright-statement"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ForwardRef("ExtLink"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class DataTitle:
    """
    <div> <h3>Data Title in a Citation</h3> </div>
    """

    class Meta:
        name = "data-title"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ForwardRef("ExtLink"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class ExtLink:
    """
    <div> <h3>External Link</h3> </div>
    """

    class Meta:
        name = "ext-link"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    ext_link_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ext-link-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class AnswerSet:
    """
    <div> <h3>Answer Set</h3> </div>
    """

    class Meta:
        name = "answer-set"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: Optional["Label"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    subtitle: list["Subtitle"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alt_title: list[AltTitle] = field(
        default_factory=list,
        metadata={
            "name": "alt-title",
            "type": "Element",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    explanation: list["Explanation"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class ChemStructWrap:
    """
    <div> <h3>Chemical Structure Wrapper</h3> </div>
    """

    class Meta:
        name = "chem-struct-wrap"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: Optional["Label"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    caption: Optional[Caption] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    abstract: list[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    kwd_group: list["KwdGroup"] = field(
        default_factory=list,
        metadata={
            "name": "kwd-group",
            "type": "Element",
        },
    )
    subj_group: list["SubjGroup"] = field(
        default_factory=list,
        metadata={
            "name": "subj-group",
            "type": "Element",
        },
    )
    alt_text: list[AltText] = field(
        default_factory=list,
        metadata={
            "name": "alt-text",
            "type": "Element",
        },
    )
    long_desc: list[LongDesc] = field(
        default_factory=list,
        metadata={
            "name": "long-desc",
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list["ExtLink"] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    chem_struct: list[ChemStruct] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct",
            "type": "Element",
        },
    )
    code: list["Code"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    graphic: list["Graphic"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list["Media"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list["Preformat"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    textual_form: list["TextualForm"] = field(
        default_factory=list,
        metadata={
            "name": "textual-form",
            "type": "Element",
        },
    )
    attrib: list[Attrib] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    permissions: list["Permissions"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    orientation: ChemStructWrapOrientation = field(
        default=ChemStructWrapOrientation.PORTRAIT,
        metadata={
            "type": "Attribute",
        },
    )
    position: ChemStructWrapPosition = field(
        default=ChemStructWrapPosition.FLOAT,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Comment:
    """
    <div> <h3>Comment in a Citation</h3> </div>
    """

    class Meta:
        name = "comment"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ForwardRef("ExtLink"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": ForwardRef("InlineSupplementaryMaterial"),
                },
                {
                    "name": "related-article",
                    "type": ForwardRef("RelatedArticle"),
                },
                {
                    "name": "related-object",
                    "type": ForwardRef("RelatedObject"),
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": ForwardRef("InlineFormula"),
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": ForwardRef("IndexTerm"),
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": ForwardRef("Fn"),
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class DefHead:
    """
    <div> <h3>Definition List: Definition Head</h3> </div>
    """

    class Meta:
        name = "def-head"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ForwardRef("ExtLink"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": ForwardRef("InlineSupplementaryMaterial"),
                },
                {
                    "name": "related-article",
                    "type": ForwardRef("RelatedArticle"),
                },
                {
                    "name": "related-object",
                    "type": ForwardRef("RelatedObject"),
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": ForwardRef("InlineFormula"),
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": ForwardRef("IndexTerm"),
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": ForwardRef("Fn"),
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class DispFormula:
    """
    <div> <h3>Formula, Display</h3> </div>
    """

    class Meta:
        name = "disp-formula"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "alt-text",
                    "type": AltText,
                },
                {
                    "name": "long-desc",
                    "type": LongDesc,
                },
                {
                    "name": "abstract",
                    "type": Abstract,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ForwardRef("ExtLink"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "break",
                    "type": Break,
                },
                {
                    "name": "caption",
                    "type": Caption,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "object-id",
                    "type": ObjectId,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": ForwardRef("InlineFormula"),
                },
                {
                    "name": "kwd-group",
                    "type": ForwardRef("KwdGroup"),
                },
                {
                    "name": "subj-group",
                    "type": ForwardRef("SubjGroup"),
                },
                {
                    "name": "label",
                    "type": ForwardRef("Label"),
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "array",
                    "type": Array,
                },
                {
                    "name": "code",
                    "type": Code,
                },
                {
                    "name": "graphic",
                    "type": ForwardRef("Graphic"),
                },
                {
                    "name": "media",
                    "type": ForwardRef("Media"),
                },
                {
                    "name": "preformat",
                    "type": ForwardRef("Preformat"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class EventDesc:
    """
    <div> <h3>Event Description</h3> </div>
    """

    class Meta:
        name = "event-desc"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "article-id",
                    "type": ArticleId,
                },
                {
                    "name": "issn",
                    "type": Issn,
                },
                {
                    "name": "issn-l",
                    "type": IssnL,
                },
                {
                    "name": "isbn",
                    "type": Isbn,
                },
                {
                    "name": "article-version",
                    "type": ArticleVersion,
                },
                {
                    "name": "article-version-alternatives",
                    "type": ArticleVersionAlternatives,
                },
                {
                    "name": "date",
                    "type": Date,
                },
                {
                    "name": "string-date",
                    "type": StringDate,
                },
                {
                    "name": "pub-date",
                    "type": PubDate,
                },
                {
                    "name": "pub-date-not-available",
                    "type": PubDateNotAvailable,
                },
            ),
        },
    )


@dataclass
class FixedCase:
    """
    <div> <h3>Fixed Case</h3> </div>
    """

    class Meta:
        name = "fixed-case"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": ForwardRef("InlineSupplementaryMaterial"),
                },
                {
                    "name": "related-article",
                    "type": ForwardRef("RelatedArticle"),
                },
                {
                    "name": "related-object",
                    "type": ForwardRef("RelatedObject"),
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": ForwardRef("InlineFormula"),
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": ForwardRef("IndexTerm"),
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": ForwardRef("Fn"),
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class Graphic:
    """
    <div> <h3>Graphic</h3> </div>
    """

    class Meta:
        name = "graphic"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    alt_text: list[AltText] = field(
        default_factory=list,
        metadata={
            "name": "alt-text",
            "type": "Element",
        },
    )
    long_desc: list[LongDesc] = field(
        default_factory=list,
        metadata={
            "name": "long-desc",
            "type": "Element",
        },
    )
    abstract: list[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list[ExtLink] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    caption: list[Caption] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    attrib: list[Attrib] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    permissions: list["Permissions"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: list["Label"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    kwd_group: list["KwdGroup"] = field(
        default_factory=list,
        metadata={
            "name": "kwd-group",
            "type": "Element",
        },
    )
    subj_group: list["SubjGroup"] = field(
        default_factory=list,
        metadata={
            "name": "subj-group",
            "type": "Element",
        },
    )
    xref: list["Xref"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    mime_subtype: Optional[str] = field(
        default=None,
        metadata={
            "name": "mime-subtype",
            "type": "Attribute",
        },
    )
    mimetype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    orientation: GraphicOrientation = field(
        default=GraphicOrientation.PORTRAIT,
        metadata={
            "type": "Attribute",
        },
    )
    position: GraphicPosition = field(
        default=GraphicPosition.FLOAT,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "required": True,
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Permissions:
    """
    <div> <h3>Permissions</h3> </div>
    """

    class Meta:
        name = "permissions"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    copyright_statement: list[CopyrightStatement] = field(
        default_factory=list,
        metadata={
            "name": "copyright-statement",
            "type": "Element",
        },
    )
    copyright_year: list[CopyrightYear] = field(
        default_factory=list,
        metadata={
            "name": "copyright-year",
            "type": "Element",
        },
    )
    copyright_holder: list[CopyrightHolder] = field(
        default_factory=list,
        metadata={
            "name": "copyright-holder",
            "type": "Element",
        },
    )
    free_to_read: list[FreeToRead] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.niso.org/schemas/ali/1.0/",
        },
    )
    license: list[License] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class PublisherLoc:
    """
    <div> <h3>Publisher's Location</h3> </div>
    """

    class Meta:
        name = "publisher-loc"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "addr-line",
                    "type": AddrLine,
                },
                {
                    "name": "city",
                    "type": City,
                },
                {
                    "name": "country",
                    "type": Country,
                },
                {
                    "name": "fax",
                    "type": Fax,
                },
                {
                    "name": "institution",
                    "type": Institution,
                },
                {
                    "name": "institution-wrap",
                    "type": InstitutionWrap,
                },
                {
                    "name": "phone",
                    "type": Phone,
                },
                {
                    "name": "postal-code",
                    "type": PostalCode,
                },
                {
                    "name": "state",
                    "type": State,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
            ),
        },
    )


@dataclass
class Bio:
    """
    <div> <h3>Biography</h3> </div>
    """

    class Meta:
        name = "bio"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    sec_meta: Optional["SecMeta"] = field(
        default=None,
        metadata={
            "name": "sec-meta",
            "type": "Element",
        },
    )
    label: Optional["Label"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer_set: list[AnswerSet] = field(
        default_factory=list,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list["BlockAlternatives"] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list["BoxedText"] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list["ChemStructWrap"] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list["Code"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    explanation: list["Explanation"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list["Fig"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list["FigGroup"] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list["Graphic"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list["Media"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list["Preformat"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question: list["Question"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question_wrap: list["QuestionWrap"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
        },
    )
    question_wrap_group: list["QuestionWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap-group",
            "type": "Element",
        },
    )
    supplementary_material: list["SupplementaryMaterial"] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list["TableWrap"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list["TableWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    disp_formula: list["DispFormula"] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list["DispFormulaGroup"] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    def_list: list["DefList"] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list["List"] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    related_article: list["RelatedArticle"] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list["RelatedObject"] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    disp_quote: list["DispQuote"] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list["Speech"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list["Statement"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list["VerseGroup"] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    sec: list["Sec"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fn_group: list["FnGroup"] = field(
        default_factory=list,
        metadata={
            "name": "fn-group",
            "type": "Element",
        },
    )
    glossary: list["Glossary"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ref_list: list["RefList"] = field(
        default_factory=list,
        metadata={
            "name": "ref-list",
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title_attribute: Optional[str] = field(
        default=None,
        metadata={
            "name": "title",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class BoxedText:
    """
    <div> <h3>Boxed Text</h3> </div>
    """

    class Meta:
        name = "boxed-text"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    sec_meta: Optional["SecMeta"] = field(
        default=None,
        metadata={
            "name": "sec-meta",
            "type": "Element",
        },
    )
    label: Optional["Label"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    caption: Optional["Caption"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer_set: list[AnswerSet] = field(
        default_factory=list,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list[BlockAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list["BoxedText"] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list["ChemStructWrap"] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list["Code"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    explanation: list["Explanation"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list["Fig"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list["FigGroup"] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list["Graphic"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list["Media"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list["Preformat"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question: list["Question"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question_wrap: list["QuestionWrap"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
        },
    )
    question_wrap_group: list["QuestionWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap-group",
            "type": "Element",
        },
    )
    supplementary_material: list["SupplementaryMaterial"] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list["TableWrap"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list["TableWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    disp_formula: list["DispFormula"] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list["DispFormulaGroup"] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    def_list: list["DefList"] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list["List"] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    related_article: list["RelatedArticle"] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list["RelatedObject"] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    disp_quote: list["DispQuote"] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list["Speech"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list["Statement"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list["VerseGroup"] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    sec: list["Sec"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fn_group: list["FnGroup"] = field(
        default_factory=list,
        metadata={
            "name": "fn-group",
            "type": "Element",
        },
    )
    glossary: list["Glossary"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ref_list: list["RefList"] = field(
        default_factory=list,
        metadata={
            "name": "ref-list",
            "type": "Element",
        },
    )
    attrib: list[Attrib] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    permissions: list["Permissions"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    orientation: BoxedTextOrientation = field(
        default=BoxedTextOrientation.PORTRAIT,
        metadata={
            "type": "Attribute",
        },
    )
    position: BoxedTextPosition = field(
        default=BoxedTextPosition.FLOAT,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class DefList:
    """
    <div> <h3>Definition List</h3> </div>
    """

    class Meta:
        name = "def-list"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    label: Optional["Label"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    term_head: Optional["TermHead"] = field(
        default=None,
        metadata={
            "name": "term-head",
            "type": "Element",
        },
    )
    def_head: Optional[DefHead] = field(
        default=None,
        metadata={
            "name": "def-head",
            "type": "Element",
        },
    )
    def_item: list[DefItem] = field(
        default_factory=list,
        metadata={
            "name": "def-item",
            "type": "Element",
        },
    )
    def_list: list["DefList"] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    continued_from: Optional[str] = field(
        default=None,
        metadata={
            "name": "continued-from",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    list_content: Optional[str] = field(
        default=None,
        metadata={
            "name": "list-content",
            "type": "Attribute",
        },
    )
    list_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "list-type",
            "type": "Attribute",
        },
    )
    prefix_word: Optional[str] = field(
        default=None,
        metadata={
            "name": "prefix-word",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class DispFormulaGroup:
    """
    <div> <h3>Formula, Display Group</h3> </div>
    """

    class Meta:
        name = "disp-formula-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: Optional["Label"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    caption: Optional[Caption] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    abstract: list[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    kwd_group: list["KwdGroup"] = field(
        default_factory=list,
        metadata={
            "name": "kwd-group",
            "type": "Element",
        },
    )
    subj_group: list["SubjGroup"] = field(
        default_factory=list,
        metadata={
            "name": "subj-group",
            "type": "Element",
        },
    )
    alt_text: list[AltText] = field(
        default_factory=list,
        metadata={
            "name": "alt-text",
            "type": "Element",
        },
    )
    long_desc: list[LongDesc] = field(
        default_factory=list,
        metadata={
            "name": "long-desc",
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list["ExtLink"] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list["DispFormulaGroup"] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class FundingSource:
    """
    <div> <h3>Funding Source</h3> </div>
    """

    class Meta:
        name = "funding-source"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    country: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    source_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "source-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": ForwardRef("InlineFormula"),
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": ForwardRef("IndexTerm"),
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
                {
                    "name": "institution",
                    "type": ForwardRef("Institution"),
                },
                {
                    "name": "institution-wrap",
                    "type": ForwardRef("InstitutionWrap"),
                },
            ),
        },
    )


@dataclass
class Gov:
    """
    <div> <h3>Government Report, Cited</h3> </div>
    """

    class Meta:
        name = "gov"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
            ),
        },
    )


@dataclass
class InlineFormula:
    """
    <div> <h3>Formula, Inline</h3> </div>
    """

    class Meta:
        name = "inline-formula"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "alt-text",
                    "type": AltText,
                },
                {
                    "name": "long-desc",
                    "type": LongDesc,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": ForwardRef("InlineFormula"),
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class InlineMedia:
    """
    <div> <h3>Inline Media Object</h3> </div>
    """

    class Meta:
        name = "inline-media"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    mime_subtype: Optional[str] = field(
        default=None,
        metadata={
            "name": "mime-subtype",
            "type": "Attribute",
        },
    )
    mimetype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    vocab_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term",
            "type": "Attribute",
        },
    )
    vocab_term_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term-identifier",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "required": True,
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "alt-text",
                    "type": AltText,
                },
                {
                    "name": "long-desc",
                    "type": LongDesc,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class InlineSupplementaryMaterial:
    """
    <div> <h3>Inline Supplementary Material</h3> </div>
    """

    class Meta:
        name = "inline-supplementary-material"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    mime_subtype: Optional[str] = field(
        default=None,
        metadata={
            "name": "mime-subtype",
            "type": "Attribute",
        },
    )
    mimetype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "alt-text",
                    "type": AltText,
                },
                {
                    "name": "long-desc",
                    "type": LongDesc,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class Publisher:
    """
    <div> <h3>Publisher</h3> </div>
    """

    class Meta:
        name = "publisher"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    publisher_name: list[PublisherName] = field(
        default_factory=list,
        metadata={
            "name": "publisher-name",
            "type": "Element",
            "sequence": 1,
        },
    )
    publisher_loc: list[PublisherLoc] = field(
        default_factory=list,
        metadata={
            "name": "publisher-loc",
            "type": "Element",
            "sequence": 1,
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Collab:
    """
    <div> <h3>Collaborative (Group) Author</h3> </div>
    """

    class Meta:
        name = "collab"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    collab_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "collab-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    symbol: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": ForwardRef("FixedCase"),
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": ForwardRef("InlineMedia"),
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": ForwardRef("InlineFormula"),
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": ForwardRef("IndexTerm"),
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
                {
                    "name": "addr-line",
                    "type": AddrLine,
                },
                {
                    "name": "city",
                    "type": City,
                },
                {
                    "name": "country",
                    "type": Country,
                },
                {
                    "name": "fax",
                    "type": Fax,
                },
                {
                    "name": "institution",
                    "type": ForwardRef("Institution"),
                },
                {
                    "name": "institution-wrap",
                    "type": ForwardRef("InstitutionWrap"),
                },
                {
                    "name": "phone",
                    "type": Phone,
                },
                {
                    "name": "postal-code",
                    "type": PostalCode,
                },
                {
                    "name": "state",
                    "type": State,
                },
                {
                    "name": "contrib-group",
                    "type": ForwardRef("ContribGroup"),
                },
                {
                    "name": "address",
                    "type": Address,
                },
                {
                    "name": "aff",
                    "type": Aff,
                },
                {
                    "name": "aff-alternatives",
                    "type": AffAlternatives,
                },
                {
                    "name": "author-comment",
                    "type": AuthorComment,
                },
                {
                    "name": "bio",
                    "type": Bio,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ForwardRef("ExtLink"),
                },
                {
                    "name": "on-behalf-of",
                    "type": ForwardRef("OnBehalfOf"),
                },
                {
                    "name": "role",
                    "type": ForwardRef("Role"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "fn",
                    "type": ForwardRef("Fn"),
                },
            ),
        },
    )


@dataclass
class DispQuote:
    """
    <div> <h3>Quote, Displayed</h3> </div>
    """

    class Meta:
        name = "disp-quote"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    label: Optional["Label"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer_set: list[AnswerSet] = field(
        default_factory=list,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list[BlockAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list[BoxedText] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    explanation: list["Explanation"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list["Fig"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list["FigGroup"] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list["Graphic"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list["Media"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list["Preformat"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question: list["Question"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question_wrap: list["QuestionWrap"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
        },
    )
    question_wrap_group: list["QuestionWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap-group",
            "type": "Element",
        },
    )
    supplementary_material: list["SupplementaryMaterial"] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list["TableWrap"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list["TableWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list[DispFormulaGroup] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list["List"] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    related_article: list["RelatedArticle"] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list["RelatedObject"] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    disp_quote: list["DispQuote"] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list["Speech"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list["Statement"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list["VerseGroup"] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    attrib: list[Attrib] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    permissions: list["Permissions"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Italic:
    """
    <div> <h3>Italic</h3> </div>
    """

    class Meta:
        name = "italic"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    toggle: ItalicToggle = field(
        default=ItalicToggle.YES,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": ForwardRef("RelatedArticle"),
                },
                {
                    "name": "related-object",
                    "type": ForwardRef("RelatedObject"),
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": ForwardRef("Italic"),
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class CollabAlternatives:
    """
    <div> <h3>Collaboration Alternatives</h3> </div>
    """

    class Meta:
        name = "collab-alternatives"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    collab: list[Collab] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Explanation:
    """
    <div> <h3>Explanation</h3> </div>
    """

    class Meta:
        name = "explanation"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: Optional["Label"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    subtitle: list["Subtitle"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alt_title: list[AltTitle] = field(
        default_factory=list,
        metadata={
            "name": "alt-title",
            "type": "Element",
        },
    )
    sec: list["Sec"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer_set: list[AnswerSet] = field(
        default_factory=list,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list[BlockAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list[BoxedText] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list["Fig"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list["FigGroup"] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list["Graphic"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list["Media"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list["Preformat"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question: list["Question"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question_wrap: list["QuestionWrap"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
        },
    )
    question_wrap_group: list["QuestionWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap-group",
            "type": "Element",
        },
    )
    supplementary_material: list["SupplementaryMaterial"] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list["TableWrap"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list["TableWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list[DispFormulaGroup] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list["List"] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    related_article: list["RelatedArticle"] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list["RelatedObject"] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    disp_quote: list[DispQuote] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list["Speech"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list["Statement"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list["VerseGroup"] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    fn_group: list["FnGroup"] = field(
        default_factory=list,
        metadata={
            "name": "fn-group",
            "type": "Element",
        },
    )
    glossary: list["Glossary"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ref_list: list["RefList"] = field(
        default_factory=list,
        metadata={
            "name": "ref-list",
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    pointer_to_explained: list[str] = field(
        default_factory=list,
        metadata={
            "name": "pointer-to-explained",
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Fig:
    """
    <div> <h3>Figure</h3> </div>
    """

    class Meta:
        name = "fig"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: list["Label"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    caption: list[Caption] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    abstract: list[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    kwd_group: list["KwdGroup"] = field(
        default_factory=list,
        metadata={
            "name": "kwd-group",
            "type": "Element",
        },
    )
    subj_group: list["SubjGroup"] = field(
        default_factory=list,
        metadata={
            "name": "subj-group",
            "type": "Element",
        },
    )
    alt_text: list[AltText] = field(
        default_factory=list,
        metadata={
            "name": "alt-text",
            "type": "Element",
        },
    )
    long_desc: list[LongDesc] = field(
        default_factory=list,
        metadata={
            "name": "long-desc",
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list[ExtLink] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list[DispFormulaGroup] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    disp_quote: list[DispQuote] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list["Speech"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list["Statement"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list["VerseGroup"] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    table_wrap: list["TableWrap"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list["List"] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    graphic: list["Graphic"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list["Media"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list["Preformat"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    xref: list["Xref"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    attrib: list[Attrib] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    permissions: list["Permissions"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "fig-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    orientation: FigOrientation = field(
        default=FigOrientation.PORTRAIT,
        metadata={
            "type": "Attribute",
        },
    )
    position: FigPosition = field(
        default=FigPosition.FLOAT,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Kwd:
    """
    <div> <h3>Keyword</h3> </div>
    """

    class Meta:
        name = "kwd"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    vocab_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term",
            "type": "Attribute",
        },
    )
    vocab_term_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term-identifier",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class Label:
    """
    <div> <h3>Label of a Figure, Reference, Etc.</h3> </div>
    """

    class Meta:
        name = "label"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    alt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class Monospace:
    """
    <div> <h3>Monospace Text (Typewriter Text)</h3> </div>
    """

    class Meta:
        name = "monospace"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    toggle: Optional[MonospaceToggle] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": ForwardRef("RelatedArticle"),
                },
                {
                    "name": "related-object",
                    "type": ForwardRef("RelatedObject"),
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class NlmCitation:
    """
    <div> <h3>Nlm Citation Model</h3> </div>
    """

    class Meta:
        name = "nlm-citation"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    person_group: list["PersonGroup"] = field(
        default_factory=list,
        metadata={
            "name": "person-group",
            "type": "Element",
        },
    )
    collab: list[Collab] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    article_title: list[ArticleTitle] = field(
        default_factory=list,
        metadata={
            "name": "article-title",
            "type": "Element",
        },
    )
    trans_title: list["TransTitle"] = field(
        default_factory=list,
        metadata={
            "name": "trans-title",
            "type": "Element",
        },
    )
    source: Optional["Source"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    patent: Optional[Patent] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    trans_source: Optional["TransSource"] = field(
        default=None,
        metadata={
            "name": "trans-source",
            "type": "Element",
        },
    )
    year: Optional[Year] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    month: Optional[Month] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    day: Optional[Day] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    time_stamp: Optional[TimeStamp] = field(
        default=None,
        metadata={
            "name": "time-stamp",
            "type": "Element",
        },
    )
    season: Optional[Season] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    access_date: Optional[AccessDate] = field(
        default=None,
        metadata={
            "name": "access-date",
            "type": "Element",
        },
    )
    volume: Optional[Volume] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    edition: Optional[Edition] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    conf_name: Optional[ConfName] = field(
        default=None,
        metadata={
            "name": "conf-name",
            "type": "Element",
        },
    )
    conf_date: Optional[ConfDate] = field(
        default=None,
        metadata={
            "name": "conf-date",
            "type": "Element",
        },
    )
    conf_loc: Optional[ConfLoc] = field(
        default=None,
        metadata={
            "name": "conf-loc",
            "type": "Element",
        },
    )
    issue: list[Issue] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    supplement: list["Supplement"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    publisher_loc: Optional[PublisherLoc] = field(
        default=None,
        metadata={
            "name": "publisher-loc",
            "type": "Element",
        },
    )
    publisher_name: Optional[PublisherName] = field(
        default=None,
        metadata={
            "name": "publisher-name",
            "type": "Element",
        },
    )
    fpage: list[Fpage] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    lpage: list[Lpage] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    page_count: Optional[PageCount] = field(
        default=None,
        metadata={
            "name": "page-count",
            "type": "Element",
        },
    )
    series: Optional["Series"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    comment: list[Comment] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    pub_id: list[PubId] = field(
        default_factory=list,
        metadata={
            "name": "pub-id",
            "type": "Element",
        },
    )
    annotation: Optional[Annotation] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    publication_format: Optional[str] = field(
        default=None,
        metadata={
            "name": "publication-format",
            "type": "Attribute",
        },
    )
    publication_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "publication-type",
            "type": "Attribute",
        },
    )
    publisher_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "publisher-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Contrib:
    """
    <div> <h3>Contributor</h3> </div>
    """

    class Meta:
        name = "contrib"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    contrib_id: list[ContribId] = field(
        default_factory=list,
        metadata={
            "name": "contrib-id",
            "type": "Element",
        },
    )
    anonymous: list[Anonymous] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    collab: list[Collab] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    collab_alternatives: list[CollabAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "collab-alternatives",
            "type": "Element",
        },
    )
    name: list[Name] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    name_alternatives: list[NameAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "name-alternatives",
            "type": "Element",
        },
    )
    string_name: list[StringName] = field(
        default_factory=list,
        metadata={
            "name": "string-name",
            "type": "Element",
        },
    )
    degrees: list[Degrees] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    aff: list[Aff] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    aff_alternatives: list[AffAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "aff-alternatives",
            "type": "Element",
        },
    )
    author_comment: list[AuthorComment] = field(
        default_factory=list,
        metadata={
            "name": "author-comment",
            "type": "Element",
        },
    )
    bio: list[Bio] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list["ExtLink"] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    on_behalf_of: list["OnBehalfOf"] = field(
        default_factory=list,
        metadata={
            "name": "on-behalf-of",
            "type": "Element",
        },
    )
    role: list["Role"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    xref: list["Xref"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    contrib_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "contrib-type",
            "type": "Attribute",
        },
    )
    corresp: Optional[ContribCorresp] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    deceased: Optional[ContribDeceased] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    equal_contrib: Optional[ContribEqualContrib] = field(
        default=None,
        metadata={
            "name": "equal-contrib",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role_attribute: Optional[str] = field(
        default=None,
        metadata={
            "name": "role",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class ElementCitation:
    """
    <div> <h3>Element Citation</h3> </div>
    """

    class Meta:
        name = "element-citation"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    bold: list[Bold] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fixed_case: list["FixedCase"] = field(
        default_factory=list,
        metadata={
            "name": "fixed-case",
            "type": "Element",
        },
    )
    italic: list["Italic"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    monospace: list["Monospace"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    overline: list["Overline"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    roman: list["Roman"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    sans_serif: list["SansSerif"] = field(
        default_factory=list,
        metadata={
            "name": "sans-serif",
            "type": "Element",
        },
    )
    sc: list["Sc"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    strike: list["Strike"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    underline: list["Underline"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ruby: list["Ruby"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    inline_graphic: list[InlineGraphic] = field(
        default_factory=list,
        metadata={
            "name": "inline-graphic",
            "type": "Element",
        },
    )
    inline_media: list["InlineMedia"] = field(
        default_factory=list,
        metadata={
            "name": "inline-media",
            "type": "Element",
        },
    )
    private_char: list[PrivateChar] = field(
        default_factory=list,
        metadata={
            "name": "private-char",
            "type": "Element",
        },
    )
    chem_struct: list[ChemStruct] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct",
            "type": "Element",
        },
    )
    inline_formula: list["InlineFormula"] = field(
        default_factory=list,
        metadata={
            "name": "inline-formula",
            "type": "Element",
        },
    )
    label: list["Label"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    abbrev: list[Abbrev] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    index_term: list["IndexTerm"] = field(
        default_factory=list,
        metadata={
            "name": "index-term",
            "type": "Element",
        },
    )
    index_term_range_end: list[IndexTermRangeEnd] = field(
        default_factory=list,
        metadata={
            "name": "index-term-range-end",
            "type": "Element",
        },
    )
    milestone_end: list[MilestoneEnd] = field(
        default_factory=list,
        metadata={
            "name": "milestone-end",
            "type": "Element",
        },
    )
    milestone_start: list[MilestoneStart] = field(
        default_factory=list,
        metadata={
            "name": "milestone-start",
            "type": "Element",
        },
    )
    named_content: list["NamedContent"] = field(
        default_factory=list,
        metadata={
            "name": "named-content",
            "type": "Element",
        },
    )
    styled_content: list["StyledContent"] = field(
        default_factory=list,
        metadata={
            "name": "styled-content",
            "type": "Element",
        },
    )
    annotation: list[Annotation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    article_title: list[ArticleTitle] = field(
        default_factory=list,
        metadata={
            "name": "article-title",
            "type": "Element",
        },
    )
    chapter_title: list[ChapterTitle] = field(
        default_factory=list,
        metadata={
            "name": "chapter-title",
            "type": "Element",
        },
    )
    collab: list[Collab] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    collab_alternatives: list[CollabAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "collab-alternatives",
            "type": "Element",
        },
    )
    comment: list[Comment] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    conf_acronym: list[ConfAcronym] = field(
        default_factory=list,
        metadata={
            "name": "conf-acronym",
            "type": "Element",
        },
    )
    conf_date: list[ConfDate] = field(
        default_factory=list,
        metadata={
            "name": "conf-date",
            "type": "Element",
        },
    )
    conf_loc: list[ConfLoc] = field(
        default_factory=list,
        metadata={
            "name": "conf-loc",
            "type": "Element",
        },
    )
    conf_name: list[ConfName] = field(
        default_factory=list,
        metadata={
            "name": "conf-name",
            "type": "Element",
        },
    )
    conf_sponsor: list[ConfSponsor] = field(
        default_factory=list,
        metadata={
            "name": "conf-sponsor",
            "type": "Element",
        },
    )
    data_title: list[DataTitle] = field(
        default_factory=list,
        metadata={
            "name": "data-title",
            "type": "Element",
        },
    )
    date: list[Date] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    date_in_citation: list[DateInCitation] = field(
        default_factory=list,
        metadata={
            "name": "date-in-citation",
            "type": "Element",
        },
    )
    day: list[Day] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    edition: list[Edition] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    elocation_id: list[ElocationId] = field(
        default_factory=list,
        metadata={
            "name": "elocation-id",
            "type": "Element",
        },
    )
    etal: list[Etal] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list["ExtLink"] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    fpage: list[Fpage] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    gov: list["Gov"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    institution: list["Institution"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    institution_wrap: list["InstitutionWrap"] = field(
        default_factory=list,
        metadata={
            "name": "institution-wrap",
            "type": "Element",
        },
    )
    isbn: list[Isbn] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    issn: list[Issn] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    issn_l: list[IssnL] = field(
        default_factory=list,
        metadata={
            "name": "issn-l",
            "type": "Element",
        },
    )
    issue: list[Issue] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    issue_id: list[IssueId] = field(
        default_factory=list,
        metadata={
            "name": "issue-id",
            "type": "Element",
        },
    )
    issue_part: list[IssuePart] = field(
        default_factory=list,
        metadata={
            "name": "issue-part",
            "type": "Element",
        },
    )
    issue_title: list[IssueTitle] = field(
        default_factory=list,
        metadata={
            "name": "issue-title",
            "type": "Element",
        },
    )
    lpage: list[Lpage] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    month: list[Month] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    name: list[Name] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    name_alternatives: list[NameAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "name-alternatives",
            "type": "Element",
        },
    )
    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    page_range: list[PageRange] = field(
        default_factory=list,
        metadata={
            "name": "page-range",
            "type": "Element",
        },
    )
    part_title: list["PartTitle"] = field(
        default_factory=list,
        metadata={
            "name": "part-title",
            "type": "Element",
        },
    )
    patent: list[Patent] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    person_group: list["PersonGroup"] = field(
        default_factory=list,
        metadata={
            "name": "person-group",
            "type": "Element",
        },
    )
    pub_id: list[PubId] = field(
        default_factory=list,
        metadata={
            "name": "pub-id",
            "type": "Element",
        },
    )
    publisher_loc: list["PublisherLoc"] = field(
        default_factory=list,
        metadata={
            "name": "publisher-loc",
            "type": "Element",
        },
    )
    publisher_name: list["PublisherName"] = field(
        default_factory=list,
        metadata={
            "name": "publisher-name",
            "type": "Element",
        },
    )
    role: list["Role"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    season: list[Season] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    series: list["Series"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    size: list[Size] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    source: list["Source"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    std: list["Std"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    string_date: list[StringDate] = field(
        default_factory=list,
        metadata={
            "name": "string-date",
            "type": "Element",
        },
    )
    string_name: list[StringName] = field(
        default_factory=list,
        metadata={
            "name": "string-name",
            "type": "Element",
        },
    )
    supplement: list["Supplement"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    trans_source: list["TransSource"] = field(
        default_factory=list,
        metadata={
            "name": "trans-source",
            "type": "Element",
        },
    )
    trans_title: list["TransTitle"] = field(
        default_factory=list,
        metadata={
            "name": "trans-title",
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    version: list["Version"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    volume: list[Volume] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    volume_id: list[VolumeId] = field(
        default_factory=list,
        metadata={
            "name": "volume-id",
            "type": "Element",
        },
    )
    volume_series: list[VolumeSeries] = field(
        default_factory=list,
        metadata={
            "name": "volume-series",
            "type": "Element",
        },
    )
    year: list[Year] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    sub: list["Sub"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    sup: list["Sup"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    publication_format: Optional[str] = field(
        default=None,
        metadata={
            "name": "publication-format",
            "type": "Attribute",
        },
    )
    publication_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "publication-type",
            "type": "Attribute",
        },
    )
    publisher_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "publisher-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    use_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "use-type",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role_attribute: Optional[str] = field(
        default=None,
        metadata={
            "name": "role",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class FigGroup:
    """
    <div> <h3>Figure Group</h3> </div>
    """

    class Meta:
        name = "fig-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: list["Label"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    caption: list[Caption] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    abstract: list[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    kwd_group: list["KwdGroup"] = field(
        default_factory=list,
        metadata={
            "name": "kwd-group",
            "type": "Element",
        },
    )
    subj_group: list["SubjGroup"] = field(
        default_factory=list,
        metadata={
            "name": "subj-group",
            "type": "Element",
        },
    )
    alt_text: list[AltText] = field(
        default_factory=list,
        metadata={
            "name": "alt-text",
            "type": "Element",
        },
    )
    long_desc: list[LongDesc] = field(
        default_factory=list,
        metadata={
            "name": "long-desc",
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list[ExtLink] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list[Fig] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list[BlockAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    xref: list["Xref"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    graphic: list["Graphic"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list["Media"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    orientation: FigGroupOrientation = field(
        default=FigGroupOrientation.PORTRAIT,
        metadata={
            "type": "Attribute",
        },
    )
    position: FigGroupPosition = field(
        default=FigGroupPosition.FLOAT,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class List:
    """
    <div> <h3>List</h3> </div>
    """

    class Meta:
        name = "list"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    list_item: list["ListItem"] = field(
        default_factory=list,
        metadata={
            "name": "list-item",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    continued_from: Optional[str] = field(
        default=None,
        metadata={
            "name": "continued-from",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    list_content: Optional[str] = field(
        default=None,
        metadata={
            "name": "list-content",
            "type": "Attribute",
        },
    )
    list_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "list-type",
            "type": "Attribute",
        },
    )
    prefix_word: Optional[str] = field(
        default=None,
        metadata={
            "name": "prefix-word",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class MixedCitation:
    """
    <div> <h3>Mixed Citation</h3> </div>
    """

    class Meta:
        name = "mixed-citation"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    publication_format: Optional[str] = field(
        default=None,
        metadata={
            "name": "publication-format",
            "type": "Attribute",
        },
    )
    publication_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "publication-type",
            "type": "Attribute",
        },
    )
    publisher_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "publisher-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    use_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "use-type",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": ForwardRef("Monospace"),
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "label",
                    "type": Label,
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "annotation",
                    "type": Annotation,
                },
                {
                    "name": "article-title",
                    "type": ArticleTitle,
                },
                {
                    "name": "chapter-title",
                    "type": ChapterTitle,
                },
                {
                    "name": "collab",
                    "type": Collab,
                },
                {
                    "name": "collab-alternatives",
                    "type": CollabAlternatives,
                },
                {
                    "name": "comment",
                    "type": Comment,
                },
                {
                    "name": "conf-acronym",
                    "type": ConfAcronym,
                },
                {
                    "name": "conf-date",
                    "type": ConfDate,
                },
                {
                    "name": "conf-loc",
                    "type": ConfLoc,
                },
                {
                    "name": "conf-name",
                    "type": ConfName,
                },
                {
                    "name": "conf-sponsor",
                    "type": ConfSponsor,
                },
                {
                    "name": "data-title",
                    "type": DataTitle,
                },
                {
                    "name": "date",
                    "type": Date,
                },
                {
                    "name": "date-in-citation",
                    "type": DateInCitation,
                },
                {
                    "name": "day",
                    "type": Day,
                },
                {
                    "name": "edition",
                    "type": Edition,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "elocation-id",
                    "type": ElocationId,
                },
                {
                    "name": "etal",
                    "type": Etal,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "fpage",
                    "type": Fpage,
                },
                {
                    "name": "gov",
                    "type": Gov,
                },
                {
                    "name": "institution",
                    "type": Institution,
                },
                {
                    "name": "institution-wrap",
                    "type": InstitutionWrap,
                },
                {
                    "name": "isbn",
                    "type": Isbn,
                },
                {
                    "name": "issn",
                    "type": Issn,
                },
                {
                    "name": "issn-l",
                    "type": IssnL,
                },
                {
                    "name": "issue",
                    "type": Issue,
                },
                {
                    "name": "issue-id",
                    "type": IssueId,
                },
                {
                    "name": "issue-part",
                    "type": IssuePart,
                },
                {
                    "name": "issue-title",
                    "type": IssueTitle,
                },
                {
                    "name": "lpage",
                    "type": Lpage,
                },
                {
                    "name": "month",
                    "type": Month,
                },
                {
                    "name": "name",
                    "type": Name,
                },
                {
                    "name": "name-alternatives",
                    "type": NameAlternatives,
                },
                {
                    "name": "object-id",
                    "type": ObjectId,
                },
                {
                    "name": "page-range",
                    "type": PageRange,
                },
                {
                    "name": "part-title",
                    "type": ForwardRef("PartTitle"),
                },
                {
                    "name": "patent",
                    "type": Patent,
                },
                {
                    "name": "person-group",
                    "type": ForwardRef("PersonGroup"),
                },
                {
                    "name": "pub-id",
                    "type": PubId,
                },
                {
                    "name": "publisher-loc",
                    "type": PublisherLoc,
                },
                {
                    "name": "publisher-name",
                    "type": PublisherName,
                },
                {
                    "name": "role",
                    "type": ForwardRef("Role"),
                },
                {
                    "name": "season",
                    "type": Season,
                },
                {
                    "name": "series",
                    "type": ForwardRef("Series"),
                },
                {
                    "name": "size",
                    "type": Size,
                },
                {
                    "name": "source",
                    "type": ForwardRef("Source"),
                },
                {
                    "name": "std",
                    "type": ForwardRef("Std"),
                },
                {
                    "name": "string-date",
                    "type": StringDate,
                },
                {
                    "name": "string-name",
                    "type": StringName,
                },
                {
                    "name": "supplement",
                    "type": ForwardRef("Supplement"),
                },
                {
                    "name": "trans-source",
                    "type": ForwardRef("TransSource"),
                },
                {
                    "name": "trans-title",
                    "type": ForwardRef("TransTitle"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "version",
                    "type": ForwardRef("Version"),
                },
                {
                    "name": "volume",
                    "type": Volume,
                },
                {
                    "name": "volume-id",
                    "type": VolumeId,
                },
                {
                    "name": "volume-series",
                    "type": VolumeSeries,
                },
                {
                    "name": "year",
                    "type": Year,
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class NestedKwd:
    """
    <div> <h3>Nested Keyword</h3> </div>
    """

    class Meta:
        name = "nested-kwd"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    kwd: list[Kwd] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    compound_kwd: list[CompoundKwd] = field(
        default_factory=list,
        metadata={
            "name": "compound-kwd",
            "type": "Element",
        },
    )
    nested_kwd: list["NestedKwd"] = field(
        default_factory=list,
        metadata={
            "name": "nested-kwd",
            "type": "Element",
        },
    )
    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    vocab_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term",
            "type": "Attribute",
        },
    )
    vocab_term_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term-identifier",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Note:
    """
    <div> <h3>Note in a Reference List</h3> </div>
    """

    class Meta:
        name = "note"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    product: list["Product"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class PersonGroup:
    """
    <div> <h3>Person Group For a Cited Publication</h3> </div>
    """

    class Meta:
        name = "person-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    custom_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "custom-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    person_group_type: Optional[PersonGroupPersonGroupType] = field(
        default=None,
        metadata={
            "name": "person-group-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "anonymous",
                    "type": Anonymous,
                },
                {
                    "name": "collab",
                    "type": Collab,
                },
                {
                    "name": "collab-alternatives",
                    "type": CollabAlternatives,
                },
                {
                    "name": "name",
                    "type": Name,
                },
                {
                    "name": "name-alternatives",
                    "type": NameAlternatives,
                },
                {
                    "name": "string-name",
                    "type": StringName,
                },
                {
                    "name": "aff",
                    "type": Aff,
                },
                {
                    "name": "aff-alternatives",
                    "type": AffAlternatives,
                },
                {
                    "name": "etal",
                    "type": Etal,
                },
                {
                    "name": "role",
                    "type": ForwardRef("Role"),
                },
            ),
        },
    )


@dataclass
class ContribGroup:
    """
    <div> <h3>Contributor Group</h3> </div>
    """

    class Meta:
        name = "contrib-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    contrib: list[Contrib] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    aff: list[Aff] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    aff_alternatives: list[AffAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "aff-alternatives",
            "type": "Element",
        },
    )
    author_comment: list[AuthorComment] = field(
        default_factory=list,
        metadata={
            "name": "author-comment",
            "type": "Element",
        },
    )
    bio: list[Bio] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list["ExtLink"] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    on_behalf_of: list["OnBehalfOf"] = field(
        default_factory=list,
        metadata={
            "name": "on-behalf-of",
            "type": "Element",
        },
    )
    role: list["Role"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    xref: list["Xref"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Glossary:
    """
    <div> <h3>Glossary Elements</h3> </div>
    """

    class Meta:
        name = "glossary"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: Optional["Label"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer_set: list[AnswerSet] = field(
        default_factory=list,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list[BlockAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list[BoxedText] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    explanation: list[Explanation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list[Fig] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list[FigGroup] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list["Graphic"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list["Media"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list["Preformat"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question: list["Question"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question_wrap: list["QuestionWrap"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
        },
    )
    question_wrap_group: list["QuestionWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap-group",
            "type": "Element",
        },
    )
    supplementary_material: list["SupplementaryMaterial"] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list["TableWrap"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list["TableWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list[DispFormulaGroup] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list["List"] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    related_article: list["RelatedArticle"] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list["RelatedObject"] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    disp_quote: list[DispQuote] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list["Speech"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list["Statement"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list["VerseGroup"] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    glossary: list["Glossary"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class KwdGroup:
    """
    <div> <h3>Keyword Group</h3> </div>
    """

    class Meta:
        name = "kwd-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    label: Optional["Label"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    kwd: list[Kwd] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    compound_kwd: list[CompoundKwd] = field(
        default_factory=list,
        metadata={
            "name": "compound-kwd",
            "type": "Element",
        },
    )
    nested_kwd: list[NestedKwd] = field(
        default_factory=list,
        metadata={
            "name": "nested-kwd",
            "type": "Element",
        },
    )
    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    kwd_group_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "kwd-group-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Ref:
    """
    <div> <h3>Reference Item</h3> </div>
    """

    class Meta:
        name = "ref"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    citation_alternatives: list[CitationAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "citation-alternatives",
            "type": "Element",
        },
    )
    element_citation: list[ElementCitation] = field(
        default_factory=list,
        metadata={
            "name": "element-citation",
            "type": "Element",
        },
    )
    mixed_citation: list[MixedCitation] = field(
        default_factory=list,
        metadata={
            "name": "mixed-citation",
            "type": "Element",
        },
    )
    nlm_citation: list[NlmCitation] = field(
        default_factory=list,
        metadata={
            "name": "nlm-citation",
            "type": "Element",
        },
    )
    note: list[Note] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Media:
    """
    <div> <h3>Media Object</h3> </div>
    """

    class Meta:
        name = "media"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    alt_text: list[AltText] = field(
        default_factory=list,
        metadata={
            "name": "alt-text",
            "type": "Element",
        },
    )
    long_desc: list[LongDesc] = field(
        default_factory=list,
        metadata={
            "name": "long-desc",
            "type": "Element",
        },
    )
    abstract: list[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list[ExtLink] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    caption: list[Caption] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    attrib: list[Attrib] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    permissions: list[Permissions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: list[Label] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    kwd_group: list[KwdGroup] = field(
        default_factory=list,
        metadata={
            "name": "kwd-group",
            "type": "Element",
        },
    )
    subj_group: list["SubjGroup"] = field(
        default_factory=list,
        metadata={
            "name": "subj-group",
            "type": "Element",
        },
    )
    xref: list["Xref"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    mime_subtype: Optional[str] = field(
        default=None,
        metadata={
            "name": "mime-subtype",
            "type": "Attribute",
        },
    )
    mimetype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    orientation: MediaOrientation = field(
        default=MediaOrientation.PORTRAIT,
        metadata={
            "type": "Attribute",
        },
    )
    position: MediaPosition = field(
        default=MediaPosition.FLOAT,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "required": True,
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class NamedContent:
    """
    <div> <h3>Named Special (Subject) Content</h3> </div>
    """

    class Meta:
        name = "named-content"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    alt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
            "required": True,
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    vocab_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term",
            "type": "Attribute",
        },
    )
    vocab_term_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term-identifier",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": ForwardRef("RelatedArticle"),
                },
                {
                    "name": "related-object",
                    "type": ForwardRef("RelatedObject"),
                },
                {
                    "name": "address",
                    "type": Address,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "answer",
                    "type": Answer,
                },
                {
                    "name": "answer-set",
                    "type": AnswerSet,
                },
                {
                    "name": "array",
                    "type": Array,
                },
                {
                    "name": "block-alternatives",
                    "type": BlockAlternatives,
                },
                {
                    "name": "boxed-text",
                    "type": BoxedText,
                },
                {
                    "name": "chem-struct-wrap",
                    "type": ChemStructWrap,
                },
                {
                    "name": "code",
                    "type": Code,
                },
                {
                    "name": "explanation",
                    "type": Explanation,
                },
                {
                    "name": "fig",
                    "type": Fig,
                },
                {
                    "name": "fig-group",
                    "type": FigGroup,
                },
                {
                    "name": "graphic",
                    "type": Graphic,
                },
                {
                    "name": "media",
                    "type": Media,
                },
                {
                    "name": "preformat",
                    "type": ForwardRef("Preformat"),
                },
                {
                    "name": "question",
                    "type": ForwardRef("Question"),
                },
                {
                    "name": "question-wrap",
                    "type": ForwardRef("QuestionWrap"),
                },
                {
                    "name": "question-wrap-group",
                    "type": ForwardRef("QuestionWrapGroup"),
                },
                {
                    "name": "supplementary-material",
                    "type": ForwardRef("SupplementaryMaterial"),
                },
                {
                    "name": "table-wrap",
                    "type": ForwardRef("TableWrap"),
                },
                {
                    "name": "table-wrap-group",
                    "type": ForwardRef("TableWrapGroup"),
                },
                {
                    "name": "disp-formula",
                    "type": DispFormula,
                },
                {
                    "name": "disp-formula-group",
                    "type": DispFormulaGroup,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "def-list",
                    "type": DefList,
                },
                {
                    "name": "list",
                    "type": List,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": ForwardRef("NamedContent"),
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
                {
                    "name": "disp-quote",
                    "type": DispQuote,
                },
                {
                    "name": "speech",
                    "type": ForwardRef("Speech"),
                },
                {
                    "name": "statement",
                    "type": ForwardRef("Statement"),
                },
                {
                    "name": "verse-group",
                    "type": ForwardRef("VerseGroup"),
                },
            ),
        },
    )


@dataclass
class Option:
    """
    <div> <h3>Option Elements</h3> </div>
    """

    class Meta:
        name = "option"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    subtitle: list["Subtitle"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alt_title: list[AltTitle] = field(
        default_factory=list,
        metadata={
            "name": "alt-title",
            "type": "Element",
        },
    )
    sec: list["Sec"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer_set: list[AnswerSet] = field(
        default_factory=list,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list[BlockAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list[BoxedText] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list[Fig] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list[FigGroup] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list[Graphic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list[Media] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list["Preformat"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question: list["Question"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question_wrap: list["QuestionWrap"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
        },
    )
    question_wrap_group: list["QuestionWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap-group",
            "type": "Element",
        },
    )
    supplementary_material: list["SupplementaryMaterial"] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list["TableWrap"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list["TableWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list[DispFormulaGroup] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    p: list["P"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    related_article: list["RelatedArticle"] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list["RelatedObject"] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    disp_quote: list[DispQuote] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list["Speech"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list["Statement"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list["VerseGroup"] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    fn_group: list[FnGroup] = field(
        default_factory=list,
        metadata={
            "name": "fn-group",
            "type": "Element",
        },
    )
    glossary: list[Glossary] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ref_list: list["RefList"] = field(
        default_factory=list,
        metadata={
            "name": "ref-list",
            "type": "Element",
        },
    )
    explanation: list[Explanation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    correct: Optional[OptionCorrect] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Overline:
    """
    <div> <h3>Overline</h3> </div>
    """

    class Meta:
        name = "overline"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    toggle: Optional[OverlineToggle] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": ForwardRef("RelatedArticle"),
                },
                {
                    "name": "related-object",
                    "type": ForwardRef("RelatedObject"),
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": ForwardRef("Overline"),
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class P:
    """
    <div> <h3>Paragraph</h3> </div>
    """

    class Meta:
        name = "p"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": ForwardRef("RelatedArticle"),
                },
                {
                    "name": "related-object",
                    "type": ForwardRef("RelatedObject"),
                },
                {
                    "name": "address",
                    "type": Address,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "answer",
                    "type": Answer,
                },
                {
                    "name": "answer-set",
                    "type": AnswerSet,
                },
                {
                    "name": "array",
                    "type": Array,
                },
                {
                    "name": "block-alternatives",
                    "type": BlockAlternatives,
                },
                {
                    "name": "boxed-text",
                    "type": BoxedText,
                },
                {
                    "name": "chem-struct-wrap",
                    "type": ChemStructWrap,
                },
                {
                    "name": "code",
                    "type": Code,
                },
                {
                    "name": "explanation",
                    "type": Explanation,
                },
                {
                    "name": "fig",
                    "type": Fig,
                },
                {
                    "name": "fig-group",
                    "type": FigGroup,
                },
                {
                    "name": "graphic",
                    "type": Graphic,
                },
                {
                    "name": "media",
                    "type": Media,
                },
                {
                    "name": "preformat",
                    "type": ForwardRef("Preformat"),
                },
                {
                    "name": "question",
                    "type": ForwardRef("Question"),
                },
                {
                    "name": "question-wrap",
                    "type": ForwardRef("QuestionWrap"),
                },
                {
                    "name": "question-wrap-group",
                    "type": ForwardRef("QuestionWrapGroup"),
                },
                {
                    "name": "supplementary-material",
                    "type": ForwardRef("SupplementaryMaterial"),
                },
                {
                    "name": "table-wrap",
                    "type": ForwardRef("TableWrap"),
                },
                {
                    "name": "table-wrap-group",
                    "type": ForwardRef("TableWrapGroup"),
                },
                {
                    "name": "disp-formula",
                    "type": DispFormula,
                },
                {
                    "name": "disp-formula-group",
                    "type": DispFormulaGroup,
                },
                {
                    "name": "citation-alternatives",
                    "type": CitationAlternatives,
                },
                {
                    "name": "element-citation",
                    "type": ElementCitation,
                },
                {
                    "name": "mixed-citation",
                    "type": MixedCitation,
                },
                {
                    "name": "nlm-citation",
                    "type": NlmCitation,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "award-id",
                    "type": AwardId,
                },
                {
                    "name": "funding-source",
                    "type": FundingSource,
                },
                {
                    "name": "open-access",
                    "type": OpenAccess,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "def-list",
                    "type": DefList,
                },
                {
                    "name": "list",
                    "type": List,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "disp-quote",
                    "type": DispQuote,
                },
                {
                    "name": "speech",
                    "type": ForwardRef("Speech"),
                },
                {
                    "name": "statement",
                    "type": ForwardRef("Statement"),
                },
                {
                    "name": "verse-group",
                    "type": ForwardRef("VerseGroup"),
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class PartTitle:
    """
    <div> <h3>Part Title in a Citation</h3> </div>
    """

    class Meta:
        name = "part-title"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class Preformat:
    """
    <div> <h3>Preformatted Text</h3> </div>
    """

    class Meta:
        name = "preformat"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    orientation: PreformatOrientation = field(
        default=PreformatOrientation.PORTRAIT,
        metadata={
            "type": "Attribute",
        },
    )
    position: PreformatPosition = field(
        default=PreformatPosition.FLOAT,
        metadata={
            "type": "Attribute",
        },
    )
    preformat_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "preformat-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    space: SpaceValue = field(
        init=False,
        default=SpaceValue.PRESERVE,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "alt-text",
                    "type": AltText,
                },
                {
                    "name": "long-desc",
                    "type": LongDesc,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "attrib",
                    "type": Attrib,
                },
                {
                    "name": "permissions",
                    "type": Permissions,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": ForwardRef("Ruby"),
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class Rb:
    """
    <div> <h3>Ruby Base</h3> </div>
    """

    class Meta:
        name = "rb"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
            ),
        },
    )


@dataclass
class Question:
    """
    <div> <h3>Question</h3> </div>
    """

    class Meta:
        name = "question"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    sec_meta: Optional["SecMeta"] = field(
        default=None,
        metadata={
            "name": "sec-meta",
            "type": "Element",
        },
    )
    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    subtitle: list["Subtitle"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alt_title: list[AltTitle] = field(
        default_factory=list,
        metadata={
            "name": "alt-title",
            "type": "Element",
        },
    )
    sec: list["Sec"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer_set: list[AnswerSet] = field(
        default_factory=list,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list[BlockAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list[BoxedText] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    explanation: list[Explanation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list[Fig] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list[FigGroup] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list[Graphic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list[Media] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list[Preformat] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question: list["Question"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question_wrap: list["QuestionWrap"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
        },
    )
    question_wrap_group: list["QuestionWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap-group",
            "type": "Element",
        },
    )
    supplementary_material: list["SupplementaryMaterial"] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list["TableWrap"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list["TableWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list[DispFormulaGroup] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    related_article: list["RelatedArticle"] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list["RelatedObject"] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    disp_quote: list[DispQuote] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list["Speech"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list["Statement"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list["VerseGroup"] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    option: list[Option] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fn_group: list[FnGroup] = field(
        default_factory=list,
        metadata={
            "name": "fn-group",
            "type": "Element",
        },
    )
    glossary: list[Glossary] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ref_list: list["RefList"] = field(
        default_factory=list,
        metadata={
            "name": "ref-list",
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    question_response_type: Optional[QuestionQuestionResponseType] = field(
        default=None,
        metadata={
            "name": "question-response-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Ruby:
    """
    <div> <h3>Ruby Wrapper</h3> </div>
    """

    class Meta:
        name = "ruby"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    rb: Optional[Rb] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    rt: Optional[Rt] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Speech:
    """
    <div> <h3>Speech</h3> </div>
    """

    class Meta:
        name = "speech"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    speaker: Optional[Speaker] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Statement:
    """
    <div> <h3>Statement, Formal</h3> </div>
    """

    class Meta:
        name = "statement"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    abstract: list[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    kwd_group: list[KwdGroup] = field(
        default_factory=list,
        metadata={
            "name": "kwd-group",
            "type": "Element",
        },
    )
    subj_group: list["SubjGroup"] = field(
        default_factory=list,
        metadata={
            "name": "subj-group",
            "type": "Element",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list["Statement"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    attrib: list[Attrib] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    permissions: list[Permissions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class SupportDescription:
    """
    <div> <h3>Support Description</h3> </div>
    """

    class Meta:
        name = "support-description"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class QuestionWrap:
    """
    <div> <h3>Question Wrap</h3> </div>
    """

    class Meta:
        name = "question-wrap"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    question: Optional[Question] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    answer: Optional[Answer] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    answer_set: Optional[AnswerSet] = field(
        default=None,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    explanation: list[Explanation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    audience: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class RelatedArticle:
    """
    <div> <h3>Related Article Information</h3> </div>
    """

    class Meta:
        name = "related-article"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    elocation_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "elocation-id",
            "type": "Attribute",
        },
    )
    ext_link_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ext-link-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    issue: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    journal_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "journal-id",
            "type": "Attribute",
        },
    )
    journal_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "journal-id-type",
            "type": "Attribute",
        },
    )
    page: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    related_article_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "related-article-type",
            "type": "Attribute",
            "required": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    vol: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "journal-id",
                    "type": JournalId,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "annotation",
                    "type": Annotation,
                },
                {
                    "name": "article-title",
                    "type": ArticleTitle,
                },
                {
                    "name": "chapter-title",
                    "type": ChapterTitle,
                },
                {
                    "name": "collab",
                    "type": Collab,
                },
                {
                    "name": "collab-alternatives",
                    "type": CollabAlternatives,
                },
                {
                    "name": "comment",
                    "type": Comment,
                },
                {
                    "name": "conf-acronym",
                    "type": ConfAcronym,
                },
                {
                    "name": "conf-date",
                    "type": ConfDate,
                },
                {
                    "name": "conf-loc",
                    "type": ConfLoc,
                },
                {
                    "name": "conf-name",
                    "type": ConfName,
                },
                {
                    "name": "conf-sponsor",
                    "type": ConfSponsor,
                },
                {
                    "name": "data-title",
                    "type": DataTitle,
                },
                {
                    "name": "date",
                    "type": Date,
                },
                {
                    "name": "date-in-citation",
                    "type": DateInCitation,
                },
                {
                    "name": "day",
                    "type": Day,
                },
                {
                    "name": "edition",
                    "type": Edition,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "elocation-id",
                    "type": ElocationId,
                },
                {
                    "name": "etal",
                    "type": Etal,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "fpage",
                    "type": Fpage,
                },
                {
                    "name": "gov",
                    "type": Gov,
                },
                {
                    "name": "institution",
                    "type": Institution,
                },
                {
                    "name": "institution-wrap",
                    "type": InstitutionWrap,
                },
                {
                    "name": "isbn",
                    "type": Isbn,
                },
                {
                    "name": "issn",
                    "type": Issn,
                },
                {
                    "name": "issn-l",
                    "type": IssnL,
                },
                {
                    "name": "issue",
                    "type": Issue,
                },
                {
                    "name": "issue-id",
                    "type": IssueId,
                },
                {
                    "name": "issue-part",
                    "type": IssuePart,
                },
                {
                    "name": "issue-title",
                    "type": IssueTitle,
                },
                {
                    "name": "lpage",
                    "type": Lpage,
                },
                {
                    "name": "month",
                    "type": Month,
                },
                {
                    "name": "name",
                    "type": Name,
                },
                {
                    "name": "name-alternatives",
                    "type": NameAlternatives,
                },
                {
                    "name": "object-id",
                    "type": ObjectId,
                },
                {
                    "name": "page-range",
                    "type": PageRange,
                },
                {
                    "name": "part-title",
                    "type": PartTitle,
                },
                {
                    "name": "patent",
                    "type": Patent,
                },
                {
                    "name": "person-group",
                    "type": PersonGroup,
                },
                {
                    "name": "pub-id",
                    "type": PubId,
                },
                {
                    "name": "publisher-loc",
                    "type": PublisherLoc,
                },
                {
                    "name": "publisher-name",
                    "type": PublisherName,
                },
                {
                    "name": "role",
                    "type": ForwardRef("Role"),
                },
                {
                    "name": "season",
                    "type": Season,
                },
                {
                    "name": "series",
                    "type": ForwardRef("Series"),
                },
                {
                    "name": "size",
                    "type": Size,
                },
                {
                    "name": "source",
                    "type": ForwardRef("Source"),
                },
                {
                    "name": "std",
                    "type": ForwardRef("Std"),
                },
                {
                    "name": "string-date",
                    "type": StringDate,
                },
                {
                    "name": "string-name",
                    "type": StringName,
                },
                {
                    "name": "supplement",
                    "type": ForwardRef("Supplement"),
                },
                {
                    "name": "trans-source",
                    "type": ForwardRef("TransSource"),
                },
                {
                    "name": "trans-title",
                    "type": ForwardRef("TransTitle"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "version",
                    "type": ForwardRef("Version"),
                },
                {
                    "name": "volume",
                    "type": Volume,
                },
                {
                    "name": "volume-id",
                    "type": VolumeId,
                },
                {
                    "name": "volume-series",
                    "type": VolumeSeries,
                },
                {
                    "name": "year",
                    "type": Year,
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class RelatedObject:
    """
    <div> <h3>Related Object Information</h3> </div>
    """

    class Meta:
        name = "related-object"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    document_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "document-id",
            "type": "Attribute",
        },
    )
    document_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "document-id-type",
            "type": "Attribute",
        },
    )
    document_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "document-type",
            "type": "Attribute",
        },
    )
    ext_link_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ext-link-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    link_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "link-type",
            "type": "Attribute",
        },
    )
    object_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "object-id",
            "type": "Attribute",
        },
    )
    object_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "object-id-type",
            "type": "Attribute",
        },
    )
    object_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "object-type",
            "type": "Attribute",
        },
    )
    source_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "source-id",
            "type": "Attribute",
        },
    )
    source_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "source-id-type",
            "type": "Attribute",
        },
    )
    source_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "source-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "annotation",
                    "type": Annotation,
                },
                {
                    "name": "article-title",
                    "type": ArticleTitle,
                },
                {
                    "name": "chapter-title",
                    "type": ChapterTitle,
                },
                {
                    "name": "collab",
                    "type": Collab,
                },
                {
                    "name": "collab-alternatives",
                    "type": CollabAlternatives,
                },
                {
                    "name": "comment",
                    "type": Comment,
                },
                {
                    "name": "conf-acronym",
                    "type": ConfAcronym,
                },
                {
                    "name": "conf-date",
                    "type": ConfDate,
                },
                {
                    "name": "conf-loc",
                    "type": ConfLoc,
                },
                {
                    "name": "conf-name",
                    "type": ConfName,
                },
                {
                    "name": "conf-sponsor",
                    "type": ConfSponsor,
                },
                {
                    "name": "data-title",
                    "type": DataTitle,
                },
                {
                    "name": "date",
                    "type": Date,
                },
                {
                    "name": "date-in-citation",
                    "type": DateInCitation,
                },
                {
                    "name": "day",
                    "type": Day,
                },
                {
                    "name": "edition",
                    "type": Edition,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "elocation-id",
                    "type": ElocationId,
                },
                {
                    "name": "etal",
                    "type": Etal,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "fpage",
                    "type": Fpage,
                },
                {
                    "name": "gov",
                    "type": Gov,
                },
                {
                    "name": "institution",
                    "type": Institution,
                },
                {
                    "name": "institution-wrap",
                    "type": InstitutionWrap,
                },
                {
                    "name": "isbn",
                    "type": Isbn,
                },
                {
                    "name": "issn",
                    "type": Issn,
                },
                {
                    "name": "issn-l",
                    "type": IssnL,
                },
                {
                    "name": "issue",
                    "type": Issue,
                },
                {
                    "name": "issue-id",
                    "type": IssueId,
                },
                {
                    "name": "issue-part",
                    "type": IssuePart,
                },
                {
                    "name": "issue-title",
                    "type": IssueTitle,
                },
                {
                    "name": "lpage",
                    "type": Lpage,
                },
                {
                    "name": "month",
                    "type": Month,
                },
                {
                    "name": "name",
                    "type": Name,
                },
                {
                    "name": "name-alternatives",
                    "type": NameAlternatives,
                },
                {
                    "name": "object-id",
                    "type": ObjectId,
                },
                {
                    "name": "page-range",
                    "type": PageRange,
                },
                {
                    "name": "part-title",
                    "type": PartTitle,
                },
                {
                    "name": "patent",
                    "type": Patent,
                },
                {
                    "name": "person-group",
                    "type": PersonGroup,
                },
                {
                    "name": "pub-id",
                    "type": PubId,
                },
                {
                    "name": "publisher-loc",
                    "type": PublisherLoc,
                },
                {
                    "name": "publisher-name",
                    "type": PublisherName,
                },
                {
                    "name": "role",
                    "type": ForwardRef("Role"),
                },
                {
                    "name": "season",
                    "type": Season,
                },
                {
                    "name": "series",
                    "type": ForwardRef("Series"),
                },
                {
                    "name": "size",
                    "type": Size,
                },
                {
                    "name": "source",
                    "type": ForwardRef("Source"),
                },
                {
                    "name": "std",
                    "type": ForwardRef("Std"),
                },
                {
                    "name": "string-date",
                    "type": StringDate,
                },
                {
                    "name": "string-name",
                    "type": StringName,
                },
                {
                    "name": "supplement",
                    "type": ForwardRef("Supplement"),
                },
                {
                    "name": "trans-source",
                    "type": ForwardRef("TransSource"),
                },
                {
                    "name": "trans-title",
                    "type": ForwardRef("TransTitle"),
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "version",
                    "type": ForwardRef("Version"),
                },
                {
                    "name": "volume",
                    "type": Volume,
                },
                {
                    "name": "volume-id",
                    "type": VolumeId,
                },
                {
                    "name": "volume-series",
                    "type": VolumeSeries,
                },
                {
                    "name": "year",
                    "type": Year,
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class QuestionPreamble:
    """
    <div> <h3>Question Preamble</h3> </div>
    """

    class Meta:
        name = "question-preamble"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    subtitle: list["Subtitle"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alt_title: list[AltTitle] = field(
        default_factory=list,
        metadata={
            "name": "alt-title",
            "type": "Element",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer_set: list[AnswerSet] = field(
        default_factory=list,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list[BlockAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list[BoxedText] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    explanation: list[Explanation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list[Fig] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list[FigGroup] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list[Graphic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list[Media] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list[Preformat] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question: list[Question] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question_wrap: list[QuestionWrap] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
        },
    )
    question_wrap_group: list["QuestionWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap-group",
            "type": "Element",
        },
    )
    supplementary_material: list["SupplementaryMaterial"] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list["TableWrap"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list["TableWrapGroup"] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list[DispFormulaGroup] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    related_article: list["RelatedArticle"] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list["RelatedObject"] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    disp_quote: list[DispQuote] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list["Speech"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list["Statement"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list["VerseGroup"] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    sec: list["Sec"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Roman:
    """
    <div> <h3>Roman</h3> </div>
    """

    class Meta:
        name = "roman"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    toggle: RomanToggle = field(
        default=RomanToggle.NO,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": ForwardRef("Roman"),
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class QuestionWrapGroup:
    """
    <div> <h3>Question Wrap Group</h3> </div>
    """

    class Meta:
        name = "question-wrap-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional["Title"] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    subtitle: list["Subtitle"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alt_title: list[AltTitle] = field(
        default_factory=list,
        metadata={
            "name": "alt-title",
            "type": "Element",
        },
    )
    question_preamble: Optional[QuestionPreamble] = field(
        default=None,
        metadata={
            "name": "question-preamble",
            "type": "Element",
        },
    )
    question_wrap: list[QuestionWrap] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    audience: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class SansSerif:
    """
    <div> <h3>Sans Serif</h3> </div>
    """

    class Meta:
        name = "sans-serif"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    toggle: Optional[SansSerifToggle] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": ForwardRef("SansSerif"),
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class Sc:
    """
    <div> <h3>Small Caps</h3> </div>
    """

    class Meta:
        name = "sc"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    toggle: Optional[ScToggle] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": ForwardRef("Sc"),
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class Strike:
    """
    <div> <h3>Strike Through</h3> </div>
    """

    class Meta:
        name = "strike"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    toggle: Optional[StrikeToggle] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": ForwardRef("Strike"),
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class StyledContent:
    """
    <div> <h3>Styled Special (Subject) Content</h3> </div>
    """

    class Meta:
        name = "styled-content"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    alt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    style_detail: Optional[str] = field(
        default=None,
        metadata={
            "name": "style-detail",
            "type": "Attribute",
        },
    )
    style_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "style-type",
            "type": "Attribute",
        },
    )
    toggle: Optional[StyledContentToggle] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "address",
                    "type": Address,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "answer",
                    "type": Answer,
                },
                {
                    "name": "answer-set",
                    "type": AnswerSet,
                },
                {
                    "name": "array",
                    "type": Array,
                },
                {
                    "name": "block-alternatives",
                    "type": BlockAlternatives,
                },
                {
                    "name": "boxed-text",
                    "type": BoxedText,
                },
                {
                    "name": "chem-struct-wrap",
                    "type": ChemStructWrap,
                },
                {
                    "name": "code",
                    "type": Code,
                },
                {
                    "name": "explanation",
                    "type": Explanation,
                },
                {
                    "name": "fig",
                    "type": Fig,
                },
                {
                    "name": "fig-group",
                    "type": FigGroup,
                },
                {
                    "name": "graphic",
                    "type": Graphic,
                },
                {
                    "name": "media",
                    "type": Media,
                },
                {
                    "name": "preformat",
                    "type": Preformat,
                },
                {
                    "name": "question",
                    "type": Question,
                },
                {
                    "name": "question-wrap",
                    "type": QuestionWrap,
                },
                {
                    "name": "question-wrap-group",
                    "type": QuestionWrapGroup,
                },
                {
                    "name": "supplementary-material",
                    "type": ForwardRef("SupplementaryMaterial"),
                },
                {
                    "name": "table-wrap",
                    "type": ForwardRef("TableWrap"),
                },
                {
                    "name": "table-wrap-group",
                    "type": ForwardRef("TableWrapGroup"),
                },
                {
                    "name": "disp-formula",
                    "type": DispFormula,
                },
                {
                    "name": "disp-formula-group",
                    "type": DispFormulaGroup,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "def-list",
                    "type": DefList,
                },
                {
                    "name": "list",
                    "type": List,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": ForwardRef("StyledContent"),
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
                {
                    "name": "disp-quote",
                    "type": DispQuote,
                },
                {
                    "name": "speech",
                    "type": Speech,
                },
                {
                    "name": "statement",
                    "type": Statement,
                },
                {
                    "name": "verse-group",
                    "type": ForwardRef("VerseGroup"),
                },
            ),
        },
    )


@dataclass
class Sub:
    """
    <div> <h3>Subscript</h3> </div>
    """

    class Meta:
        name = "sub"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    arrange: Optional[SubArrange] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class Sup:
    """
    <div> <h3>Superscript</h3> </div>
    """

    class Meta:
        name = "sup"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    arrange: Optional[SupArrange] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": ForwardRef("Target"),
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                },
            ),
        },
    )


@dataclass
class StdOrganization:
    """
    <div> <h3>Standards Organization</h3> </div>
    """

    class Meta:
        name = "std-organization"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "institution",
                    "type": Institution,
                },
                {
                    "name": "institution-wrap",
                    "type": InstitutionWrap,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class Target:
    """
    <div> <h3>Target of an Internal Link</h3> </div>
    """

    class Meta:
        name = "target"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    target_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "target-type",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class Version:
    """
    <div> <h3>Version Statement, Cited</h3> </div>
    """

    class Meta:
        name = "version"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    designator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class Underline:
    """
    <div> <h3>Underline</h3> </div>
    """

    class Meta:
        name = "underline"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    toggle: Optional[UnderlineToggle] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    underline_style: Optional[str] = field(
        default=None,
        metadata={
            "name": "underline-style",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": ForwardRef("Underline"),
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": ForwardRef("Xref"),
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class CompoundSubjectPart:
    """
    <div> <h3>Compound Subject Part Name</h3> </div>
    """

    class Meta:
        name = "compound-subject-part"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class ConfTheme:
    """
    <div> <h3>Conference Theme</h3> </div>
    """

    class Meta:
        name = "conf-theme"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class Corresp:
    """
    <div> <h3>Correspondence Information</h3> </div>
    """

    class Meta:
        name = "corresp"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "addr-line",
                    "type": AddrLine,
                },
                {
                    "name": "city",
                    "type": City,
                },
                {
                    "name": "country",
                    "type": Country,
                },
                {
                    "name": "fax",
                    "type": Fax,
                },
                {
                    "name": "institution",
                    "type": Institution,
                },
                {
                    "name": "institution-wrap",
                    "type": InstitutionWrap,
                },
                {
                    "name": "phone",
                    "type": Phone,
                },
                {
                    "name": "postal-code",
                    "type": PostalCode,
                },
                {
                    "name": "state",
                    "type": State,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "label",
                    "type": Label,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class FundingStatement:
    """
    <div> <h3>Funding Statement</h3> </div>
    """

    class Meta:
        name = "funding-statement"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class Price:
    """
    <div> <h3>Price</h3> </div>
    """

    class Meta:
        name = "price"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    currency: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
            ),
        },
    )


@dataclass
class ResourceName:
    """
    <div> <h3>Resource Name</h3> </div>
    """

    class Meta:
        name = "resource-name"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class Role:
    """
    <div> <h3>Role or Function Title of Contributor</h3> </div>
    """

    class Meta:
        name = "role"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    degree_contribution: Optional[str] = field(
        default=None,
        metadata={
            "name": "degree-contribution",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    vocab_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term",
            "type": "Attribute",
        },
    )
    vocab_term_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term-identifier",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
            ),
        },
    )


@dataclass
class Series:
    """
    <div> <h3>Series</h3> </div>
    """

    class Meta:
        name = "series"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
            ),
        },
    )


@dataclass
class SeriesText:
    """
    <div> <h3>Series Text: Header Text to Describe</h3> </div>
    """

    class Meta:
        name = "series-text"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
            ),
        },
    )


@dataclass
class SeriesTitle:
    """
    <div> <h3>Series Title</h3> </div>
    """

    class Meta:
        name = "series-title"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
            ),
        },
    )


@dataclass
class Sig:
    """
    <div> <h3>Signature</h3> </div>
    """

    class Meta:
        name = "sig"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "break",
                    "type": Break,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "graphic",
                    "type": Graphic,
                },
                {
                    "name": "media",
                    "type": Media,
                },
            ),
        },
    )


@dataclass
class Subject:
    """
    <div> <h3>Subject Name</h3> </div>
    """

    class Meta:
        name = "subject"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    vocab_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term",
            "type": "Attribute",
        },
    )
    vocab_term_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term-identifier",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class SupportSource:
    """
    <div> <h3>Support Source</h3> </div>
    """

    class Meta:
        name = "support-source"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    country: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    support_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "support-type",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "institution",
                    "type": Institution,
                },
                {
                    "name": "institution-wrap",
                    "type": InstitutionWrap,
                },
            ),
        },
    )


@dataclass
class TextualForm:
    """
    <div> <h3>Textual Form</h3> </div>
    """

    class Meta:
        name = "textual-form"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class Xref:
    """
    <div> <h3>X(cross) Reference</h3> </div>
    """

    class Meta:
        name = "xref"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    alt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    custom_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "custom-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    ref_type: Optional[XrefRefType] = field(
        default=None,
        metadata={
            "name": "ref-type",
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class AwardGroup:
    """
    <div> <h3>Award Group</h3> </div>
    """

    class Meta:
        name = "award-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    funding_source: list[FundingSource] = field(
        default_factory=list,
        metadata={
            "name": "funding-source",
            "type": "Element",
        },
    )
    support_source: list[SupportSource] = field(
        default_factory=list,
        metadata={
            "name": "support-source",
            "type": "Element",
        },
    )
    award_id: list[AwardId] = field(
        default_factory=list,
        metadata={
            "name": "award-id",
            "type": "Element",
        },
    )
    award_name: Optional[AwardName] = field(
        default=None,
        metadata={
            "name": "award-name",
            "type": "Element",
        },
    )
    award_desc: Optional[AwardDesc] = field(
        default=None,
        metadata={
            "name": "award-desc",
            "type": "Element",
        },
    )
    principal_award_recipient: list[PrincipalAwardRecipient] = field(
        default_factory=list,
        metadata={
            "name": "principal-award-recipient",
            "type": "Element",
        },
    )
    principal_investigator: list[PrincipalInvestigator] = field(
        default_factory=list,
        metadata={
            "name": "principal-investigator",
            "type": "Element",
        },
    )
    award_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "award-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class CompoundKwdPart:
    """
    <div> <h3>Compound Keyword Part</h3> </div>
    """

    class Meta:
        name = "compound-kwd-part"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class Conference:
    """
    <div> <h3>Conference Information</h3> </div>
    """

    class Meta:
        name = "conference"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    conf_date: Optional[ConfDate] = field(
        default=None,
        metadata={
            "name": "conf-date",
            "type": "Element",
            "required": True,
        },
    )
    conf_name: list[ConfName] = field(
        default_factory=list,
        metadata={
            "name": "conf-name",
            "type": "Element",
        },
    )
    conf_acronym: list[ConfAcronym] = field(
        default_factory=list,
        metadata={
            "name": "conf-acronym",
            "type": "Element",
        },
    )
    conf_num: Optional[ConfNum] = field(
        default=None,
        metadata={
            "name": "conf-num",
            "type": "Element",
        },
    )
    conf_loc: Optional[ConfLoc] = field(
        default=None,
        metadata={
            "name": "conf-loc",
            "type": "Element",
        },
    )
    conf_sponsor: list[ConfSponsor] = field(
        default_factory=list,
        metadata={
            "name": "conf-sponsor",
            "type": "Element",
        },
    )
    conf_theme: Optional[ConfTheme] = field(
        default=None,
        metadata={
            "name": "conf-theme",
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class MetaValue:
    """
    <div> <h3>Metadata Data Value For Custom Metadata</h3> </div>
    """

    class Meta:
        name = "meta-value"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class OnBehalfOf:
    """
    <div> <h3>On Behalf of</h3> </div>
    """

    class Meta:
        name = "on-behalf-of"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "institution",
                    "type": Institution,
                },
                {
                    "name": "institution-wrap",
                    "type": InstitutionWrap,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
            ),
        },
    )


@dataclass
class ResourceWrap:
    """
    <div> <h3>Resource Wrap</h3> </div>
    """

    class Meta:
        name = "resource-wrap"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    resource_name: Optional[ResourceName] = field(
        default=None,
        metadata={
            "name": "resource-name",
            "type": "Element",
            "required": True,
        },
    )
    resource_id: list[ResourceId] = field(
        default_factory=list,
        metadata={
            "name": "resource-id",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class See:
    """
    <div> <h3>See</h3> </div>
    """

    class Meta:
        name = "see"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "disp-formula",
                    "type": DispFormula,
                },
                {
                    "name": "disp-formula-group",
                    "type": DispFormulaGroup,
                },
                {
                    "name": "array",
                    "type": Array,
                },
                {
                    "name": "code",
                    "type": Code,
                },
                {
                    "name": "graphic",
                    "type": Graphic,
                },
                {
                    "name": "media",
                    "type": Media,
                },
                {
                    "name": "preformat",
                    "type": Preformat,
                },
            ),
        },
    )


@dataclass
class SeeAlso:
    """
    <div> <h3>See-Also Term</h3> </div>
    """

    class Meta:
        name = "see-also"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    vocab_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term",
            "type": "Attribute",
        },
    )
    vocab_term_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term-identifier",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "disp-formula",
                    "type": DispFormula,
                },
                {
                    "name": "disp-formula-group",
                    "type": DispFormulaGroup,
                },
                {
                    "name": "array",
                    "type": Array,
                },
                {
                    "name": "code",
                    "type": Code,
                },
                {
                    "name": "graphic",
                    "type": Graphic,
                },
                {
                    "name": "media",
                    "type": Media,
                },
                {
                    "name": "preformat",
                    "type": Preformat,
                },
            ),
        },
    )


@dataclass
class SigBlock:
    """
    <div> <h3>Signature Block</h3> </div>
    """

    class Meta:
        name = "sig-block"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "break",
                    "type": Break,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "graphic",
                    "type": Graphic,
                },
                {
                    "name": "media",
                    "type": Media,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "sig",
                    "type": Sig,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class Source:
    """
    <div> <h3>Source</h3> </div>
    """

    class Meta:
        name = "source"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class StringConf:
    """
    <div> <h3>String Conference Name</h3> </div>
    """

    class Meta:
        name = "string-conf"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "conf-date",
                    "type": ConfDate,
                },
                {
                    "name": "conf-name",
                    "type": ConfName,
                },
                {
                    "name": "conf-num",
                    "type": ConfNum,
                },
                {
                    "name": "conf-loc",
                    "type": ConfLoc,
                },
                {
                    "name": "conf-sponsor",
                    "type": ConfSponsor,
                },
                {
                    "name": "conf-theme",
                    "type": ConfTheme,
                },
                {
                    "name": "conf-acronym",
                    "type": ConfAcronym,
                },
                {
                    "name": "string-conf",
                    "type": ForwardRef("StringConf"),
                },
            ),
        },
    )


@dataclass
class SubjGroup:
    class Meta:
        name = "subj-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    subject: list[Subject] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    compound_subject: list[CompoundSubject] = field(
        default_factory=list,
        metadata={
            "name": "compound-subject",
            "type": "Element",
        },
    )
    subj_group: list["SubjGroup"] = field(
        default_factory=list,
        metadata={
            "name": "subj-group",
            "type": "Element",
        },
    )
    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    subj_group_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "subj-group-type",
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Subtitle:
    """
    <div> <h3>Article Subtitle</h3> </div>
    """

    class Meta:
        name = "subtitle"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "break",
                    "type": Break,
                },
            ),
        },
    )


@dataclass
class Term:
    """
    <div> <h3>Definition List: Term</h3> </div>
    """

    class Meta:
        name = "term"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    term_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "term-status",
            "type": "Attribute",
        },
    )
    term_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "term-type",
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    vocab_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term",
            "type": "Attribute",
        },
    )
    vocab_term_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term-identifier",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "disp-formula",
                    "type": DispFormula,
                },
                {
                    "name": "disp-formula-group",
                    "type": DispFormulaGroup,
                },
                {
                    "name": "array",
                    "type": Array,
                },
                {
                    "name": "code",
                    "type": Code,
                },
                {
                    "name": "graphic",
                    "type": Graphic,
                },
                {
                    "name": "media",
                    "type": Media,
                },
                {
                    "name": "preformat",
                    "type": Preformat,
                },
            ),
        },
    )


@dataclass
class TermHead:
    """
    <div> <h3>Definition List: Term Head</h3> </div>
    """

    class Meta:
        name = "term-head"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class Title:
    """
    <div> <h3>Title</h3> </div>
    """

    class Meta:
        name = "title"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "break",
                    "type": Break,
                },
                {
                    "name": "citation-alternatives",
                    "type": CitationAlternatives,
                },
                {
                    "name": "element-citation",
                    "type": ElementCitation,
                },
                {
                    "name": "mixed-citation",
                    "type": MixedCitation,
                },
                {
                    "name": "nlm-citation",
                    "type": NlmCitation,
                },
            ),
        },
    )


@dataclass
class TransSource:
    """
    <div> <h3>Translated Source</h3> </div>
    """

    class Meta:
        name = "trans-source"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class TransSubtitle:
    """
    <div> <h3>Translated Subtitle</h3> </div>
    """

    class Meta:
        name = "trans-subtitle"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "break",
                    "type": Break,
                },
            ),
        },
    )


@dataclass
class TransTitle:
    """
    <div> <h3>Translated Title</h3> </div>
    """

    class Meta:
        name = "trans-title"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "break",
                    "type": Break,
                },
            ),
        },
    )


@dataclass
class VerseLine:
    """
    <div> <h3>Line of a Verse</h3> </div>
    """

    class Meta:
        name = "verse-line"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    indent_level: Optional[str] = field(
        default=None,
        metadata={
            "name": "indent-level",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    style_detail: Optional[str] = field(
        default=None,
        metadata={
            "name": "style-detail",
            "type": "Attribute",
        },
    )
    style_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "style-type",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
            ),
        },
    )


@dataclass
class ArticleCategories:
    """
    <div> <h3>Article Grouping Data</h3> </div>
    """

    class Meta:
        name = "article-categories"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    subj_group: list[SubjGroup] = field(
        default_factory=list,
        metadata={
            "name": "subj-group",
            "type": "Element",
        },
    )
    series_title: list[SeriesTitle] = field(
        default_factory=list,
        metadata={
            "name": "series-title",
            "type": "Element",
        },
    )
    series_text: list[SeriesText] = field(
        default_factory=list,
        metadata={
            "name": "series-text",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class AuthorNotes:
    """
    <div> <h3>Author Note Group</h3> </div>
    """

    class Meta:
        name = "author-notes"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional[Title] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    corresp: list[Corresp] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fn: list[Fn] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rid: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class CustomMeta:
    """
    <div> <h3>Custom Metadata</h3> </div>
    """

    class Meta:
        name = "custom-meta"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    meta_name: Optional[MetaName] = field(
        default=None,
        metadata={
            "name": "meta-name",
            "type": "Element",
            "required": True,
        },
    )
    meta_value: Optional[MetaValue] = field(
        default=None,
        metadata={
            "name": "meta-value",
            "type": "Element",
            "required": True,
        },
    )
    assigning_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "assigning-authority",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    vocab: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    vocab_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-identifier",
            "type": "Attribute",
        },
    )
    vocab_term: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term",
            "type": "Attribute",
        },
    )
    vocab_term_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "vocab-term-identifier",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class FundingGroup:
    """
    <div> <h3>Funding Group</h3> </div>
    """

    class Meta:
        name = "funding-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    award_group: list[AwardGroup] = field(
        default_factory=list,
        metadata={
            "name": "award-group",
            "type": "Element",
        },
    )
    funding_statement: list[FundingStatement] = field(
        default_factory=list,
        metadata={
            "name": "funding-statement",
            "type": "Element",
        },
    )
    open_access: list[OpenAccess] = field(
        default_factory=list,
        metadata={
            "name": "open-access",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class ListItem:
    """
    <div> <h3>List Item</h3> </div>
    """

    class Meta:
        name = "list-item"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional[Title] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class ResourceGroup:
    """
    <div> <h3>Resource Group</h3> </div>
    """

    class Meta:
        name = "resource-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    resource_name: list[ResourceName] = field(
        default_factory=list,
        metadata={
            "name": "resource-name",
            "type": "Element",
        },
    )
    resource_wrap: list[ResourceWrap] = field(
        default_factory=list,
        metadata={
            "name": "resource-wrap",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class SecMeta:
    """
    <div> <h3>Section Metadata</h3> </div>
    """

    class Meta:
        name = "sec-meta"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    contrib_group: list[ContribGroup] = field(
        default_factory=list,
        metadata={
            "name": "contrib-group",
            "type": "Element",
        },
    )
    abstract: list[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    kwd_group: list[KwdGroup] = field(
        default_factory=list,
        metadata={
            "name": "kwd-group",
            "type": "Element",
        },
    )
    subj_group: list[SubjGroup] = field(
        default_factory=list,
        metadata={
            "name": "subj-group",
            "type": "Element",
        },
    )
    permissions: Optional[Permissions] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Std:
    """
    <div> <h3>Standard, Cited</h3> </div>
    """

    class Meta:
        name = "std"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "day",
                    "type": Day,
                },
                {
                    "name": "month",
                    "type": Month,
                },
                {
                    "name": "pub-id",
                    "type": PubId,
                },
                {
                    "name": "source",
                    "type": Source,
                },
                {
                    "name": "std-organization",
                    "type": StdOrganization,
                },
                {
                    "name": "year",
                    "type": Year,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class Supplement:
    """
    <div> <h3>Supplement</h3> </div>
    """

    class Meta:
        name = "supplement"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    supplement_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "supplement-type",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "contrib-group",
                    "type": ContribGroup,
                },
                {
                    "name": "title",
                    "type": Title,
                },
            ),
        },
    )


@dataclass
class TableWrapFoot:
    """
    <div> <h3>Table Wrap Footer</h3> </div>
    """

    class Meta:
        name = "table-wrap-foot"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    title: Optional[Title] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fn_group: list[FnGroup] = field(
        default_factory=list,
        metadata={
            "name": "fn-group",
            "type": "Element",
        },
    )
    fn: list[Fn] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    attrib: list[Attrib] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    permissions: list[Permissions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class TransTitleGroup:
    """
    <div> <h3>Translated Title Group</h3> </div>
    """

    class Meta:
        name = "trans-title-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    trans_title: Optional[TransTitle] = field(
        default=None,
        metadata={
            "name": "trans-title",
            "type": "Element",
            "required": True,
        },
    )
    trans_subtitle: list[TransSubtitle] = field(
        default_factory=list,
        metadata={
            "name": "trans-subtitle",
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class VerseGroup:
    """
    <div> <h3>Verse Form For Poetry</h3> </div>
    """

    class Meta:
        name = "verse-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional[Title] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    subtitle: Optional[Subtitle] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    verse_line: list[VerseLine] = field(
        default_factory=list,
        metadata={
            "name": "verse-line",
            "type": "Element",
        },
    )
    verse_group: list["VerseGroup"] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    attrib: list[Attrib] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    permissions: list[Permissions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    style_detail: Optional[str] = field(
        default=None,
        metadata={
            "name": "style-detail",
            "type": "Attribute",
        },
    )
    style_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "style-type",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class ContributedResourceGroup:
    """
    <div> <h3>Contributed Resource Group</h3> </div>
    """

    class Meta:
        name = "contributed-resource-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    award_group: list[AwardGroup] = field(
        default_factory=list,
        metadata={
            "name": "award-group",
            "type": "Element",
        },
    )
    support_description: list[SupportDescription] = field(
        default_factory=list,
        metadata={
            "name": "support-description",
            "type": "Element",
        },
    )
    resource_group: list[ResourceGroup] = field(
        default_factory=list,
        metadata={
            "name": "resource-group",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    resource_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "resource-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class CustomMetaGroup:
    """
    <div> <h3>Custom Metadata Group</h3> </div>
    """

    class Meta:
        name = "custom-meta-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    custom_meta: list[CustomMeta] = field(
        default_factory=list,
        metadata={
            "name": "custom-meta",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class IssueTitleGroup:
    """
    <div> <h3>Issue Title Group</h3> </div>
    """

    class Meta:
        name = "issue-title-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    issue_title: Optional[IssueTitle] = field(
        default=None,
        metadata={
            "name": "issue-title",
            "type": "Element",
            "required": True,
        },
    )
    issue_subtitle: list[IssueSubtitle] = field(
        default_factory=list,
        metadata={
            "name": "issue-subtitle",
            "type": "Element",
        },
    )
    trans_title_group: list[TransTitleGroup] = field(
        default_factory=list,
        metadata={
            "name": "trans-title-group",
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class JournalTitleGroup:
    """
    <div> <h3>Journal Title Group</h3> </div>
    """

    class Meta:
        name = "journal-title-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    journal_title: list[JournalTitle] = field(
        default_factory=list,
        metadata={
            "name": "journal-title",
            "type": "Element",
        },
    )
    journal_subtitle: list[JournalSubtitle] = field(
        default_factory=list,
        metadata={
            "name": "journal-subtitle",
            "type": "Element",
        },
    )
    trans_title_group: list[TransTitleGroup] = field(
        default_factory=list,
        metadata={
            "name": "trans-title-group",
            "type": "Element",
        },
    )
    abbrev_journal_title: list[AbbrevJournalTitle] = field(
        default_factory=list,
        metadata={
            "name": "abbrev-journal-title",
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Product:
    """
    <div> <h3>Product Information</h3> </div>
    """

    class Meta:
        name = "product"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    product_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "product-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "break",
                    "type": Break,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "price",
                    "type": Price,
                },
                {
                    "name": "annotation",
                    "type": Annotation,
                },
                {
                    "name": "article-title",
                    "type": ArticleTitle,
                },
                {
                    "name": "chapter-title",
                    "type": ChapterTitle,
                },
                {
                    "name": "collab",
                    "type": Collab,
                },
                {
                    "name": "collab-alternatives",
                    "type": CollabAlternatives,
                },
                {
                    "name": "comment",
                    "type": Comment,
                },
                {
                    "name": "conf-acronym",
                    "type": ConfAcronym,
                },
                {
                    "name": "conf-date",
                    "type": ConfDate,
                },
                {
                    "name": "conf-loc",
                    "type": ConfLoc,
                },
                {
                    "name": "conf-name",
                    "type": ConfName,
                },
                {
                    "name": "conf-sponsor",
                    "type": ConfSponsor,
                },
                {
                    "name": "data-title",
                    "type": DataTitle,
                },
                {
                    "name": "date",
                    "type": Date,
                },
                {
                    "name": "date-in-citation",
                    "type": DateInCitation,
                },
                {
                    "name": "day",
                    "type": Day,
                },
                {
                    "name": "edition",
                    "type": Edition,
                },
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "elocation-id",
                    "type": ElocationId,
                },
                {
                    "name": "etal",
                    "type": Etal,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "fpage",
                    "type": Fpage,
                },
                {
                    "name": "gov",
                    "type": Gov,
                },
                {
                    "name": "institution",
                    "type": Institution,
                },
                {
                    "name": "institution-wrap",
                    "type": InstitutionWrap,
                },
                {
                    "name": "isbn",
                    "type": Isbn,
                },
                {
                    "name": "issn",
                    "type": Issn,
                },
                {
                    "name": "issn-l",
                    "type": IssnL,
                },
                {
                    "name": "issue",
                    "type": Issue,
                },
                {
                    "name": "issue-id",
                    "type": IssueId,
                },
                {
                    "name": "issue-part",
                    "type": IssuePart,
                },
                {
                    "name": "issue-title",
                    "type": IssueTitle,
                },
                {
                    "name": "lpage",
                    "type": Lpage,
                },
                {
                    "name": "month",
                    "type": Month,
                },
                {
                    "name": "name",
                    "type": Name,
                },
                {
                    "name": "name-alternatives",
                    "type": NameAlternatives,
                },
                {
                    "name": "object-id",
                    "type": ObjectId,
                },
                {
                    "name": "page-range",
                    "type": PageRange,
                },
                {
                    "name": "part-title",
                    "type": PartTitle,
                },
                {
                    "name": "patent",
                    "type": Patent,
                },
                {
                    "name": "person-group",
                    "type": PersonGroup,
                },
                {
                    "name": "pub-id",
                    "type": PubId,
                },
                {
                    "name": "publisher-loc",
                    "type": PublisherLoc,
                },
                {
                    "name": "publisher-name",
                    "type": PublisherName,
                },
                {
                    "name": "role",
                    "type": Role,
                },
                {
                    "name": "season",
                    "type": Season,
                },
                {
                    "name": "series",
                    "type": Series,
                },
                {
                    "name": "size",
                    "type": Size,
                },
                {
                    "name": "source",
                    "type": Source,
                },
                {
                    "name": "std",
                    "type": Std,
                },
                {
                    "name": "string-date",
                    "type": StringDate,
                },
                {
                    "name": "string-name",
                    "type": StringName,
                },
                {
                    "name": "supplement",
                    "type": Supplement,
                },
                {
                    "name": "trans-source",
                    "type": TransSource,
                },
                {
                    "name": "trans-title",
                    "type": TransTitle,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "version",
                    "type": Version,
                },
                {
                    "name": "volume",
                    "type": Volume,
                },
                {
                    "name": "volume-id",
                    "type": VolumeId,
                },
                {
                    "name": "volume-series",
                    "type": VolumeSeries,
                },
                {
                    "name": "year",
                    "type": Year,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class Td:
    class Meta:
        name = "td"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    abbr: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    align: Optional[TdAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    axis: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    colspan: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    headers: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rowspan: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        },
    )
    scope: Optional[TdScope] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    valign: Optional[TdValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "hr",
                    "type": Hr,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "disp-formula",
                    "type": DispFormula,
                },
                {
                    "name": "disp-formula-group",
                    "type": DispFormulaGroup,
                },
                {
                    "name": "break",
                    "type": Break,
                },
                {
                    "name": "citation-alternatives",
                    "type": CitationAlternatives,
                },
                {
                    "name": "element-citation",
                    "type": ElementCitation,
                },
                {
                    "name": "mixed-citation",
                    "type": MixedCitation,
                },
                {
                    "name": "nlm-citation",
                    "type": NlmCitation,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "disp-quote",
                    "type": DispQuote,
                },
                {
                    "name": "speech",
                    "type": Speech,
                },
                {
                    "name": "statement",
                    "type": Statement,
                },
                {
                    "name": "verse-group",
                    "type": VerseGroup,
                },
                {
                    "name": "def-list",
                    "type": DefList,
                },
                {
                    "name": "list",
                    "type": List,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "p",
                    "type": P,
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "array",
                    "type": Array,
                },
                {
                    "name": "code",
                    "type": Code,
                },
                {
                    "name": "graphic",
                    "type": Graphic,
                },
                {
                    "name": "media",
                    "type": Media,
                },
                {
                    "name": "preformat",
                    "type": Preformat,
                },
                {
                    "name": "answer",
                    "type": Answer,
                },
                {
                    "name": "answer-set",
                    "type": AnswerSet,
                },
                {
                    "name": "explanation",
                    "type": Explanation,
                },
                {
                    "name": "question",
                    "type": Question,
                },
                {
                    "name": "question-wrap",
                    "type": QuestionWrap,
                },
                {
                    "name": "question-wrap-group",
                    "type": QuestionWrapGroup,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class Th:
    class Meta:
        name = "th"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    abbr: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    align: Optional[ThAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    axis: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    colspan: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    headers: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rowspan: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        },
    )
    scope: Optional[ThScope] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    valign: Optional[ThValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "hr",
                    "type": Hr,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "disp-formula",
                    "type": DispFormula,
                },
                {
                    "name": "disp-formula-group",
                    "type": DispFormulaGroup,
                },
                {
                    "name": "break",
                    "type": Break,
                },
                {
                    "name": "citation-alternatives",
                    "type": CitationAlternatives,
                },
                {
                    "name": "element-citation",
                    "type": ElementCitation,
                },
                {
                    "name": "mixed-citation",
                    "type": MixedCitation,
                },
                {
                    "name": "nlm-citation",
                    "type": NlmCitation,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "disp-quote",
                    "type": DispQuote,
                },
                {
                    "name": "speech",
                    "type": Speech,
                },
                {
                    "name": "statement",
                    "type": Statement,
                },
                {
                    "name": "verse-group",
                    "type": VerseGroup,
                },
                {
                    "name": "def-list",
                    "type": DefList,
                },
                {
                    "name": "list",
                    "type": List,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "p",
                    "type": P,
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "array",
                    "type": Array,
                },
                {
                    "name": "code",
                    "type": Code,
                },
                {
                    "name": "graphic",
                    "type": Graphic,
                },
                {
                    "name": "media",
                    "type": Media,
                },
                {
                    "name": "preformat",
                    "type": Preformat,
                },
                {
                    "name": "answer",
                    "type": Answer,
                },
                {
                    "name": "answer-set",
                    "type": AnswerSet,
                },
                {
                    "name": "explanation",
                    "type": Explanation,
                },
                {
                    "name": "question",
                    "type": Question,
                },
                {
                    "name": "question-wrap",
                    "type": QuestionWrap,
                },
                {
                    "name": "question-wrap-group",
                    "type": QuestionWrapGroup,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
            ),
        },
    )


@dataclass
class TitleGroup:
    """
    <div> <h3>Title Group</h3> </div>
    """

    class Meta:
        name = "title-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    article_title: Optional[ArticleTitle] = field(
        default=None,
        metadata={
            "name": "article-title",
            "type": "Element",
            "required": True,
        },
    )
    subtitle: list[Subtitle] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    trans_title_group: list[TransTitleGroup] = field(
        default_factory=list,
        metadata={
            "name": "trans-title-group",
            "type": "Element",
        },
    )
    alt_title: list[AltTitle] = field(
        default_factory=list,
        metadata={
            "name": "alt-title",
            "type": "Element",
        },
    )
    fn_group: Optional[FnGroup] = field(
        default=None,
        metadata={
            "name": "fn-group",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class ProcessingMeta:
    """
    <div> <h3>Processing Metadata Model</h3> </div>
    """

    class Meta:
        name = "processing-meta"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    restricted_by: list[RestrictedBy] = field(
        default_factory=list,
        metadata={
            "name": "restricted-by",
            "type": "Element",
        },
    )
    extended_by: list[ExtendedBy] = field(
        default_factory=list,
        metadata={
            "name": "extended-by",
            "type": "Element",
        },
    )
    custom_meta_group: list[CustomMetaGroup] = field(
        default_factory=list,
        metadata={
            "name": "custom-meta-group",
            "type": "Element",
        },
    )
    base_tagset: Optional[ProcessingMetaBaseTagset] = field(
        default=None,
        metadata={
            "name": "base-tagset",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    math_representation: list[str] = field(
        default_factory=list,
        metadata={
            "name": "math-representation",
            "type": "Attribute",
            "tokens": True,
        },
    )
    mathml_version: Optional[ProcessingMetaMathmlVersion] = field(
        default=None,
        metadata={
            "name": "mathml-version",
            "type": "Attribute",
        },
    )
    table_model: Optional[ProcessingMetaTableModel] = field(
        default=None,
        metadata={
            "name": "table-model",
            "type": "Attribute",
        },
    )
    tagset_family: Optional[ProcessingMetaTagsetFamily] = field(
        default=None,
        metadata={
            "name": "tagset-family",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class SupportGroup:
    """
    <div> <h3>Support Group</h3> </div>
    """

    class Meta:
        name = "support-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    funding_group: list[FundingGroup] = field(
        default_factory=list,
        metadata={
            "name": "funding-group",
            "type": "Element",
        },
    )
    contributed_resource_group: list[ContributedResourceGroup] = field(
        default_factory=list,
        metadata={
            "name": "contributed-resource-group",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Tr:
    class Meta:
        name = "tr"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    th: list[Th] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    td: list[Td] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    align: Optional[TrAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    valign: Optional[TrValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class VolumeIssueGroup:
    """
    <div> <h3>Translated Title Group</h3> </div>
    """

    class Meta:
        name = "volume-issue-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    volume: list[Volume] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    volume_id: list[VolumeId] = field(
        default_factory=list,
        metadata={
            "name": "volume-id",
            "type": "Element",
        },
    )
    volume_series: Optional[VolumeSeries] = field(
        default=None,
        metadata={
            "name": "volume-series",
            "type": "Element",
        },
    )
    issue: list[Issue] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    issue_id: list[IssueId] = field(
        default_factory=list,
        metadata={
            "name": "issue-id",
            "type": "Element",
        },
    )
    issue_title: list[IssueTitle] = field(
        default_factory=list,
        metadata={
            "name": "issue-title",
            "type": "Element",
        },
    )
    issue_title_group: list[IssueTitleGroup] = field(
        default_factory=list,
        metadata={
            "name": "issue-title-group",
            "type": "Element",
        },
    )
    issue_sponsor: list[IssueSponsor] = field(
        default_factory=list,
        metadata={
            "name": "issue-sponsor",
            "type": "Element",
        },
    )
    issue_part: Optional[IssuePart] = field(
        default=None,
        metadata={
            "name": "issue-part",
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Tbody:
    class Meta:
        name = "tbody"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    tr: list[Tr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    align: Optional[TbodyAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    valign: Optional[TbodyValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Tfoot:
    class Meta:
        name = "tfoot"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    tr: list[Tr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    align: Optional[TfootAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    valign: Optional[TfootValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Thead:
    class Meta:
        name = "thead"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    tr: list[Tr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    align: Optional[TheadAlign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    char: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    charoff: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    valign: Optional[TheadValign] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Table:
    """
    <div> <h3>Table: Table Element ..............................</h3> </div>
    """

    class Meta:
        name = "table"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    col: list[Col] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    colgroup: list[Colgroup] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    thead: Optional[Thead] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    tfoot: Optional[Tfoot] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    tbody: list[Tbody] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    tr: list[Tr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    border: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    cellpadding: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    cellspacing: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    frame: Optional[TableFrame] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rules: Optional[TableRules] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    summary: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    width: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class TableWrap:
    """
    <div> <h3>Table Wrapper</h3> </div>
    """

    class Meta:
        name = "table-wrap"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: list[Label] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    caption: list[Caption] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    abstract: list[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    kwd_group: list[KwdGroup] = field(
        default_factory=list,
        metadata={
            "name": "kwd-group",
            "type": "Element",
        },
    )
    subj_group: list[SubjGroup] = field(
        default_factory=list,
        metadata={
            "name": "subj-group",
            "type": "Element",
        },
    )
    alt_text: list[AltText] = field(
        default_factory=list,
        metadata={
            "name": "alt-text",
            "type": "Element",
        },
    )
    long_desc: list[LongDesc] = field(
        default_factory=list,
        metadata={
            "name": "long-desc",
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list[ExtLink] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    disp_quote: list[DispQuote] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list[Speech] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list[Statement] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list[VerseGroup] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    graphic: list[Graphic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list[Media] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list[Preformat] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    table: list[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    xref: list[Xref] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    table_wrap_foot: list[TableWrapFoot] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-foot",
            "type": "Element",
        },
    )
    attrib: list[Attrib] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    permissions: list[Permissions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    orientation: TableWrapOrientation = field(
        default=TableWrapOrientation.PORTRAIT,
        metadata={
            "type": "Attribute",
        },
    )
    position: TableWrapPosition = field(
        default=TableWrapPosition.FLOAT,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class SupplementaryMaterial:
    """
    <div> <h3>Supplementary Material</h3> </div>
    """

    class Meta:
        name = "supplementary-material"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: list[Label] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    caption: list[Caption] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    abstract: list[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    kwd_group: list[KwdGroup] = field(
        default_factory=list,
        metadata={
            "name": "kwd-group",
            "type": "Element",
        },
    )
    subj_group: list[SubjGroup] = field(
        default_factory=list,
        metadata={
            "name": "subj-group",
            "type": "Element",
        },
    )
    alt_text: list[AltText] = field(
        default_factory=list,
        metadata={
            "name": "alt-text",
            "type": "Element",
        },
    )
    long_desc: list[LongDesc] = field(
        default_factory=list,
        metadata={
            "name": "long-desc",
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list[ExtLink] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list[DispFormulaGroup] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    disp_quote: list[DispQuote] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list[Speech] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list[Statement] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list[VerseGroup] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    table_wrap: list[TableWrap] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    graphic: list[Graphic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list[Media] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list[Preformat] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    xref: list[Xref] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    attrib: list[Attrib] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    permissions: list[Permissions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    hreflang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    mime_subtype: Optional[str] = field(
        default=None,
        metadata={
            "name": "mime-subtype",
            "type": "Attribute",
        },
    )
    mimetype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    orientation: SupplementaryMaterialOrientation = field(
        default=SupplementaryMaterialOrientation.PORTRAIT,
        metadata={
            "type": "Attribute",
        },
    )
    position: SupplementaryMaterialPosition = field(
        default=SupplementaryMaterialPosition.FLOAT,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    actuate: Optional[ActuateType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    show: Optional[ShowType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class TableWrapGroup:
    """
    <div> <h3>Table Wrapper Group</h3> </div>
    """

    class Meta:
        name = "table-wrap-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: list[Label] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    caption: list[Caption] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    abstract: list[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    kwd_group: list[KwdGroup] = field(
        default_factory=list,
        metadata={
            "name": "kwd-group",
            "type": "Element",
        },
    )
    subj_group: list[SubjGroup] = field(
        default_factory=list,
        metadata={
            "name": "subj-group",
            "type": "Element",
        },
    )
    alt_text: list[AltText] = field(
        default_factory=list,
        metadata={
            "name": "alt-text",
            "type": "Element",
        },
    )
    long_desc: list[LongDesc] = field(
        default_factory=list,
        metadata={
            "name": "long-desc",
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list[ExtLink] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    table_wrap: list[TableWrap] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    xref: list[Xref] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    orientation: TableWrapGroupOrientation = field(
        default=TableWrapGroupOrientation.PORTRAIT,
        metadata={
            "type": "Attribute",
        },
    )
    position: TableWrapGroupPosition = field(
        default=TableWrapGroupPosition.FLOAT,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class FloatsGroup:
    """
    <div> <h3>Floats Group</h3> </div>
    """

    class Meta:
        name = "floats-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list[BlockAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list[BoxedText] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list[Fig] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list[FigGroup] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list[Graphic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list[Media] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list[Preformat] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    supplementary_material: list[SupplementaryMaterial] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list[TableWrap] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list[TableWrapGroup] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class LicenseP:
    """
    <div> <h3>License Paragraph</h3> </div>
    """

    class Meta:
        name = "license-p"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "email",
                    "type": Email,
                },
                {
                    "name": "ext-link",
                    "type": ExtLink,
                },
                {
                    "name": "uri",
                    "type": Uri,
                },
                {
                    "name": "inline-supplementary-material",
                    "type": InlineSupplementaryMaterial,
                },
                {
                    "name": "related-article",
                    "type": RelatedArticle,
                },
                {
                    "name": "related-object",
                    "type": RelatedObject,
                },
                {
                    "name": "address",
                    "type": Address,
                },
                {
                    "name": "alternatives",
                    "type": Alternatives,
                },
                {
                    "name": "answer",
                    "type": Answer,
                },
                {
                    "name": "answer-set",
                    "type": AnswerSet,
                },
                {
                    "name": "array",
                    "type": Array,
                },
                {
                    "name": "block-alternatives",
                    "type": BlockAlternatives,
                },
                {
                    "name": "boxed-text",
                    "type": BoxedText,
                },
                {
                    "name": "chem-struct-wrap",
                    "type": ChemStructWrap,
                },
                {
                    "name": "code",
                    "type": Code,
                },
                {
                    "name": "explanation",
                    "type": Explanation,
                },
                {
                    "name": "fig",
                    "type": Fig,
                },
                {
                    "name": "fig-group",
                    "type": FigGroup,
                },
                {
                    "name": "graphic",
                    "type": Graphic,
                },
                {
                    "name": "media",
                    "type": Media,
                },
                {
                    "name": "preformat",
                    "type": Preformat,
                },
                {
                    "name": "question",
                    "type": Question,
                },
                {
                    "name": "question-wrap",
                    "type": QuestionWrap,
                },
                {
                    "name": "question-wrap-group",
                    "type": QuestionWrapGroup,
                },
                {
                    "name": "supplementary-material",
                    "type": SupplementaryMaterial,
                },
                {
                    "name": "table-wrap",
                    "type": TableWrap,
                },
                {
                    "name": "table-wrap-group",
                    "type": TableWrapGroup,
                },
                {
                    "name": "disp-formula",
                    "type": DispFormula,
                },
                {
                    "name": "disp-formula-group",
                    "type": DispFormulaGroup,
                },
                {
                    "name": "citation-alternatives",
                    "type": CitationAlternatives,
                },
                {
                    "name": "element-citation",
                    "type": ElementCitation,
                },
                {
                    "name": "mixed-citation",
                    "type": MixedCitation,
                },
                {
                    "name": "nlm-citation",
                    "type": NlmCitation,
                },
                {
                    "name": "bold",
                    "type": Bold,
                },
                {
                    "name": "fixed-case",
                    "type": FixedCase,
                },
                {
                    "name": "italic",
                    "type": Italic,
                },
                {
                    "name": "monospace",
                    "type": Monospace,
                },
                {
                    "name": "overline",
                    "type": Overline,
                },
                {
                    "name": "roman",
                    "type": Roman,
                },
                {
                    "name": "sans-serif",
                    "type": SansSerif,
                },
                {
                    "name": "sc",
                    "type": Sc,
                },
                {
                    "name": "strike",
                    "type": Strike,
                },
                {
                    "name": "underline",
                    "type": Underline,
                },
                {
                    "name": "ruby",
                    "type": Ruby,
                },
                {
                    "name": "award-id",
                    "type": AwardId,
                },
                {
                    "name": "funding-source",
                    "type": FundingSource,
                },
                {
                    "name": "open-access",
                    "type": OpenAccess,
                },
                {
                    "name": "chem-struct",
                    "type": ChemStruct,
                },
                {
                    "name": "inline-formula",
                    "type": InlineFormula,
                },
                {
                    "name": "inline-graphic",
                    "type": InlineGraphic,
                },
                {
                    "name": "inline-media",
                    "type": InlineMedia,
                },
                {
                    "name": "private-char",
                    "type": PrivateChar,
                },
                {
                    "name": "def-list",
                    "type": DefList,
                },
                {
                    "name": "list",
                    "type": List,
                },
                {
                    "name": "tex-math",
                    "type": TexMath,
                },
                {
                    "name": "math",
                    "type": Math,
                    "namespace": "http://www.w3.org/1998/Math/MathML",
                },
                {
                    "name": "abbrev",
                    "type": Abbrev,
                },
                {
                    "name": "index-term",
                    "type": IndexTerm,
                },
                {
                    "name": "index-term-range-end",
                    "type": IndexTermRangeEnd,
                },
                {
                    "name": "milestone-end",
                    "type": MilestoneEnd,
                },
                {
                    "name": "milestone-start",
                    "type": MilestoneStart,
                },
                {
                    "name": "named-content",
                    "type": NamedContent,
                },
                {
                    "name": "styled-content",
                    "type": StyledContent,
                },
                {
                    "name": "disp-quote",
                    "type": DispQuote,
                },
                {
                    "name": "speech",
                    "type": Speech,
                },
                {
                    "name": "statement",
                    "type": Statement,
                },
                {
                    "name": "verse-group",
                    "type": VerseGroup,
                },
                {
                    "name": "fn",
                    "type": Fn,
                },
                {
                    "name": "target",
                    "type": Target,
                },
                {
                    "name": "xref",
                    "type": Xref,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "price",
                    "type": Price,
                },
            ),
        },
    )


@dataclass
class RefList:
    """
    <div> <h3>Reference List (Bibliographic Reference List)</h3> </div>
    """

    class Meta:
        name = "ref-list"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional[Title] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer_set: list[AnswerSet] = field(
        default_factory=list,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list[BlockAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list[BoxedText] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    explanation: list[Explanation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list[Fig] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list[FigGroup] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list[Graphic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list[Media] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list[Preformat] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question: list[Question] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question_wrap: list[QuestionWrap] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
        },
    )
    question_wrap_group: list[QuestionWrapGroup] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap-group",
            "type": "Element",
        },
    )
    supplementary_material: list[SupplementaryMaterial] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list[TableWrap] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list[TableWrapGroup] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list[DispFormulaGroup] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    related_article: list[RelatedArticle] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list[RelatedObject] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    disp_quote: list[DispQuote] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list[Speech] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list[Statement] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list[VerseGroup] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    ref: list[Ref] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ref_list: list["RefList"] = field(
        default_factory=list,
        metadata={
            "name": "ref-list",
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Sec:
    """
    <div> <h3>Section</h3> </div>
    """

    class Meta:
        name = "sec"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    sec_meta: Optional[SecMeta] = field(
        default=None,
        metadata={
            "name": "sec-meta",
            "type": "Element",
        },
    )
    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    title: list[Title] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer_set: list[AnswerSet] = field(
        default_factory=list,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list[BlockAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list[BoxedText] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    explanation: list[Explanation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list[Fig] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list[FigGroup] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list[Graphic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list[Media] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list[Preformat] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question: list[Question] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question_wrap: list[QuestionWrap] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
        },
    )
    question_wrap_group: list[QuestionWrapGroup] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap-group",
            "type": "Element",
        },
    )
    supplementary_material: list[SupplementaryMaterial] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list[TableWrap] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list[TableWrapGroup] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list[DispFormulaGroup] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    related_article: list[RelatedArticle] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list[RelatedObject] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    disp_quote: list[DispQuote] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list[Speech] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list[Statement] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list[VerseGroup] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    sec: list["Sec"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fn_group: list[FnGroup] = field(
        default_factory=list,
        metadata={
            "name": "fn-group",
            "type": "Element",
        },
    )
    glossary: list[Glossary] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ref_list: list[RefList] = field(
        default_factory=list,
        metadata={
            "name": "ref-list",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    sec_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "sec-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Ack:
    """
    <div> <h3>Acknowledgments</h3> </div>
    """

    class Meta:
        name = "ack"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional[Title] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    abstract: list[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    kwd_group: list[KwdGroup] = field(
        default_factory=list,
        metadata={
            "name": "kwd-group",
            "type": "Element",
        },
    )
    subj_group: list[SubjGroup] = field(
        default_factory=list,
        metadata={
            "name": "subj-group",
            "type": "Element",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    sec: list[Sec] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ref_list: list[RefList] = field(
        default_factory=list,
        metadata={
            "name": "ref-list",
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class App:
    """
    <div> <h3>Appendix</h3> </div>
    """

    class Meta:
        name = "app"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    sec_meta: Optional[SecMeta] = field(
        default=None,
        metadata={
            "name": "sec-meta",
            "type": "Element",
        },
    )
    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    title: list[Title] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
            "max_occurs": 2,
            "sequence": 1,
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer_set: list[AnswerSet] = field(
        default_factory=list,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list[BlockAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list[BoxedText] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    explanation: list[Explanation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list[Fig] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list[FigGroup] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list[Graphic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list[Media] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list[Preformat] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question: list[Question] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question_wrap: list[QuestionWrap] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
        },
    )
    question_wrap_group: list[QuestionWrapGroup] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap-group",
            "type": "Element",
        },
    )
    supplementary_material: list[SupplementaryMaterial] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list[TableWrap] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list[TableWrapGroup] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list[DispFormulaGroup] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    related_article: list[RelatedArticle] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list[RelatedObject] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    disp_quote: list[DispQuote] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list[Speech] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list[Statement] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list[VerseGroup] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    sec: list[Sec] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fn_group: list[FnGroup] = field(
        default_factory=list,
        metadata={
            "name": "fn-group",
            "type": "Element",
        },
    )
    glossary: list[Glossary] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ref_list: list[RefList] = field(
        default_factory=list,
        metadata={
            "name": "ref-list",
            "type": "Element",
        },
    )
    permissions: Optional[Permissions] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Body:
    """
    <div> <h3>Body of the Article</h3> </div>
    """

    class Meta:
        name = "body"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer_set: list[AnswerSet] = field(
        default_factory=list,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list[BlockAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list[BoxedText] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    explanation: list[Explanation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list[Fig] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list[FigGroup] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list[Graphic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list[Media] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list[Preformat] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question: list[Question] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question_wrap: list[QuestionWrap] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
        },
    )
    question_wrap_group: list[QuestionWrapGroup] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap-group",
            "type": "Element",
        },
    )
    supplementary_material: list[SupplementaryMaterial] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list[TableWrap] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list[TableWrapGroup] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list[DispFormulaGroup] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    related_article: list[RelatedArticle] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list[RelatedObject] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    disp_quote: list[DispQuote] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list[Speech] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list[Statement] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list[VerseGroup] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    sec: list[Sec] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    sig_block: Optional[SigBlock] = field(
        default=None,
        metadata={
            "name": "sig-block",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Notes:
    """
    <div> <h3>Notes</h3> </div>
    """

    class Meta:
        name = "notes"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    sec_meta: Optional[SecMeta] = field(
        default=None,
        metadata={
            "name": "sec-meta",
            "type": "Element",
        },
    )
    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional[Title] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer_set: list[AnswerSet] = field(
        default_factory=list,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list[BlockAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list[BoxedText] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    explanation: list[Explanation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list[Fig] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list[FigGroup] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list[Graphic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list[Media] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list[Preformat] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question: list[Question] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question_wrap: list[QuestionWrap] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
        },
    )
    question_wrap_group: list[QuestionWrapGroup] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap-group",
            "type": "Element",
        },
    )
    supplementary_material: list[SupplementaryMaterial] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list[TableWrap] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list[TableWrapGroup] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list[DispFormulaGroup] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    related_article: list[RelatedArticle] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list[RelatedObject] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    disp_quote: list[DispQuote] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list[Speech] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list[Statement] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list[VerseGroup] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    sec: list[Sec] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fn_group: list[FnGroup] = field(
        default_factory=list,
        metadata={
            "name": "fn-group",
            "type": "Element",
        },
    )
    glossary: list[Glossary] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ref_list: list[RefList] = field(
        default_factory=list,
        metadata={
            "name": "ref-list",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    notes_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "notes-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class TransAbstract:
    """
    <div> <h3>Translated Abstract</h3> </div>
    """

    class Meta:
        name = "trans-abstract"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional[Title] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    sec: list[Sec] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    abstract_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "abstract-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class AppGroup:
    """
    <div> <h3>Appendix Group</h3> </div>
    """

    class Meta:
        name = "app-group"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    object_id: list[ObjectId] = field(
        default_factory=list,
        metadata={
            "name": "object-id",
            "type": "Element",
        },
    )
    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: Optional[Title] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    abstract: list[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    kwd_group: list[KwdGroup] = field(
        default_factory=list,
        metadata={
            "name": "kwd-group",
            "type": "Element",
        },
    )
    subj_group: list[SubjGroup] = field(
        default_factory=list,
        metadata={
            "name": "subj-group",
            "type": "Element",
        },
    )
    address: list[Address] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    alternatives: list[Alternatives] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer: list[Answer] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    answer_set: list[AnswerSet] = field(
        default_factory=list,
        metadata={
            "name": "answer-set",
            "type": "Element",
        },
    )
    array: list[Array] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    block_alternatives: list[BlockAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "block-alternatives",
            "type": "Element",
        },
    )
    boxed_text: list[BoxedText] = field(
        default_factory=list,
        metadata={
            "name": "boxed-text",
            "type": "Element",
        },
    )
    chem_struct_wrap: list[ChemStructWrap] = field(
        default_factory=list,
        metadata={
            "name": "chem-struct-wrap",
            "type": "Element",
        },
    )
    code: list[Code] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    explanation: list[Explanation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig: list[Fig] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fig_group: list[FigGroup] = field(
        default_factory=list,
        metadata={
            "name": "fig-group",
            "type": "Element",
        },
    )
    graphic: list[Graphic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    media: list[Media] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    preformat: list[Preformat] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question: list[Question] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    question_wrap: list[QuestionWrap] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap",
            "type": "Element",
        },
    )
    question_wrap_group: list[QuestionWrapGroup] = field(
        default_factory=list,
        metadata={
            "name": "question-wrap-group",
            "type": "Element",
        },
    )
    supplementary_material: list[SupplementaryMaterial] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    table_wrap: list[TableWrap] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap",
            "type": "Element",
        },
    )
    table_wrap_group: list[TableWrapGroup] = field(
        default_factory=list,
        metadata={
            "name": "table-wrap-group",
            "type": "Element",
        },
    )
    disp_formula: list[DispFormula] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula",
            "type": "Element",
        },
    )
    disp_formula_group: list[DispFormulaGroup] = field(
        default_factory=list,
        metadata={
            "name": "disp-formula-group",
            "type": "Element",
        },
    )
    def_list: list[DefList] = field(
        default_factory=list,
        metadata={
            "name": "def-list",
            "type": "Element",
        },
    )
    list_value: list[List] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
        },
    )
    tex_math: list[TexMath] = field(
        default_factory=list,
        metadata={
            "name": "tex-math",
            "type": "Element",
        },
    )
    math: list[Math] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1998/Math/MathML",
        },
    )
    p: list[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    related_article: list[RelatedArticle] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list[RelatedObject] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    disp_quote: list[DispQuote] = field(
        default_factory=list,
        metadata={
            "name": "disp-quote",
            "type": "Element",
        },
    )
    speech: list[Speech] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    statement: list[Statement] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    verse_group: list[VerseGroup] = field(
        default_factory=list,
        metadata={
            "name": "verse-group",
            "type": "Element",
        },
    )
    app: list[App] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ref_list: list[RefList] = field(
        default_factory=list,
        metadata={
            "name": "ref-list",
            "type": "Element",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Event:
    """
    <div> <h3>Event in Publishing History</h3> </div>
    """

    class Meta:
        name = "event"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    event_desc: Optional[EventDesc] = field(
        default=None,
        metadata={
            "name": "event-desc",
            "type": "Element",
        },
    )
    article_id: list[ArticleId] = field(
        default_factory=list,
        metadata={
            "name": "article-id",
            "type": "Element",
        },
    )
    article_version: Optional[ArticleVersion] = field(
        default=None,
        metadata={
            "name": "article-version",
            "type": "Element",
        },
    )
    article_version_alternatives: Optional[ArticleVersionAlternatives] = field(
        default=None,
        metadata={
            "name": "article-version-alternatives",
            "type": "Element",
        },
    )
    pub_date: list[PubDate] = field(
        default_factory=list,
        metadata={
            "name": "pub-date",
            "type": "Element",
        },
    )
    pub_date_not_available: Optional[PubDateNotAvailable] = field(
        default=None,
        metadata={
            "name": "pub-date-not-available",
            "type": "Element",
        },
    )
    date: list[Date] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    issn: list[Issn] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    issn_l: Optional[IssnL] = field(
        default=None,
        metadata={
            "name": "issn-l",
            "type": "Element",
        },
    )
    isbn: list[Isbn] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    permissions: Optional[Permissions] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    notes: list[Notes] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    self_uri: list[SelfUri] = field(
        default_factory=list,
        metadata={
            "name": "self-uri",
            "type": "Element",
        },
    )
    event_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "event-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class JournalMeta:
    """
    <div> <h3>Journal Metadata</h3> </div>
    """

    class Meta:
        name = "journal-meta"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    journal_id: list[JournalId] = field(
        default_factory=list,
        metadata={
            "name": "journal-id",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    journal_title_group: list[JournalTitleGroup] = field(
        default_factory=list,
        metadata={
            "name": "journal-title-group",
            "type": "Element",
        },
    )
    contrib_group: list[ContribGroup] = field(
        default_factory=list,
        metadata={
            "name": "contrib-group",
            "type": "Element",
        },
    )
    aff: list[Aff] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    aff_alternatives: list[AffAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "aff-alternatives",
            "type": "Element",
        },
    )
    issn: list[Issn] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    issn_l: Optional[IssnL] = field(
        default=None,
        metadata={
            "name": "issn-l",
            "type": "Element",
        },
    )
    isbn: list[Isbn] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    publisher: Optional[Publisher] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    notes: list[Notes] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    self_uri: list[SelfUri] = field(
        default_factory=list,
        metadata={
            "name": "self-uri",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Back:
    """
    <div> <h3>Back Matter</h3> </div>
    """

    class Meta:
        name = "back"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    label: Optional[Label] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    title: list[Title] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ack: list[Ack] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    app_group: list[AppGroup] = field(
        default_factory=list,
        metadata={
            "name": "app-group",
            "type": "Element",
        },
    )
    bio: list[Bio] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    fn_group: list[FnGroup] = field(
        default_factory=list,
        metadata={
            "name": "fn-group",
            "type": "Element",
        },
    )
    glossary: list[Glossary] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ref_list: list[RefList] = field(
        default_factory=list,
        metadata={
            "name": "ref-list",
            "type": "Element",
        },
    )
    notes: list[Notes] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    sec: list[Sec] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class PubHistory:
    """
    <div> <h3>Publication History</h3> </div>
    """

    class Meta:
        name = "pub-history"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    event: list[Event] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class ArticleMeta:
    """
    <div> <h3>Article Metadata</h3> </div>
    """

    class Meta:
        name = "article-meta"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    article_id: list[ArticleId] = field(
        default_factory=list,
        metadata={
            "name": "article-id",
            "type": "Element",
        },
    )
    article_version: Optional[ArticleVersion] = field(
        default=None,
        metadata={
            "name": "article-version",
            "type": "Element",
        },
    )
    article_version_alternatives: Optional[ArticleVersionAlternatives] = field(
        default=None,
        metadata={
            "name": "article-version-alternatives",
            "type": "Element",
        },
    )
    article_categories: Optional[ArticleCategories] = field(
        default=None,
        metadata={
            "name": "article-categories",
            "type": "Element",
        },
    )
    title_group: Optional[TitleGroup] = field(
        default=None,
        metadata={
            "name": "title-group",
            "type": "Element",
            "required": True,
        },
    )
    contrib_group: list[ContribGroup] = field(
        default_factory=list,
        metadata={
            "name": "contrib-group",
            "type": "Element",
        },
    )
    aff: list[Aff] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    aff_alternatives: list[AffAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "aff-alternatives",
            "type": "Element",
        },
    )
    author_notes: Optional[AuthorNotes] = field(
        default=None,
        metadata={
            "name": "author-notes",
            "type": "Element",
        },
    )
    pub_date: list[PubDate] = field(
        default_factory=list,
        metadata={
            "name": "pub-date",
            "type": "Element",
        },
    )
    pub_date_not_available: Optional[PubDateNotAvailable] = field(
        default=None,
        metadata={
            "name": "pub-date-not-available",
            "type": "Element",
        },
    )
    volume: list[Volume] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    volume_id: list[VolumeId] = field(
        default_factory=list,
        metadata={
            "name": "volume-id",
            "type": "Element",
        },
    )
    volume_series: Optional[VolumeSeries] = field(
        default=None,
        metadata={
            "name": "volume-series",
            "type": "Element",
        },
    )
    issue: list[Issue] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    issue_id: list[IssueId] = field(
        default_factory=list,
        metadata={
            "name": "issue-id",
            "type": "Element",
        },
    )
    issue_title: list[IssueTitle] = field(
        default_factory=list,
        metadata={
            "name": "issue-title",
            "type": "Element",
        },
    )
    issue_title_group: list[IssueTitleGroup] = field(
        default_factory=list,
        metadata={
            "name": "issue-title-group",
            "type": "Element",
        },
    )
    issue_sponsor: list[IssueSponsor] = field(
        default_factory=list,
        metadata={
            "name": "issue-sponsor",
            "type": "Element",
        },
    )
    issue_part: Optional[IssuePart] = field(
        default=None,
        metadata={
            "name": "issue-part",
            "type": "Element",
        },
    )
    volume_issue_group: list[VolumeIssueGroup] = field(
        default_factory=list,
        metadata={
            "name": "volume-issue-group",
            "type": "Element",
        },
    )
    isbn: list[Isbn] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    supplement: Optional[Supplement] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    fpage: Optional[Fpage] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    lpage: Optional[Lpage] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    page_range: Optional[PageRange] = field(
        default=None,
        metadata={
            "name": "page-range",
            "type": "Element",
        },
    )
    elocation_id: Optional[ElocationId] = field(
        default=None,
        metadata={
            "name": "elocation-id",
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list[ExtLink] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    product: list[Product] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    supplementary_material: list[SupplementaryMaterial] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    history: Optional[History] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    pub_history: Optional[PubHistory] = field(
        default=None,
        metadata={
            "name": "pub-history",
            "type": "Element",
        },
    )
    permissions: Optional[Permissions] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    self_uri: list[SelfUri] = field(
        default_factory=list,
        metadata={
            "name": "self-uri",
            "type": "Element",
        },
    )
    related_article: list[RelatedArticle] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list[RelatedObject] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    abstract: list[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    trans_abstract: list[TransAbstract] = field(
        default_factory=list,
        metadata={
            "name": "trans-abstract",
            "type": "Element",
        },
    )
    kwd_group: list[KwdGroup] = field(
        default_factory=list,
        metadata={
            "name": "kwd-group",
            "type": "Element",
        },
    )
    funding_group: list[FundingGroup] = field(
        default_factory=list,
        metadata={
            "name": "funding-group",
            "type": "Element",
        },
    )
    support_group: list[SupportGroup] = field(
        default_factory=list,
        metadata={
            "name": "support-group",
            "type": "Element",
        },
    )
    conference: list[Conference] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    counts: Optional[Counts] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    custom_meta_group: Optional[CustomMetaGroup] = field(
        default=None,
        metadata={
            "name": "custom-meta-group",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class FrontStub:
    """
    <div> <h3>Stub Front Metadata</h3> </div>
    """

    class Meta:
        name = "front-stub"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    article_id: list[ArticleId] = field(
        default_factory=list,
        metadata={
            "name": "article-id",
            "type": "Element",
        },
    )
    article_version: Optional[ArticleVersion] = field(
        default=None,
        metadata={
            "name": "article-version",
            "type": "Element",
        },
    )
    article_version_alternatives: Optional[ArticleVersionAlternatives] = field(
        default=None,
        metadata={
            "name": "article-version-alternatives",
            "type": "Element",
        },
    )
    article_categories: Optional[ArticleCategories] = field(
        default=None,
        metadata={
            "name": "article-categories",
            "type": "Element",
        },
    )
    title_group: Optional[TitleGroup] = field(
        default=None,
        metadata={
            "name": "title-group",
            "type": "Element",
        },
    )
    contrib_group: list[ContribGroup] = field(
        default_factory=list,
        metadata={
            "name": "contrib-group",
            "type": "Element",
        },
    )
    aff: list[Aff] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    aff_alternatives: list[AffAlternatives] = field(
        default_factory=list,
        metadata={
            "name": "aff-alternatives",
            "type": "Element",
        },
    )
    author_notes: Optional[AuthorNotes] = field(
        default=None,
        metadata={
            "name": "author-notes",
            "type": "Element",
        },
    )
    pub_date: list[PubDate] = field(
        default_factory=list,
        metadata={
            "name": "pub-date",
            "type": "Element",
        },
    )
    pub_date_not_available: Optional[PubDateNotAvailable] = field(
        default=None,
        metadata={
            "name": "pub-date-not-available",
            "type": "Element",
        },
    )
    volume: list[Volume] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    volume_id: list[VolumeId] = field(
        default_factory=list,
        metadata={
            "name": "volume-id",
            "type": "Element",
        },
    )
    volume_series: Optional[VolumeSeries] = field(
        default=None,
        metadata={
            "name": "volume-series",
            "type": "Element",
        },
    )
    issue: list[Issue] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    issue_id: list[IssueId] = field(
        default_factory=list,
        metadata={
            "name": "issue-id",
            "type": "Element",
        },
    )
    issue_title: list[IssueTitle] = field(
        default_factory=list,
        metadata={
            "name": "issue-title",
            "type": "Element",
        },
    )
    issue_title_group: list[IssueTitleGroup] = field(
        default_factory=list,
        metadata={
            "name": "issue-title-group",
            "type": "Element",
        },
    )
    issue_sponsor: list[IssueSponsor] = field(
        default_factory=list,
        metadata={
            "name": "issue-sponsor",
            "type": "Element",
        },
    )
    issue_part: Optional[IssuePart] = field(
        default=None,
        metadata={
            "name": "issue-part",
            "type": "Element",
        },
    )
    volume_issue_group: list[VolumeIssueGroup] = field(
        default_factory=list,
        metadata={
            "name": "volume-issue-group",
            "type": "Element",
        },
    )
    isbn: list[Isbn] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    supplement: Optional[Supplement] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    fpage: Optional[Fpage] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    lpage: Optional[Lpage] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    page_range: Optional[PageRange] = field(
        default=None,
        metadata={
            "name": "page-range",
            "type": "Element",
        },
    )
    elocation_id: Optional[ElocationId] = field(
        default=None,
        metadata={
            "name": "elocation-id",
            "type": "Element",
        },
    )
    email: list[Email] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    ext_link: list[ExtLink] = field(
        default_factory=list,
        metadata={
            "name": "ext-link",
            "type": "Element",
        },
    )
    uri: list[Uri] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    product: list[Product] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    supplementary_material: list[SupplementaryMaterial] = field(
        default_factory=list,
        metadata={
            "name": "supplementary-material",
            "type": "Element",
        },
    )
    history: Optional[History] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    pub_history: Optional[PubHistory] = field(
        default=None,
        metadata={
            "name": "pub-history",
            "type": "Element",
        },
    )
    permissions: Optional[Permissions] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    self_uri: list[SelfUri] = field(
        default_factory=list,
        metadata={
            "name": "self-uri",
            "type": "Element",
        },
    )
    related_article: list[RelatedArticle] = field(
        default_factory=list,
        metadata={
            "name": "related-article",
            "type": "Element",
        },
    )
    related_object: list[RelatedObject] = field(
        default_factory=list,
        metadata={
            "name": "related-object",
            "type": "Element",
        },
    )
    abstract: list[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    trans_abstract: list[TransAbstract] = field(
        default_factory=list,
        metadata={
            "name": "trans-abstract",
            "type": "Element",
        },
    )
    kwd_group: list[KwdGroup] = field(
        default_factory=list,
        metadata={
            "name": "kwd-group",
            "type": "Element",
        },
    )
    funding_group: list[FundingGroup] = field(
        default_factory=list,
        metadata={
            "name": "funding-group",
            "type": "Element",
        },
    )
    support_group: list[SupportGroup] = field(
        default_factory=list,
        metadata={
            "name": "support-group",
            "type": "Element",
        },
    )
    conference: list[Conference] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    counts: Optional[Counts] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    custom_meta_group: Optional[CustomMetaGroup] = field(
        default=None,
        metadata={
            "name": "custom-meta-group",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Front:
    """
    <div> <h3>Front Matter</h3> </div>
    """

    class Meta:
        name = "front"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    journal_meta: Optional[JournalMeta] = field(
        default=None,
        metadata={
            "name": "journal-meta",
            "type": "Element",
            "required": True,
        },
    )
    article_meta: Optional[ArticleMeta] = field(
        default=None,
        metadata={
            "name": "article-meta",
            "type": "Element",
            "required": True,
        },
    )
    notes: Optional[Notes] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Response:
    """
    <div> <h3>Response</h3> </div>
    """

    class Meta:
        name = "response"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    processing_meta: Optional[ProcessingMeta] = field(
        default=None,
        metadata={
            "name": "processing-meta",
            "type": "Element",
        },
    )
    front: Optional[Front] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    front_stub: Optional[FrontStub] = field(
        default=None,
        metadata={
            "name": "front-stub",
            "type": "Element",
        },
    )
    body: Optional[Body] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    back: Optional[Back] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    floats_group: Optional[FloatsGroup] = field(
        default=None,
        metadata={
            "name": "floats-group",
            "type": "Element",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    response_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "response-type",
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class SubArticle:
    """
    <div> <h3>Sub-Article</h3> </div>
    """

    class Meta:
        name = "sub-article"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    processing_meta: Optional[ProcessingMeta] = field(
        default=None,
        metadata={
            "name": "processing-meta",
            "type": "Element",
        },
    )
    front: Optional[Front] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    front_stub: Optional[FrontStub] = field(
        default=None,
        metadata={
            "name": "front-stub",
            "type": "Element",
        },
    )
    body: Optional[Body] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    back: Optional[Back] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    floats_group: Optional[FloatsGroup] = field(
        default=None,
        metadata={
            "name": "floats-group",
            "type": "Element",
        },
    )
    sub_article: list["SubArticle"] = field(
        default_factory=list,
        metadata={
            "name": "sub-article",
            "type": "Element",
        },
    )
    response: list[Response] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    article_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "article-type",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Article:
    """
    <div> <h3>Article</h3> </div>
    """

    class Meta:
        name = "article"
        namespace = "http://www.ncbi.nlm.nih.gov/JATS1"

    processing_meta: Optional[ProcessingMeta] = field(
        default=None,
        metadata={
            "name": "processing-meta",
            "type": "Element",
        },
    )
    front: Optional[Front] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    body: Optional[Body] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    back: Optional[Back] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    floats_group: Optional[FloatsGroup] = field(
        default=None,
        metadata={
            "name": "floats-group",
            "type": "Element",
        },
    )
    sub_article: list[SubArticle] = field(
        default_factory=list,
        metadata={
            "name": "sub-article",
            "type": "Element",
        },
    )
    response: list[Response] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    article_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "article-type",
            "type": "Attribute",
        },
    )
    dtd_version: Optional[ArticleDtdVersion] = field(
        default=None,
        metadata={
            "name": "dtd-version",
            "type": "Attribute",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: Optional[str] = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    base: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    lang: Union[str, LangValue] = field(
        default="en",
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
