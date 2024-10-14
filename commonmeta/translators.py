"""Web translators for commonmeta. Using BeautifulSoup to extract metadata from web pages."""

from furl import furl
import re

from .doi_utils import doi_as_url


def web_translator(soup, url: str):
    """Extract metadata from web pages"""
    f = furl(url)
    if f.host == "arxiv.org":
        return arxiv_translator(soup)
    elif f.host == "datacite.org":
        return datacite_translator(soup)
    elif f.host == "app.pan.pl":
        return pan_translator(soup)
    return {}


def arxiv_translator(soup):
    """Extract metadata from arXiv. Find the DOI and return it."""
    arxiv_id = soup.select_one("meta[name='citation_arxiv_id']")
    if arxiv_id is None:
        return {}
    return {"@id": f"https://doi.org/10.48550/arXiv.{arxiv_id['content']}"}


def datacite_translator(soup):
    """Extract metadata from DataCite blog posts. Find the DOI and return it."""
    doi = soup.select_one("div#citation")
    if doi is None:
        return {}
    return {"@id": doi.get("data-doi", None)}


def pan_translator(soup):
    """Extract metadata from Acta Palaeontologica Polonica. Find the DOI and return it."""
    caption = soup.select_one("p.caption div.vol").text
    match = re.search(
        r"doi:(10\.4202/.+)\Z",
        caption,
    )
    if match is None:
        return {}
    doi = doi_as_url(match.group(1))
    return {"@id": doi}
