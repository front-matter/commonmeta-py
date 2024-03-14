"""Web translators for commonmeta. Using BeautifulSoup to extract metadata from web pages."""

from furl import furl


def web_translator(soup, url: str):
    """Extract metadata from web pages"""
    f = furl(url)
    if f.host == "arxiv.org":
        return arxiv_translator(soup)
    return {}


def arxiv_translator(soup):
    """Extract metadata from arXiv. Find the DOI and lookup the metadata via DataCite."""
    arxiv_id = soup.select_one("meta[name='citation_arxiv_id']")
    if arxiv_id is None:
        return None
    return {"@id": f"https://doi.org/10.48550/arXiv.{arxiv_id['content']}"}
