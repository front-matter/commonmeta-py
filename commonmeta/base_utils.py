"""Base utilities for commonmeta-py"""
import html
from os import path
import re
import xmltodict
from typing import Optional, Union
import nh3


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
    """Parse XML into dict. Set default options, and options for Crossref XML"""
    if string is None:
        return None
    if path.exists(string):
        with open(string, encoding="utf-8") as file:
            string = file.read()

    if kwargs.get("dialect", None) == "crossref":
        # remove namespaces from xml
        namespaces = {
            "http://www.crossref.org/schema/5.3.1": None,
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
            "item",
            "citation",
            "program",
            "related_item",
        }

    kwargs["attr_prefix"] = ""
    kwargs["dict_constructor"] = dict
    kwargs.pop("dialect", None)
    return xmltodict.parse(string, **kwargs)


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
