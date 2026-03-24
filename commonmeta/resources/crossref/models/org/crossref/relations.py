from dataclasses import dataclass, field
from enum import Enum
from typing import ForwardRef, Optional

__NAMESPACE__ = "http://www.crossref.org/relations.xsd"


class DescriptionLanguage(Enum):
    AA = "aa"
    AB = "ab"
    AE = "ae"
    AF = "af"
    AK = "ak"
    AM = "am"
    AN = "an"
    AR = "ar"
    AS = "as"
    AV = "av"
    AY = "ay"
    AZ = "az"
    BA = "ba"
    BE = "be"
    BG = "bg"
    BH = "bh"
    BI = "bi"
    BM = "bm"
    BN = "bn"
    BO = "bo"
    BR = "br"
    BS = "bs"
    CA = "ca"
    CE = "ce"
    CH = "ch"
    CO = "co"
    CR = "cr"
    CS = "cs"
    CU = "cu"
    CV = "cv"
    CY = "cy"
    DA = "da"
    DE = "de"
    DV = "dv"
    DZ = "dz"
    EE = "ee"
    EL = "el"
    EN = "en"
    EO = "eo"
    ES = "es"
    ET = "et"
    EU = "eu"
    FA = "fa"
    FF = "ff"
    FI = "fi"
    FJ = "fj"
    FO = "fo"
    FR = "fr"
    FY = "fy"
    GA = "ga"
    GD = "gd"
    GL = "gl"
    GN = "gn"
    GU = "gu"
    GV = "gv"
    HA = "ha"
    HE = "he"
    HI = "hi"
    HO = "ho"
    HR = "hr"
    HT = "ht"
    HU = "hu"
    HY = "hy"
    HZ = "hz"
    IA = "ia"
    ID = "id"
    IE = "ie"
    IG = "ig"
    II = "ii"
    IK = "ik"
    IO = "io"
    IS = "is"
    IT = "it"
    IU = "iu"
    JA = "ja"
    JW = "jw"
    KA = "ka"
    KG = "kg"
    KI = "ki"
    KJ = "kj"
    KK = "kk"
    KL = "kl"
    KM = "km"
    KN = "kn"
    KO = "ko"
    KR = "kr"
    KS = "ks"
    KU = "ku"
    KV = "kv"
    KW = "kw"
    KY = "ky"
    LA = "la"
    LB = "lb"
    LG = "lg"
    LI = "li"
    LN = "ln"
    LO = "lo"
    LT = "lt"
    LU = "lu"
    LV = "lv"
    MG = "mg"
    MU = "mu"
    MI = "mi"
    MK = "mk"
    ML = "ml"
    MN = "mn"
    MR = "mr"
    MS = "ms"
    MT = "mt"
    MY = "my"
    NA = "na"
    NB = "nb"
    ND = "nd"
    NE = "ne"
    NG = "ng"
    NL = "nl"
    NN = "nn"
    NO = "no"
    NR = "nr"
    NV = "nv"
    NY = "ny"
    OC = "oc"
    OJ = "oj"
    OM = "om"
    OR = "or"
    OS = "os"
    PA = "pa"
    PI = "pi"
    PL = "pl"
    PS = "ps"
    PT = "pt"
    QU = "qu"
    RM = "rm"
    RN = "rn"
    RO = "ro"
    RU = "ru"
    RW = "rw"
    SA = "sa"
    SC = "sc"
    SD = "sd"
    SE = "se"
    SG = "sg"
    SI = "si"
    SK = "sk"
    SL = "sl"
    SM = "sm"
    SN = "sn"
    SO = "so"
    SQ = "sq"
    SR = "sr"
    SS = "ss"
    ST = "st"
    SU = "su"
    SV = "sv"
    SW = "sw"
    TA = "ta"
    TE = "te"
    TG = "tg"
    TH = "th"
    TI = "ti"
    TK = "tk"
    TL = "tl"
    TN = "tn"
    TO = "to"
    TR = "tr"
    TS = "ts"
    TT = "tt"
    TW = "tw"
    TY = "ty"
    UG = "ug"
    UK = "uk"
    UR = "ur"
    UZ = "uz"
    VE = "ve"
    VI = "vi"
    VO = "vo"
    WA = "wa"
    WO = "wo"
    XH = "xh"
    YI = "yi"
    YO = "yo"
    ZA = "za"
    ZH = "zh"


class InterWorkRelationIdentifierType(Enum):
    DOI = "doi"
    ISSN = "issn"
    ISBN = "isbn"
    URI = "uri"
    PMID = "pmid"
    PMCID = "pmcid"
    PURL = "purl"
    ARXIV = "arxiv"
    ARK = "ark"
    HANDLE = "handle"
    UUID = "uuid"
    ECLI = "ecli"
    ACCESSION = "accession"
    OTHER = "other"


