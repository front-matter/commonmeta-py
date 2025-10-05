"""Base utilities for commonmeta-py"""

from __future__ import annotations

import html
import re
import uuid
from datetime import datetime
from os import path
from typing import Any, Generator, Iterable, TypeVar

import nh3
import xmltodict

T = TypeVar("T")


def _tokens(path: str | Iterable[Any]) -> Generator[str | int, None, None]:
    """Yield tokens from a dot/bracket path like a.b[0]['c'] or a.0.b"""
    if isinstance(path, (list, tuple)):
        yield from path
        return
    if not isinstance(path, str) or not path:
        return

    i, n = 0, len(path)
    buf = []
    while i < n:
        c = path[i]

        if c == ".":  # end of a token
            if buf:
                token = "".join(buf)
                # Convert numeric strings to integers for list indexing
                if token.isdigit():
                    yield int(token)
                else:
                    yield token
                buf = []
            i += 1
        elif c == "[":  # bracket expression
            if buf:
                token = "".join(buf)
                # Convert numeric strings to integers for list indexing
                if token.isdigit():
                    yield int(token)
                else:
                    yield token
                buf = []
            i += 1
            if path[i] in ("'", '"'):  # quoted key
                quote = path[i]
                i += 1
                start = i
                while i < n and path[i] != quote:
                    i += 1
                yield path[start:i]
                i += 2  # skip closing quote + ]
            else:  # integer index
                start = i
                while i < n and path[i].isdigit():
                    i += 1
                yield int(path[start:i])
                i += 1  # skip ]
        else:
            buf.append(c)
            i += 1

    if buf:
        token = "".join(buf)
        # Convert numeric strings to integers for list indexing
        if token.isdigit():
            yield int(token)
        else:
            yield token


def dig(obj: Any, path: str | Iterable[Any], default: Any = None) -> Any:
    """
    Safe nested getter similar to pydash.get.
    """
    cur = obj
    for key in _tokens(path):
        try:
            if isinstance(cur, dict):
                cur = cur[key]
            elif isinstance(cur, (list, tuple)) and isinstance(key, int):
                cur = cur[key]
            else:
                # getattr expects a string attribute name
                key_str = str(key) if not isinstance(key, str) else key
                cur = getattr(cur, key_str)
        except (KeyError, IndexError, AttributeError, TypeError):
            return default
    return cur


def unique(iterable: Iterable[T] | None) -> list[T]:
    """
    Return a list of unique values in the given iterable, preserving order.
    Returns empty list if iterable is None.
    Handles unhashable types like dicts by using list comparison.
    """
    if iterable is None:
        return []

    result = []
    for item in iterable:
        if item not in result:
            result.append(item)
    return result


def omit(obj: dict[str, Any] | None, *keys) -> dict[str, Any]:
    """
    Return a new dict without the specified keys.
    Can accept keys as separate arguments or as an iterable.
    Returns empty dict if obj is None.
    """
    if obj is None:
        return {}

    # If first argument is an iterable and no other args, treat it as the keys
    if len(keys) == 1 and hasattr(keys[0], "__iter__") and not isinstance(keys[0], str):
        keys = keys[0]

    keys = set(keys)
    return {k: v for k, v in obj.items() if k not in keys}


def keep(obj: dict[str, Any] | None, keys: Iterable[str]) -> dict[str, Any]:
    """
    Return a new dict with only the specified keys.
    Returns empty dict if obj is None.
    """
    if obj is None:
        return {}

    keys = set(keys)
    return {k: v for k, v in obj.items() if k in keys}


def wrap(item: dict | list | str | None) -> list:
    """Turn None, dict, or list into list"""
    if item is None:
        return []
    if isinstance(item, list):
        return item
    return [item]


def unwrap(lst: list) -> dict | list | None:
    """Turn list into dict or None, depending on list size"""
    if len(lst) == 0:
        return None
    if len(lst) == 1:
        return lst[0]
    return lst


