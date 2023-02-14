"""Base utilities for Talbot"""
import html
import re
import bleach
from typing import Optional, Union

def wrap(item):
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


def presence(item: Optional[Union[dict, list, str]]) -> Optional[Union[dict, list, str]]:
    """Turn empty list, dict or str into None"""
    return None if item is None or len(item) == 0 else item


def compact(dict_or_list: Optional[Union[dict, list]]) -> Optional[Union[dict, list]]:
    """Remove None from dict or list"""
    if dict_or_list is None:
        return None
    if isinstance(dict_or_list, dict):
        return {k: v for k, v in dict_or_list.items() if v is not None}
    if isinstance(dict_or_list, list):
        arr = list(map(lambda x: compact(x), dict_or_list))
        return None if len(arr) == 0 else arr


def parse_attributes(element, **kwargs):
    """extract attributes from a string, dict or list"""
    content = kwargs.get("content", "__content__")

    if isinstance(element, str) and kwargs.get("content", None) is None:
        return html.unescape(element)
    if isinstance(element, dict):
        return element.get(html.unescape(content), None)
    if isinstance(element, list):
        arr = list(
            map(
                lambda x: x.get(html.unescape(content), None)
                if isinstance(x, dict)
                else x,
                element,
            )
        )
        arr = arr[0] if kwargs.get("first") else unwrap(arr)
        return arr
    

def camel_case(text: Optional[str]) -> Optional[str]:
    """Convert text to camel case"""
    if text is None:
        return None
    string = text.replace("-", " ").replace("_", " ")
    lst = string.split()
    if len(lst) == 0:
        return text
    return lst[0] + "".join(i.capitalize() for i in lst[1:])


def sanitize(text, **kwargs):
    """Sanitize text"""
    tags = kwargs.get("tags", None) or frozenset(
        {"b", "br", "code", "em", "i", "sub", "sup", "strong"}
    )
    content = kwargs.get("content", None) or "__content__"
    first = kwargs.get("first", True)
    strip = kwargs.get("strip", True)

    if isinstance(text, str):
        string = bleach.clean(text, tags=tags, strip=strip)
        # remove excessive internal whitespace
        return " ".join(re.split(r"\s+", string, flags=re.UNICODE))
        # return re.sub(r'\\s\\s+', ' ', string)
    if isinstance(text, dict):
        return sanitize(text.get(content, None))
    if isinstance(text, list):
        if len(text) == 0:
            return None

        lst = []
        for elem in text:
            lst.append(
                sanitize(elem.get(content, None)) if isinstance(
                    elem, dict) else sanitize(elem)
            )  # uniq
        return lst[0] if first else unwrap(lst)
