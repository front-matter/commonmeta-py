import pytest
from talbot.author_utils import cleanup_author, authors_as_string, get_authors, get_affiliations

def test_cleanup_author():
    "cleanup_author"
    assert "John Smith" == cleanup_author("John Smith")
    assert "Smith, John" == cleanup_author("Smith, John")
    assert "Smith, J." == cleanup_author("Smith, J.")

def test_authors_as_string():
    "authors_as_string"
    authors = [
        {'type': 'Person',
         'id': 'http://orcid.org/0000-0003-0077-4738',
         'name': 'Matt Jones'},
        {'type': 'Person',
         'id': 'http://orcid.org/0000-0002-2192-403X',
         'name': 'Peter Slaughter'},
        {'type': 'Organization',
         'name': 'University of California, Santa Barbara'}
    ]
    assert "Matt Jones and Peter Slaughter" == authors_as_string(authors[0:2])
    # single author
    assert "Matt Jones" == authors_as_string(authors[0])
    # no authors
    assert None == authors_as_string(None)
    # with organization
    assert "Matt Jones and Peter Slaughter and {University of California, Santa Barbara}" == authors_as_string(authors)

# def test_get_authors():
#     "get_authors"
#     authors = [
#         {'type': 'Person',
#          'id': 'http://orcid.org/0000-0003-0077-4738',
#          'name': 'Matt Jones'},
#         {'type': 'Person',
#          'id': 'http://orcid.org/0000-0002-2192-403X',
#          'name': 'Peter Slaughter'},
#         {'type': 'Organization',
#          'name': 'University of California, Santa Barbara'}
#     ]
#     assert [{'type': 'Person',
#              'id': 'http://orcid.org/0000-0003-0077-4738',
#              'name': 'Matt Jones'},
#             {'type': 'Person',
#              'id': 'http://orcid.org/0000-0002-2192-403X',
#              'name': 'Peter Slaughter'},
#             {'type': 'Organization',
#              'name': 'University of California, Santa Barbara'}] == get_authors(authors)

def test_get_affiliations():
    "get_affiliations"
    assert None == get_affiliations(None)
    assert [{'name': 'University of California, Santa Barbara'}] == get_affiliations(["University of California, Santa Barbara"])
    assert [{'name': 'University of California, Santa Barbara'}] == get_affiliations([{'name': 'University of California, Santa Barbara'}])
    assert [{'name': 'University of California, Santa Barbara', 'affiliationIdentifier': 'https://ror.org/02t274463', 'affiliationIdentifierScheme': 'ROR'}] == get_affiliations([{'name': 'University of California, Santa Barbara', 'affiliationIdentifier': '02t274463', 'affiliationIdentifierScheme': 'ROR', 'schemeURI': 'https://ror.org/'}])
    