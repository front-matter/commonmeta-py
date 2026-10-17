"""Property-based tests for dig and the case helpers"""

import pytest

# hypothesis is a dev dependency on Python 3.11+ only.
pytest.importorskip("hypothesis")

from hypothesis import given  # noqa: E402
from hypothesis import strategies as st  # noqa: E402

from commonmeta.base_utils import camel_case, dig, kebab_case, pascal_case  # noqa: E402

DEFAULT = object()

keys = st.text(st.characters(codec="ascii", categories=["L"]), min_size=1, max_size=5)
values = st.integers() | st.text(max_size=5)
trees = st.recursive(
    values,
    lambda children: st.lists(children, min_size=1, max_size=3)
    | st.dictionaries(keys, children, min_size=1, max_size=3),
    max_leaves=10,
)


@st.composite
def tree_and_path(draw):
    """A nested object, a path into it in both spellings, and what is there."""
    obj = draw(trees)
    node, dotted, bracketed = obj, [], ""
    while isinstance(node, (dict, list)) and draw(st.booleans()):
        if isinstance(node, dict):
            key = draw(st.sampled_from(sorted(node)))
            bracketed += f"['{key}']" if bracketed else key
        else:
            key = draw(st.integers(0, len(node) - 1))
            bracketed += f"[{key}]"
        dotted.append(str(key))
        node = node[key]
    return obj, ".".join(dotted), bracketed, node


@given(tree_and_path())
def test_dig_follows_a_path(case):
    obj, dotted, bracketed, expected = case
    if dotted:
        assert dig(obj, dotted) == expected
    if bracketed and not bracketed.startswith("["):
        assert dig(obj, bracketed) == expected


@given(trees, st.text(max_size=12))
def test_dig_never_raises(obj, path):
    dig(obj, path, DEFAULT)


@given(trees, keys)
def test_dig_answers_default_for_a_missing_key(obj, key):
    # Generated keys are at most five letters, so this one is never there.
    assert dig({"x": obj}, f"x.{key}missing", DEFAULT) is DEFAULT


# ASCII only: str.lower() and str.upper() are not inverses outside it, so
# "İ" lowercases to two characters.
words = st.text(
    st.sampled_from(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-"
    ),
    max_size=20,
)


@given(words)
def test_kebab_case_is_idempotent(string):
    assert kebab_case(kebab_case(string)) == kebab_case(string)


@given(words)
def test_case_helpers_agree_on_the_words(string):
    """Every case helper splits a string into the same words, so going through
    kebab-case first changes nothing."""
    kebab = kebab_case(string)
    assert pascal_case(kebab) == pascal_case(string)
    assert camel_case(kebab) == camel_case(string)
    assert kebab_case(pascal_case(string)).replace("-", "") == kebab.replace("-", "")


@given(words)
def test_case_helpers_keep_the_characters(string):
    letters = "".join(c for c in string if c.isalnum()).lower()
    for convert in (pascal_case, camel_case, kebab_case):
        assert convert(string).replace("-", "").lower() == letters
