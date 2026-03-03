from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "http://www.crossref.org/AccessIndicators.xsd"


@dataclass(slots=True, kw_only=True)
class FreeToRead:
    class Meta:
        name = "free_to_read"
        namespace = "http://www.crossref.org/AccessIndicators.xsd"

    end_date: None | XmlDate = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    start_date: None | XmlDate = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class LicenseRefAppliesTo(Enum):
    VOR = "vor"
    AM = "am"
    TDM = "tdm"


@dataclass(slots=True, kw_only=True)
class LicenseRef:
    class Meta:
        name = "license_ref"
        namespace = "http://www.crossref.org/AccessIndicators.xsd"

    value: str = field(
        default="",
        metadata={
            "min_length": 10,
            "pattern": r"([hH][tT][tT][pP]|[hH][tT][tT][pP][sS]|[fF][tT][pP])://.*",
        },
    )
    start_date: None | XmlDate = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    applies_to: None | LicenseRefAppliesTo = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(slots=True, kw_only=True)
class Program:
    """
    Accommodates deposit of license metadata.

    The license_ref value will be a URL. Values for the "applies_to"
    attribute are vor (version of record),am (accepted manuscript), and tdm
    (text and data mining).
    """

    class Meta:
        name = "program"
        namespace = "http://www.crossref.org/AccessIndicators.xsd"

    free_to_read: None | FreeToRead = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    license_ref: list[LicenseRef] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    name: str = field(
        init=False,
        default="AccessIndicators",
        metadata={
            "type": "Attribute",
        },
    )
