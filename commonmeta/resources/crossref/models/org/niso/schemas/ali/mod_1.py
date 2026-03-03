from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://www.niso.org/schemas/ali/1.0/"


@dataclass(slots=True, kw_only=True)
class FreeToRead:
    """
    <div> <h3>Free to Read (Niso Ali)</h3> </div>.
    """

    class Meta:
        name = "free_to_read"
        namespace = "http://www.niso.org/schemas/ali/1.0/"

    content_type: None | str = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    end_date: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: None | str = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    start_date: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(slots=True, kw_only=True)
class LicenseRef:
    """
    <div> <h3>License Reference (Niso Ali)</h3> </div>.
    """

    class Meta:
        name = "license_ref"
        namespace = "http://www.niso.org/schemas/ali/1.0/"

    content_type: None | str = field(
        default=None,
        metadata={
            "name": "content-type",
            "type": "Attribute",
        },
    )
    id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    specific_use: None | str = field(
        default=None,
        metadata={
            "name": "specific-use",
            "type": "Attribute",
        },
    )
    start_date: None | str = field(
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
        },
    )
