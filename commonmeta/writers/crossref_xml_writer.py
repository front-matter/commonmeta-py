"""Crossref XML writer for commonmeta-py"""
from typing import Optional
from ..constants import Commonmeta
from ..crossref_utils import generate_crossref_xml

def write_crossref_xml(metadata: Commonmeta) -> Optional[str]:
    """Write Crossref XML"""
    return generate_crossref_xml(metadata)
