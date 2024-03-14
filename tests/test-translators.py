# pylint: disable=invalid-name
"""Test translators."""

from os import path
import re
import pytest  # noqa: F401

from commonmeta.translators import web_translator
from bs4 import BeautifulSoup

def test_web_translator_arxiv():
    """Test web translator for arXiv"""
    filepath = path.join(path.dirname(__file__), "fixtures", "arxiv.html")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    soup = BeautifulSoup(string, "html.parser")
    metadata = web_translator(soup, "https://arxiv.org/abs/1902.02534")
    assert re.match(r"https://doi.org/10.48550/arXiv.1902.02534", metadata["@id"])