class InterWorkRelationRelationshipType(Enum):
    IS_DERIVED_FROM = "isDerivedFrom"
    HAS_DERIVATION = "hasDerivation"
    IS_REVIEW_OF = "isReviewOf"
    HAS_REVIEW = "hasReview"
    IS_COMMENT_ON = "isCommentOn"
    HAS_COMMENT = "hasComment"
    IS_REPLY_TO = "isReplyTo"
    HAS_REPLY = "hasReply"
    BASED_ON_DATA = "basedOnData"
    IS_DATA_BASIS_FOR = "isDataBasisFor"
    HAS_RELATED_MATERIAL = "hasRelatedMaterial"
    IS_RELATED_MATERIAL = "isRelatedMaterial"
    IS_COMPILED_BY = "isCompiledBy"
    COMPILES = "compiles"
    IS_DOCUMENTED_BY = "isDocumentedBy"
    DOCUMENTS = "documents"
    IS_SUPPLEMENT_TO = "isSupplementTo"
    IS_SUPPLEMENTED_BY = "isSupplementedBy"
    IS_CONTINUED_BY = "isContinuedBy"
    CONTINUES = "continues"
    IS_PART_OF = "isPartOf"
    HAS_PART = "hasPart"
    REFERENCES = "references"
    IS_REFERENCED_BY = "isReferencedBy"
    IS_BASED_ON = "isBasedOn"
    IS_BASIS_FOR = "isBasisFor"
    REQUIRES = "requires"
    IS_REQUIRED_BY = "isRequiredBy"
    FINANCES = "finances"
    IS_FINANCED_BY = "isFinancedBy"


class IntraWorkRelationIdentifierType(Enum):
    DOI = "doi"
    ISSN = "issn"
    ISBN = "isbn"
    URI = "uri"
    PMID = "pmid"
    PMCID = "pmcid"
    PURL = "purl"
    ARXIV = "arxiv"
    ARK = "ark"
    HANDLE = "handle"
    UUID = "uuid"
    ECLI = "ecli"
    ACCESSION = "accession"
    OTHER = "other"


class IntraWorkRelationRelationshipType(Enum):
    IS_TRANSLATION_OF = "isTranslationOf"
    HAS_TRANSLATION = "hasTranslation"
    IS_PREPRINT_OF = "isPreprintOf"
    HAS_PREPRINT = "hasPreprint"
    IS_MANUSCRIPT_OF = "isManuscriptOf"
    HAS_MANUSCRIPT = "hasManuscript"
    IS_EXPRESSION_OF = "isExpressionOf"
    HAS_EXPRESSION = "hasExpression"
    IS_MANIFESTATION_OF = "isManifestationOf"
    HAS_MANIFESTATION = "hasManifestation"
    IS_REPLACED_BY = "isReplacedBy"
    REPLACES = "replaces"
    IS_SAME_AS = "isSameAs"
    IS_IDENTICAL_TO = "isIdenticalTo"
    IS_VARIANT_FORM_OF = "isVariantFormOf"
    IS_ORIGINAL_FORM_OF = "isOriginalFormOf"
    IS_VERSION_OF = "isVersionOf"
    HAS_VERSION = "hasVersion"
    IS_FORMAT_OF = "isFormatOf"
    HAS_FORMAT = "hasFormat"


@dataclass
class XrefFaces:
    class Meta:
        name = "xrefFaces"

    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "b",
                    "type": ForwardRef("B"),
                    "namespace": "http://www.crossref.org/relations.xsd",
                },
                {
                    "name": "i",
                    "type": ForwardRef("I"),
                    "namespace": "http://www.crossref.org/relations.xsd",
                },
                {
                    "name": "em",
                    "type": ForwardRef("Em"),
                    "namespace": "http://www.crossref.org/relations.xsd",
                },
                {
                    "name": "strong",
                    "type": ForwardRef("Strong"),
                    "namespace": "http://www.crossref.org/relations.xsd",
                },
                {
                    "name": "u",
                    "type": ForwardRef("U"),
                    "namespace": "http://www.crossref.org/relations.xsd",
                },
                {
                    "name": "ovl",
                    "type": ForwardRef("Ovl"),
                    "namespace": "http://www.crossref.org/relations.xsd",
                },
                {
                    "name": "sup",
                    "type": ForwardRef("Sup"),
                    "namespace": "http://www.crossref.org/relations.xsd",
                },
                {
                    "name": "sub",
                    "type": ForwardRef("Sub"),
                    "namespace": "http://www.crossref.org/relations.xsd",
                },
                {
                    "name": "scp",
                    "type": ForwardRef("Scp"),
                    "namespace": "http://www.crossref.org/relations.xsd",
                },
                {
                    "name": "tt",
                    "type": ForwardRef("Tt"),
                    "namespace": "http://www.crossref.org/relations.xsd",
                },
                {
                    "name": "font",
                    "type": ForwardRef("Font"),
                    "namespace": "http://www.crossref.org/relations.xsd",
                },
            ),
        },
    )


@dataclass
class B(XrefFaces):
    class Meta:
        name = "b"
        namespace = "http://www.crossref.org/relations.xsd"


