import re, requests

def validate_prefix(doi):
    m = re.search(r"\A(?:(http|https):/(/)?(dx\.)?(doi\.org|handle\.stage\.datacite\.org|handle\.test\.datacite\.org)/)?(doi:)?(10\.\d{4,5}).*\Z", doi)
    if m is None:
        return None
    return m.group(6)

def doi_as_url(doi):
    if doi is None:
        return None
    else:
        return "https://doi.org/" + doi.lower()

# get DOI registration agency
def get_doi_ra(doi):
    prefix = validate_prefix(doi)
    if prefix == None:
        return None
    response = requests.get("https://doi.org/ra/" + prefix)
    if response.status_code != 200:
        return None
    else:
        return response.json()[0].get('RA', None)

            

   