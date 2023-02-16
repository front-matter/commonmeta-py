"""Base utilities for Talbot"""
import html
import re
from typing import Optional, Union
import bleach
import pydash as py_

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


def presence(item: Optional[Union[dict, list, str]]) -> Optional[Union[dict, list, str]]:
    """Turn empty list, dict or str into None"""
    return None if item is None or len(item) == 0 else item


def compact(dict_or_list: Union[dict, list]) -> Optional[Union[dict, list]]:
    """Remove None from dict or list"""        
    if isinstance(dict_or_list, dict):
        return {k: v for k, v in dict_or_list.items() if v is not None}
    if isinstance(dict_or_list, list):
        lst = [compact(i) for i in dict_or_list]
        return lst if len(lst) > 0 else None

    return None


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


def sanitize(text: str, tags=None, strip=True):
    """Sanitize text"""
    # default whitelisted HTML tags
    tags = tags or {"b", "br", "code", "em", "i", "sub", "sup", "strong"}
    string = bleach.clean(text, tags=tags, strip=strip)
    # remove excessive internal whitespace
    return " ".join(re.split(r"\s+", string, flags=re.UNICODE))