@dataclass
class Em(XrefFaces):
    class Meta:
        name = "em"
        namespace = "http://www.crossref.org/relations.xsd"


@dataclass
class Font(XrefFaces):
    class Meta:
        name = "font"
        namespace = "http://www.crossref.org/relations.xsd"


@dataclass
class I(XrefFaces):
    class Meta:
        name = "i"
        namespace = "http://www.crossref.org/relations.xsd"


@dataclass
class InterWorkRelation:
    """
    :ivar relationship_type: Used to describe relations between items
        that are not the same work.
    :ivar identifier_type:
    :ivar namespace: An identifier systems may require a namespace that
        is needed in addition to the identifer value to provide
        uniqueness.
    :ivar content:
    """

    class Meta:
        name = "inter_work_relation"
        namespace = "http://www.crossref.org/relations.xsd"

    relationship_type: Optional[InterWorkRelationRelationshipType] = field(
        default=None,
        metadata={
            "name": "relationship-type",
            "type": "Attribute",
            "required": True,
        },
    )
    identifier_type: Optional[InterWorkRelationIdentifierType] = field(
        default=None,
        metadata={
            "name": "identifier-type",
            "type": "Attribute",
            "required": True,
        },
    )
    namespace: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 4,
            "max_length": 1024,
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
class IntraWorkRelation:
    """
    :ivar relationship_type: Used to define relations between items that
        are essentially the same work but may differ in some way that
        impacts citation, for example a difference in format, language,
        or revision. Assigning different identifers to exactly the same
        item available in one place or as copies in multiple places can
        be problematic and should be avoided.
    :ivar identifier_type:
    :ivar namespace: An identifier systems may require a namespace that
        is needed in addition to the identifer value to provide
        uniqueness.
    :ivar content:
    """

    class Meta:
        name = "intra_work_relation"
        namespace = "http://www.crossref.org/relations.xsd"

    relationship_type: Optional[IntraWorkRelationRelationshipType] = field(
        default=None,
        metadata={
            "name": "relationship-type",
            "type": "Attribute",
            "required": True,
        },
    )
    identifier_type: Optional[IntraWorkRelationIdentifierType] = field(
        default=None,
        metadata={
            "name": "identifier-type",
            "type": "Attribute",
            "required": True,
        },
    )
    namespace: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 4,
            "max_length": 1024,
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
class Ovl(XrefFaces):
    class Meta:
        name = "ovl"
        namespace = "http://www.crossref.org/relations.xsd"


@dataclass
class Scp(XrefFaces):
    class Meta:
        name = "scp"
        namespace = "http://www.crossref.org/relations.xsd"


@dataclass
class Strong(XrefFaces):
    class Meta:
        name = "strong"
        namespace = "http://www.crossref.org/relations.xsd"


@dataclass
class Sub(XrefFaces):
    class Meta:
        name = "sub"
        namespace = "http://www.crossref.org/relations.xsd"


@dataclass
class Sup(XrefFaces):
    class Meta:
        name = "sup"
        namespace = "http://www.crossref.org/relations.xsd"


@dataclass
class Tt(XrefFaces):
    class Meta:
        name = "tt"
        namespace = "http://www.crossref.org/relations.xsd"


@dataclass
class U(XrefFaces):
    class Meta:
        name = "u"
        namespace = "http://www.crossref.org/relations.xsd"


@dataclass
class Description:
    """
    A narrative description of the relationship target item.
    """

    class Meta:
        name = "description"
        namespace = "http://www.crossref.org/relations.xsd"

    language: Optional[DescriptionLanguage] = field(
        default=None,
        metadata={
            "type": "Attribute",
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
                    "name": "b",
                    "type": B,
                },
                {
                    "name": "i",
                    "type": I,
                },
                {
                    "name": "em",
                    "type": Em,
                },
                {
                    "name": "strong",
                    "type": Strong,
                },
                {
                    "name": "u",
                    "type": U,
                },
                {
                    "name": "ovl",
                    "type": Ovl,
                },
                {
                    "name": "sup",
                    "type": Sup,
                },
                {
                    "name": "sub",
                    "type": Sub,
                },
                {
                    "name": "scp",
                    "type": Scp,
                },
                {
                    "name": "tt",
                    "type": Tt,
                },
                {
                    "name": "font",
                    "type": Font,
                },
            ),
        },
    )


@dataclass
class RelatedItem:
    class Meta:
        name = "related_item"
        namespace = "http://www.crossref.org/relations.xsd"

    description: Optional[Description] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    inter_work_relation: Optional[InterWorkRelation] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    intra_work_relation: Optional[IntraWorkRelation] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )


@dataclass
class Program:
    """
    Wrapper element for relationship metadata.
    """

    class Meta:
        name = "program"
        namespace = "http://www.crossref.org/relations.xsd"

    related_item: list[RelatedItem] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    name: str = field(
        init=False,
        default="relations",
        metadata={
            "type": "Attribute",
        },
    )
