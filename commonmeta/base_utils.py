"""Base utilities for commonmeta-py"""

import html
import re
import uuid
from datetime import datetime
from os import path
from typing import Optional, Union

import nh3
import pydash as py_
import xmltodict


def wrap(item) -> list:
    """Turn None, dict, or list into list"""
    if item is None:
        return []
    if isinstance(item, list):
        return item
    return [item]


def unwrap(lst: list) -> Optional[Union[dict, list]]:
    """Turn list into dict or None, depending on list size"""
    if len(lst) == 0:
        return None
    if len(lst) == 1:
        return lst[0]
    return lst


def presence(
    item: Optional[Union[dict, list, str]],
) -> Optional[Union[dict, list, str]]:
    """Turn empty list, dict or str into None"""
    return None if item is None or len(item) == 0 or item == [{}] else item


def compact(dict_or_list: Union[dict, list]) -> Optional[Union[dict, list]]:
    """Remove None from dict or list"""
    if isinstance(dict_or_list, dict):
        return {k: v for k, v in dict_or_list.items() if v is not None}
    if isinstance(dict_or_list, list):
        lst = [compact(i) for i in dict_or_list]
        return lst if len(lst) > 0 else None

    return None


def parse_attributes(
    element: Union[str, dict, list], **kwargs
) -> Optional[Union[str, list]]:
    """extract attributes from a string, dict or list"""

    def parse_item(item):
        if isinstance(item, dict):
            return item.get(html.unescape(content), None)
        return html.unescape(item)

    content = kwargs.get("content", "#text")
    if isinstance(element, str) and kwargs.get("content", None) is None:
        return html.unescape(element)
    if isinstance(element, dict):
        return element.get(html.unescape(content), None)
    if isinstance(element, list):
        arr = [parse_item(i) for i in element if i]
        arr = arr[0] if len(arr) > 0 and kwargs.get("first") else unwrap(arr)
        return arr


def parse_xml(string: Optional[str], **kwargs) -> Optional[Union[dict, list]]:
    """Parse XML into dict using xmltodict. Set default options, and options for Crossref XML"""
    if string is None or string == "{}":
        return None
    if path.exists(string):
        with open(string, encoding="utf-8") as file:
            string = file.read()

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
    return xmltodict.parse(string, **kwargs)


def unparse_xml(input: Optional[dict], **kwargs) -> str:
    """Unparse (dump) dict into XML using xmltodict. Set default options, and options for Crossref XML"""
    if input is None:
        return None
    if kwargs.get("dialect", None) == "crossref":
        # Add additional logic for crossref dialect
        # add body and root element as wrapping elements
        type = next(iter(input))
        attributes = input.get(type)
        input.pop(type)

        if type == "book":
            book_metadata = py_.get(input, "book_metadata") or {}
            input.pop("book_metadata")
            book_metadata = {**book_metadata, **input}
            input = {"book": {**attributes, "book_metadata": book_metadata}}
        elif type == "database":
            database_metadata = py_.get(input, "database_metadata") or {}
            input.pop("database_metadata")
            val = input.pop("publisher_item")
            institution = input.pop("institution", None)
            database_metadata = {**{"titles": val}, **database_metadata}
            database_metadata["institution"] = institution or {}
            component = input.pop("component", None)
            input = {
                "database": {
                    **attributes,
                    "database_metadata": database_metadata,
                    "component_list": {"component": component | input},
                }
            }
        elif type == "journal":
            journal_metadata = py_.get(input, "journal_metadata") or {}
            journal_issue = py_.get(input, "journal_issue") or {}
            journal_article = py_.get(input, "journal_article") or {}
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
        elif type == "proceedings_article":
            proceedings_metadata = py_.get(input, "proceedings_metadata") or {}
            input.pop("proceedings_metadata")
            input = {
                "proceedings": {
                    **attributes,
                    "proceedings_metadata": proceedings_metadata,
                    "conference_paper": input,
                }
            }
        elif type == "sa_component":
            component = py_.get(input, "component") or {}
            input.pop("component")
            input = {
                "sa_component": {
                    **attributes,
                    "component_list": {"component": component | input},
                }
            }
        else:
            input = {type: attributes | input}

        doi_batch = {
            "@xmlns": "http://www.crossref.org/schema/5.4.0",
            "@version": "5.4.0",
            "head": get_crossref_xml_head(input),
            "body": input,
        }
        input = {"doi_batch": doi_batch}
    kwargs["pretty"] = True
    kwargs["indent"] = "  "
    kwargs.pop("dialect", None)
    return xmltodict.unparse(input, **kwargs)


def unparse_xml_list(input: Optional[list], **kwargs) -> str:
    """Unparse (dump) list into XML using xmltodict. Set default options, and options for Crossref XML"""
    if input is None:
        return None
    if kwargs.get("dialect", None) == "crossref":
        # Add additional logic for crossref dialect
        # add body and root element as wrapping elements

        # Group items by type with minimal grouping
        items_by_type = {}

        for item in wrap(input):
            type = next(iter(item))
            attributes = item.get(type)
            item.pop(type)

            # handle nested book_metadata and journal structure as in unparse_xml
            if type == "book":
                book_metadata = py_.get(item, "book_metadata") or {}
                item.pop("book_metadata")
                book_metadata = {**book_metadata, **item}
                item = {"book": {**attributes, "book_metadata": book_metadata}}
            elif type == "database":
                database_metadata = py_.get(item, "database_metadata") or {}
                item.pop("database_metadata")
                database_metadata = {**database_metadata, **item}
                item = {
                    "database": {**attributes, "database_metadata": database_metadata}
                }
            elif type == "journal":
                journal_metadata = py_.get(item, "journal_metadata") or {}
                journal_issue = py_.get(item, "journal_issue") or {}
                journal_article = py_.get(item, "journal_article") or {}
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
            elif type == "sa_component":
                component = py_.get(input, "component") or {}
                item.pop("component")
                item = {
                    "sa_component": {
                        **attributes,
                        "component_list": {"component": component | item},
                    }
                }
            else:
                item = {type: attributes | item}

            # Add item to appropriate type bucket
            if type not in items_by_type:
                items_by_type[type] = []
            items_by_type[type].append(item[type])

        # Create the final structure with body containing all grouped items
        body_content = {}
        for type_key, items in items_by_type.items():
            if len(items) == 1:
                body_content[type_key] = items[0]  # Use single item without array
            else:
                body_content[type_key] = items  # Use array when multiple items
        head = kwargs["head"] or {}
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

    kwargs["pretty"] = True
    kwargs["indent"] = "  "
    kwargs.pop("dialect", None)
    kwargs.pop("head", None)
    return xmltodict.unparse(output, **kwargs)


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