def first(lst: list | None) -> Any:
    """Return the first element of a list or None if the list is empty or None."""
    if lst is not None and len(lst) > 0:
        return lst[0]
    return None


def flatten(array: Iterable[Iterable[Any]]) -> list:
    """
    Flatten a list one level deep.
    """
    result = []
    for item in array:
        if isinstance(item, (list, tuple)):
            result.extend(item)
        else:
            result.append(item)
    return result


def presence(
    item: dict | list | str | None,
) -> dict | list | str | None:
    """Turn empty list, dict or str into None"""
    return None if item is None or len(item) == 0 or item == [{}] else item


def compact(obj: dict | None) -> dict:
    """Remove None values from dict"""
    if obj is None:
        return {}
    return {k: v for k, v in obj.items() if v is not None}


def scrub(list_obj: Iterable[dict] | None) -> list | None:
    """Remove None values from list recursively"""
    if list_obj is None:
        return None
    lst = [compact(i) for i in list_obj]
    return lst if len(lst) > 0 else None


def _split_words(s: str) -> list[str]:
    """Split string into words by space, underscore, hyphen, and case changes."""
    words, current = [], []
    for i, ch in enumerate(s):
        if ch in (" ", "_", "-"):
            if current:
                words.append("".join(current))
                current = []
        elif ch.isupper() and current and not current[-1].isupper():
            # Start of a new word on case change (e.g. fooBar -> foo, Bar)
            words.append("".join(current))
            current = [ch]
        else:
            current.append(ch)
    if current:
        words.append("".join(current))
    return words


def pascal_case(s: str) -> str:
    """Convert string to PascalCase (HelloWorld)."""
    words = _split_words(s)
    return "".join(w[:1].upper() + w[1:].lower() for w in words if w)


def camel_case(s: str) -> str:
    """Convert string to camelCase (helloWorld)."""
    words = _split_words(s)
    if not words:
        return ""
    first = words[0].lower()
    rest = [w[:1].upper() + w[1:].lower() for w in words[1:] if w]
    return first + "".join(rest)


def kebab_case(s: str) -> str:
    """Convert string to kebab-case (hello-world)."""
    words = _split_words(s)
    return "-".join(w.lower() for w in words if w)


def parse_attributes(element: str | dict | list | None, **kwargs) -> list[str]:
    """Extract attributes from a string, dict or list.

    Args:
        element: Input to parse (str, dict, list, or None)
        **kwargs: Optional parameters:
            - content: Key to extract from dict (default: "#text")

    Returns:
        - list of extracted strings, or empty list if none found
    """

    def parse_item(item) -> str | None:
        """Parse a single item from the element list"""
        if isinstance(item, dict):
            return item.get(html.unescape(content), None)
        return html.unescape(item) if isinstance(item, str) else None

    if element is None:
        return []

    content = kwargs.get("content", "#text")
    if isinstance(element, str) and kwargs.get("content", None) is None:
        return [html.unescape(element)]
    if isinstance(element, dict):
        value = element.get(html.unescape(content), None)
        return [value] if value is not None else []
    if isinstance(element, list):
        arr = [parse_item(i) for i in element if i]
        # Filter out None values
        arr = [item for item in arr if item is not None]
        arr = [arr[0]] if len(arr) > 0 and kwargs.get("first") else arr
        return arr

    return []


