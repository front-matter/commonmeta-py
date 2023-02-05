from .utils import parse_attributes, wrap, unwrap, compact, normalize_orcid, normalize_id
import re

def get_one_author(author):
    """parse one author string into CSL format"""
    # if author is a string
    if type(author) == str:
        author = { 'creatorName': author } 

    # malformed XML
    if type(author.get('creatorName', None)) == list:
        return None 

    name = (parse_attributes(author.get('creatorName', None)) or
        parse_attributes(author.get('contributorName', None)) or
        parse_attributes(author.get('name', None)))
    given_name = (parse_attributes(author.get('givenName', None)) or
        parse_attributes(author.get('given', None)))
    family_name = (parse_attributes(author.get('familyName', None)) or
        parse_attributes(author.get('family', None)))

    name = cleanup_author(name)
    if family_name and given_name:
        name = f"{given_name} {family_name}"
    contributor_type = parse_attributes(author.get('contributorType', None))
    name_type = (parse_attributes(author.get('creatorName', None), content='nameType', first=True) or 
        parse_attributes(author.get('contributorName', None), content='nameType', first=True))

    name_identifiers = []
    for name_identifier in wrap(author.get('nameIdentifiers', [])):
        if name_identifier.get('nameIdentifier', None) is None:
            continue
        if name_identifier.get('nameIdentifierScheme', None) == 'ORCID':
            ni = compact({
                'nameIdentifier': normalize_orcid(name_identifier.get('nameIdentifier', None)),
                'schemeUri': 'https://orcid.org',
                'nameIdentifierScheme': 'ORCID'
            })
            name_identifiers.append(ni)
        elif name_identifier.get('schemeURI', None) is not None:
            ni = compact({
                'nameIdentifier': name_identifier.get('schemeURI') + name_identifier.get('nameIdentifier', None),
                'schemeUri': name_identifier.get('schemeURI'),
                'nameIdentifierScheme': name_identifier.get('nameIdentifierScheme', None)
            })
            name_identifiers.append(ni)
        else:
            ni = compact({
                'nameIdentifier': name_identifier.get('nameIdentifier', None),
                'nameIdentifierScheme': name_identifier.get('nameIdentifierScheme', None)
            })
            name_identifiers.append(ni)
    if len(name_identifiers) == 0:
        name_identifiers = None

    # Crossref metadata
    if name_identifiers is [] and author.get('ORCID', None):
        name_identifiers = [{
            'nameIdentifier': normalize_orcid(author.get('ORCID', None)),
            'schemeUri': 'https://orcid.org',
            'nameIdentifierScheme': 'ORCID' }]

    if family_name or given_name:
        name_type = 'Personal'
    elif name_type is None and any(ni for ni in wrap(name_identifiers) if ni.get('nameIdentifierScheme', None) == "ORCID"):
        name_type = 'Personal'
    elif name_type is None and any(ni for ni in wrap(name_identifiers) if ni.get('nameIdentifierScheme', None) in ("ISNI", "GRID", "ROR")):
        name_type = 'Organizational'
    author = compact({ 
        'nameType': name_type,
        'name': name,
        'givenName': given_name,
        'familyName': family_name,
        'nameIdentifiers': name_identifiers,
        'affiliation': get_affiliations(author.get('affiliation', None)),
        'contributorType': contributor_type })

    if family_name:
        return author

    if name_type == 'Personal':
        return compact({ 
            'nameType': 'Personal',
            'name': name,
            'givenName': given_name,
            'familyName': family_name,
            'nameIdentifiers': name_identifiers,
            'affiliation': get_affiliations(author.get('affiliation', None)),
            'contributorType': contributor_type })
    else:
        return compact({ 
            'nameType': name_type,
            'name': name,
            'nameIdentifiers': name_identifiers,
            'affiliation': get_affiliations(author.get('affiliation', None)),
            'contributorType': contributor_type })
  
def cleanup_author(author):
    if author is None:
        return None

    # detect pattern "Smith J.", but not "Smith, John K."
    if not ',' in author:
        author = re.sub(r'/([A-Z]\.)?(-?[A-Z]\.)$/', ', \1\2', author)

    # remove spaces around hyphens
    author = author.replace(' - ', '-')

    # remove non-standard space characters
    author = re.sub('/[ \t\r\n\v\f]/', ' ', author)
    return author

def get_authors(authors):
    """parse array of author strings into CSL format"""
    return list(map(lambda author: get_one_author(author), authors))

def authors_as_string(authors):
    """convert CSL authors list to string, e.g. for bibtex"""
    if authors is None:
        return None
    formatted_authors = []
    for author in wrap(authors):
        if author.get('familyName', None):
            a = f"{author['familyName']}, {author['givenName']}"
            formatted_authors.append(a)
        elif author.get('type', None) != 'Person':
            a = author['name']
            formatted_authors.append(a)   
    return ' and '.join(formatted_authors)

def get_affiliations(affiliations):
    """parse array of affiliation strings into CSL format"""
    if affiliations is None:
        return None

    formatted_affiliations = []
    for affiliation in wrap(affiliations):
        affiliation_identifier = None
        if type(affiliation) is str:
            name = affiliation
            affiliation_identifier_scheme = None
            scheme_uri = None
        else:
            if affiliation.get('affiliationIdentifier', None) is not None:
                affiliation_identifier = affiliation['affiliationIdentifier']
                if affiliation.get('schemeURI', None) is not None:
                    schemeURI = affiliation['schemeURI'] if affiliation['schemeURI'].endswith('/') else "{affiliation['schemeURI']}/"
                affiliation_identifier = normalize_id(schemeURI + affiliation_identifier) if (not affiliation_identifier.startswith('https://') and schemeURI is not None) else normalize_id(affiliation_identifier)
            name = affiliation.get('name', None) or affiliation.get('__content__', None)
            affiliation_identifier_scheme = affiliation.get('affiliationIdentifierScheme', None)
            scheme_uri = affiliation.get('SchemeURI', None)

        if name is None:
            continue

        formatted_affiliations.append({
             'name': name,
             'affiliationIdentifier': affiliation_identifier,
             'affiliationIdentifierScheme': affiliation_identifier_scheme,
             'schemeUri': scheme_uri })

    return compact(formatted_affiliations)
 
