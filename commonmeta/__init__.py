# -*- coding: utf-8 -*-

# commonmeta-py

"""
commonmeta-py library
~~~~~~~~~~~~~~~~~~~~~

commonmeta-py is a Python library to convert scholarly metadata
"""

__title__ = "commonmeta-py"
__version__ = "0.54"
__author__ = "Martin Fenner"
__license__ = "MIT"

# ruff: noqa: F401
from .metadata import Metadata, MetadataList
from .readers import (
    cff_reader,
    codemeta_reader,
    crossref_reader,
    crossref_xml_reader,
    datacite_reader,
    datacite_xml_reader,
    inveniordm_reader,
    json_feed_reader,
    kbase_reader,
    ris_reader,
    schema_org_reader,
)
from .writers import (
    bibtex_writer,
    citation_writer,
    commonmeta_writer,
    csl_writer,
    datacite_writer,
    ris_writer,
    schema_org_writer,
)
from .utils import (
    dict_to_spdx,
    from_csl,
    from_schema_org,
    get_language,
    normalize_cc_url,
    normalize_id,
    normalize_ids,
    normalize_orcid,
    normalize_url,
    normalize_ror,
    pages_as_string,
    to_csl,
    validate_orcid,
    validate_url,
    get_language,
    encode_doi,
    name_to_fos,
    from_json_feed,
)
from .author_utils import (
    authors_as_string,
    cleanup_author,
    get_affiliations,
    get_authors,
    get_one_author,
    is_personal_name,
)
from .base_utils import (
    wrap,
    unwrap,
    compact,
    presence,
    parse_attributes,
    sanitize,
)
from .date_utils import (
    get_date_from_crossref_parts,
    get_date_from_date_parts,
    get_date_from_unix_timestamp,
    get_date_parts,
    get_iso8601_date,
    strip_milliseconds,
)
from .doi_utils import (
    crossref_api_url,
    crossref_xml_api_url,
    doi_from_url,
    doi_as_url,
    doi_resolver,
    datacite_api_url,
    get_doi_ra,
    normalize_doi,
    validate_doi,
    validate_prefix,
)
