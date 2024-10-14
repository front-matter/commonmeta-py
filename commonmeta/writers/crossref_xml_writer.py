"""Crossref XML writer for commonmeta-py"""
from typing import Optional
from ..constants import Commonmeta
from ..crossref_utils import generate_crossref_xml, generate_crossref_xml_list


def write_crossref_xml(metadata: Commonmeta) -> Optional[str]:
    """Write Crossref XML"""
    return generate_crossref_xml(metadata)


def write_crossref_xml_list(metalist):
    """Write crossref_xml list"""
    if metalist is None:
        return None

    return generate_crossref_xml_list(metalist)
