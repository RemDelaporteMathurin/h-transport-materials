"""DOI helpers, with no dependencies (used at runtime and by the tooling)."""

import re


def strip_doi(doi: str) -> str:
    """Strips URL and 'doi:' prefixes, keeping the publisher's case"""
    doi = doi.strip()
    doi = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", doi, flags=re.I)
    return re.sub(r"^doi:\s*", "", doi, flags=re.I)


def normalize_doi(doi: str) -> str:
    """For comparisons: DOIs are case-insensitive"""
    return strip_doi(doi).lower()
