# -*- coding: utf-8 -*-

# commonmeta-py

"""
commonmeta-py library
~~~~~~~~~~~~~~~~~~~~~

commonmeta-py is a Python library to convert scholarly metadata
"""

__title__ = "commonmeta-py"
__version__ = "0.172"
__author__ = "Martin Fenner"
__license__ = "MIT"

# ruff: noqa: F401
from .author_utils import (
    authors_as_string,
    cleanup_author,
    get_affiliations,
    get_authors,
    get_one_author,
    is_personal_name,
)
from .base_utils import (
    compact,
    dig,
    get_crossref_xml_head,
    parse_attributes,
    parse_xml,
    presence,
    sanitize,
    unparse_xml,
    unparse_xml_list,
    unwrap,
    wrap,
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
    datacite_api_url,
    decode_doi,
    doi_as_url,
    doi_from_url,
    doi_resolver,
    encode_doi,
    get_doi_ra,
    is_rogue_scholar_doi,
    normalize_doi,
    validate_doi,
    validate_prefix,
)
from .file_utils import (
    download_file,
    read_file,
    read_gz_file,
    read_zip_file,
    uncompress_content,
    unzip_content,
)
from .metadata import Metadata, MetadataList
from .readers import (
    cff_reader,
    codemeta_reader,
    crossref_reader,
    crossref_xml_reader,
    datacite_reader,
    datacite_xml_reader,
    inveniordm_reader,
    jsonfeed_reader,
    kbase_reader,
    openalex_reader,
    ris_reader,
    schema_org_reader,
)
from .schema_utils import json_schema_errors, xml_schema_errors
from .utils import (
    dict_to_spdx,
    extract_curie,
    extract_url,
    extract_urls,
    from_csl,
    from_jsonfeed,
    from_schema_org,
    get_language,
    issn_as_url,
    name_to_fos,
    normalize_cc_url,
    normalize_id,
    normalize_ids,
    normalize_orcid,
    normalize_ror,
    normalize_url,
    pages_as_string,
    replace_curie,
    string_to_slug,
    to_csl,
    validate_orcid,
    validate_ror,
    validate_url,
)
from .writers import (
    bibtex_writer,
    citation_writer,
    commonmeta_writer,
    crossref_xml_writer,
    csl_writer,
    datacite_writer,
    ris_writer,
    schema_org_writer,
)
from .writers.crossref_xml_writer import (
    MARSHMALLOW_MAP,
    CrossrefBadRequestError,
    CrossrefError,
    CrossrefForbiddenError,
    CrossrefGoneError,
    CrossrefNoContentError,
    CrossrefNotFoundError,
    CrossrefRequestError,
    CrossrefServerError,
    CrossrefUnauthorizedError,
    CrossrefXMLClient,
    CrossrefXMLSchema,
    HttpError,
    convert_crossref_xml,
    write_crossref_xml,
)