def parse_xml(string: str | bytes | None, **kwargs) -> dict | list | None:
    """Parse XML into dict using xmltodict. Set default options, and options for Crossref XML"""
    if string is None or string == "{}":
        return None

    # Convert to string if it's a file path
    xml_string: str | bytes
    if isinstance(string, (str, bytes)) and path.exists(string):
        with open(string, encoding="utf-8") as file:
            xml_string = file.read()
    else:
        xml_string = string

    if kwargs.get("dialect", None) == "crossref":
        # remove namespaces from xml
        namespaces = {
            "http://www.crossref.org/schema/5.4.0": None,
            "http://www.crossref.org/qrschema/3.0": None,
            "http://www.crossref.org/xschema/1.0": None,
            "http://www.crossref.org/xschema/1.1": None,
            "http://www.crossref.org/AccessIndicators.xsd": None,
            "http://www.crossref.org/relations.xsd": None,
            "http://www.crossref.org/fundref.xsd": None,
            "http://www.ncbi.nlm.nih.gov/JATS1": None,
        }

        kwargs["process_namespaces"] = True
        kwargs["namespaces"] = namespaces
        kwargs["force_list"] = {
            "person_name",
            "organization",
            "titles",
            "abstract",
            "item",
            "citation",
            "program",
            "related_item",
        }

    kwargs["attr_prefix"] = ""
    kwargs["dict_constructor"] = dict
    kwargs.pop("dialect", None)
    return xmltodict.parse(xml_string, **kwargs)


def unparse_xml(input: dict | None, **kwargs) -> bytes | None:
    """Unparse (dump) dict into XML using xmltodict. Set default options, and options for Crossref XML"""
    if input is None:
        return None
    if kwargs.get("dialect", None) == "crossref":
        # Add additional logic for crossref dialect
        # add body and root element as wrapping elements
        item_type = next(iter(input))
        attributes = input.get(item_type) or {}
        input.pop(item_type)

        if item_type == "book":
            book_metadata = dig(input, "book_metadata") or {}
            input.pop("book_metadata")
            book_metadata = {**book_metadata, **input}
            input = {"book": {**attributes, "book_metadata": book_metadata}}
        elif item_type == "database":
            database_metadata = dig(input, "database_metadata") or {}
            input.pop("database_metadata")
            val = input.pop("publisher_item")
            institution = input.pop("institution", None)
            database_metadata = {**{"titles": val}, **database_metadata}
            database_metadata["institution"] = institution or {}
            component = input.pop("component", None) or {}
            input = {
                "database": {
                    **attributes,
                    "database_metadata": database_metadata,
                    "component_list": {"component": component | input},
                }
            }
        elif item_type == "journal":
            journal_metadata = dig(input, "journal_metadata") or {}
            journal_issue = dig(input, "journal_issue") or {}
            journal_article = dig(input, "journal_article") or {}
            input.pop("journal_metadata")
            input.pop("journal_issue")
            input.pop("journal_article")
            input = {
                "journal": {
                    "journal_metadata": journal_metadata,
                    "journal_issue": journal_issue,
                    "journal_article": journal_article | input,
                }
            }
        elif item_type == "proceedings_article":
            proceedings_metadata = dig(input, "proceedings_metadata") or {}
            input.pop("proceedings_metadata")
            input = {
                "proceedings": {
                    **attributes,
                    "proceedings_metadata": proceedings_metadata,
                    "conference_paper": input,
                }
            }
        elif item_type == "sa_component":
            component = dig(input, "component") or {}
            input.pop("component")
            input = {
                "sa_component": {
                    **attributes,
                    "component_list": {"component": component | input},
                }
            }
        else:
            input = {item_type: attributes | input}

        head = kwargs.get("head", {}) or {}
        doi_batch = {
            "@xmlns": "http://www.crossref.org/schema/5.4.0",
            "@xmlns:ai": "http://www.crossref.org/AccessIndicators.xsd",
            "@xmlns:rel": "http://www.crossref.org/relations.xsd",
            "@xmlns:fr": "http://www.crossref.org/fundref.xsd",
            "@version": "5.4.0",
            "head": get_crossref_xml_head(head),
            "body": input,
        }
        output: dict[str, Any] = {"doi_batch": doi_batch}
    else:
        output: dict[str, Any] = input
    kwargs["pretty"] = True
    kwargs["indent"] = "  "
    kwargs.pop("dialect", None)
    kwargs.pop("head", None)
    return xmltodict.unparse(output, **kwargs).encode("utf-8")


