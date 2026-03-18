from dataclasses import dataclass, field
from enum import Enum
from typing import ForwardRef, Optional

__NAMESPACE__ = "http://www.crossref.org/fundref.xsd"


class AssertionName(Enum):
    FUNDGROUP = "fundgroup"
    FUNDER_IDENTIFIER = "funder_identifier"
    ROR = "ror"
    FUNDER_NAME = "funder_name"
    AWARD_NUMBER = "award_number"


class AssertionProvider(Enum):
    PUBLISHER = "publisher"
    CROSSREF = "crossref"


@dataclass
class Assertion:
    """Funding data attributes included in assertion are:
    * fundgroup: used to group funding info for items with multiple funding sources. Required for items with multiple award_number assertions, optional for items with a single award_number
    * funder_identifier: funding agency identifier, must be nested within the funder_name assertion
    * ror: ROR ID of a funder
    * funder_name: name of the funding agency (required)
    * award_number: grant number or other fund identifier"""

    class Meta:
        name = "assertion"
        namespace = "http://www.crossref.org/fundref.xsd"

    provider: AssertionProvider = field(
        default=AssertionProvider.PUBLISHER,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[AssertionName] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
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
                    "name": "assertion",
                    "type": ForwardRef("Assertion"),
                },
            ),
        },
    )


@dataclass
class Program:
    """Information about registering funding data is available in our documentation: https://www.crossref.org/documentation/funder-registry/funding-data-deposits/"""

    class Meta:
        name = "program"
        namespace = "http://www.crossref.org/fundref.xsd"

    assertion: list[Assertion] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    name: str = field(
        init=False,
        default="fundref",
        metadata={
            "type": "Attribute",
        },
    )
