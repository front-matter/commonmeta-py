from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .xml import LangValue

__NAMESPACE__ = "http://www.w3.org/1999/xlink"


class ActuateType(Enum):
    ON_LOAD = "onLoad"
    ON_REQUEST = "onRequest"
    OTHER = "other"
    NONE = "none"


class ShowType(Enum):
    NEW = "new"
    REPLACE = "replace"
    EMBED = "embed"
    OTHER = "other"
    NONE = "none"


class TypeType(Enum):
    SIMPLE = "simple"
    EXTENDED = "extended"
    TITLE = "title"
    RESOURCE = "resource"
    LOCATOR = "locator"
    ARC = "arc"


@dataclass(slots=True, kw_only=True)
class ArcType:
    """
    :ivar type_value:
    :ivar arcrole:
    :ivar title:
    :ivar show:
    :ivar actuate:
    :ivar from_value:
    :ivar to: from and to have default behavior when values are missing
    """

    class Meta:
        name = "arcType"

    type_value: TypeType = field(
        init=False,
        default=TypeType.ARC,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "required": True,
        },
    )
    arcrole: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: None | ShowType = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: None | ActuateType = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    from_value: None | str = field(
        default=None,
        metadata={
            "name": "from",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    to: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )


@dataclass(slots=True, kw_only=True)
class Extended:
    """
    Intended for use as the type of user-declared elements to make them
    extended links.

    Note that the elements referenced in the content model are all
    abstract. The intention is that by simply declaring elements with these
    as their substitutionGroup, all the right things will happen.
    """

    class Meta:
        name = "extended"

    type_value: TypeType = field(
        init=False,
        default=TypeType.EXTENDED,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "required": True,
        },
    )
    role: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )


@dataclass(slots=True, kw_only=True)
class LocatorType:
    """
    :ivar type_value:
    :ivar href:
    :ivar role:
    :ivar title:
    :ivar label: label is not required, but locators have no particular
        XLink function if they are not labeled.
    """

    class Meta:
        name = "locatorType"

    type_value: TypeType = field(
        init=False,
        default=TypeType.LOCATOR,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "required": True,
        },
    )
    href: str = field(
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        }
    )
    role: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    label: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )


@dataclass(slots=True, kw_only=True)
class ResourceType:
    class Meta:
        name = "resourceType"

    type_value: TypeType = field(
        init=False,
        default=TypeType.RESOURCE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "required": True,
        },
    )
    role: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    label: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
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


@dataclass(slots=True, kw_only=True)
class Simple:
    """
    Intended for use as the type of user-declared elements to make them
    simple links.
    """

    class Meta:
        name = "simple"

    type_value: TypeType = field(
        init=False,
        default=TypeType.SIMPLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    arcrole: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "min_length": 1,
        },
    )
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: None | ShowType = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: None | ActuateType = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
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


@dataclass(slots=True, kw_only=True)
class TitleEltType:
    """
    :ivar type_value:
    :ivar lang: xml:lang is not required, but provides much of the
        motivation for title elements in addition to attributes, and so
        is provided here for convenience.
    :ivar content:
    """

    class Meta:
        name = "titleEltType"

    type_value: TypeType = field(
        init=False,
        default=TypeType.TITLE,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
            "required": True,
        },
    )
    lang: None | str | LangValue = field(
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


@dataclass(slots=True, kw_only=True)
class Arc(ArcType):
    class Meta:
        name = "arc"
        namespace = "http://www.w3.org/1999/xlink"


@dataclass(slots=True, kw_only=True)
class Locator(LocatorType):
    class Meta:
        name = "locator"
        namespace = "http://www.w3.org/1999/xlink"


@dataclass(slots=True, kw_only=True)
class Resource(ResourceType):
    class Meta:
        name = "resource"
        namespace = "http://www.w3.org/1999/xlink"


@dataclass(slots=True, kw_only=True)
class Title(TitleEltType):
    class Meta:
        name = "title"
        namespace = "http://www.w3.org/1999/xlink"