def unparse_xml_list(input: list | None, **kwargs) -> bytes | None:
    """Unparse (dump) list into XML using xmltodict. Set default options, and options for Crossref XML"""
    if input is None:
        return None
    if kwargs.get("dialect", None) == "crossref":
        # Add additional logic for crossref dialect
        # add body and root element as wrapping elements

        # Group items by type with minimal grouping
        items_by_type: dict[str, list] = {}

        for item in wrap(input):
            item_type = next(iter(item))
            attributes = item.get(item_type) or {}
            item.pop(item_type)

            # handle nested book_metadata and journal structure as in unparse_xml
            if item_type == "book":
                book_metadata = dig(item, "book_metadata") or {}
                item.pop("book_metadata")
                book_metadata = {**book_metadata, **item}
                item = {"book": {**attributes, "book_metadata": book_metadata}}
            elif item_type == "database":
                database_metadata = dig(item, "database_metadata") or {}
                item.pop("database_metadata")
                database_metadata = {**database_metadata, **item}
                item = {
                    "database": {**attributes, "database_metadata": database_metadata}
                }
            elif item_type == "journal":
                journal_metadata = dig(item, "journal_metadata") or {}
                journal_issue = dig(item, "journal_issue") or {}
                journal_article = dig(item, "journal_article") or {}
                item.pop("journal_metadata")
                item.pop("journal_issue")
                item.pop("journal_article")
                item = {
                    "journal": {
                        "journal_metadata": journal_metadata,
                        "journal_issue": journal_issue,
                        "journal_article": journal_article | item,
                    }
                }
            elif item_type == "sa_component":
                component = dig(item, "component") or {}
                item.pop("component")
                item = {
                    "sa_component": {
                        **attributes,
                        "component_list": {"component": component | item},
                    }
                }
            else:
                item = {item_type: attributes | item}

            # Add item to appropriate type bucket
            if item_type not in items_by_type:
                items_by_type[item_type] = []
            items_by_type[item_type].append(item[item_type])

        # Create the final structure with body containing all grouped items
        body_content: dict[str, Any] = {}
        for type_key, items in items_by_type.items():
            if len(items) == 1:
                body_content[type_key] = items[0]  # Use single item without array
            else:
                body_content[type_key] = items  # Use array when multiple items
        head = kwargs.get("head", {}) or {}
        doi_batch = {
            "@xmlns": "http://www.crossref.org/schema/5.4.0",
            "@xmlns:ai": "http://www.crossref.org/AccessIndicators.xsd",
            "@xmlns:rel": "http://www.crossref.org/relations.xsd",
            "@xmlns:fr": "http://www.crossref.org/fundref.xsd",
            "@version": "5.4.0",
            "head": get_crossref_xml_head(head),
            "body": body_content,
        }
        output = {"doi_batch": doi_batch}
    else:
        output = {"body": input}

    kwargs["pretty"] = True
    kwargs["indent"] = "  "
    kwargs.pop("dialect", None)
    kwargs.pop("head", None)
    return xmltodict.unparse(output, **kwargs).encode("utf-8")


def get_crossref_xml_head(metadata: dict) -> dict:
    """Get head element for Crossref XML"""

    return {
        "doi_batch_id": str(uuid.uuid4()),
        "timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
        "depositor": {
            "depositor_name": metadata.get("depositor", None) or "test",
            "email_address": metadata.get("email", None) or "info@example.org",
        },
        "registrant": metadata.get("registrant", None) or "test",
    }


def sanitize(text: str, **kwargs) -> str:
    """Sanitize text"""
    # default whitelisted HTML tags
    tags = kwargs.get("tags", None) or {
        "b",
        "br",
        "code",
        "em",
        "i",
        "sub",
        "sup",
        "strong",
    }
    attributes = kwargs.get("attributes", None)
    string = nh3.clean(text, tags=tags, attributes=attributes, link_rel=None)
    # remove excessive internal whitespace
    return " ".join(re.split(r"\s+", string, flags=re.UNICODE))
