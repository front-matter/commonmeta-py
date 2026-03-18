from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.crossref.org/clinicaltrials.xsd"


class ClinicalTrialNumberType(Enum):
    PRE_RESULTS = "preResults"
    RESULTS = "results"
    POST_RESULTS = "postResults"


@dataclass
class ClinicalTrialNumber:
    """
    :ivar registry: The clinical trial identifier related to the
        article.
    :ivar type_value: Used to identify the article publication date in
        relation to the issuance of the trial results
    :ivar content:
    """

    class Meta:
        name = "clinical-trial-number"
        namespace = "http://www.crossref.org/clinicaltrials.xsd"

    registry: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 12,
            "max_length": 200,
            "pattern": r"10.18810/[a-z-]+",
        },
    )
    type_value: Optional[ClinicalTrialNumberType] = field(
        default=None,
        metadata={
            "name": "type",
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
class Program:
    """Accommodates deposit of linked clincal trials metadata.

    The clinical-trial-number value will be a string that must match a
    specific pattern appropriate for a given clinical trial registry.
    The registry is identified in the required attribute 'registry' and
    must be the DOI of a recognized registry (see
    http://dx.doi.org/10.18810/registries)
    """

    class Meta:
        name = "program"
        namespace = "http://www.crossref.org/clinicaltrials.xsd"

    clinical_trial_number: list[ClinicalTrialNumber] = field(
        default_factory=list,
        metadata={
            "name": "clinical-trial-number",
            "type": "Element",
        },
    )
