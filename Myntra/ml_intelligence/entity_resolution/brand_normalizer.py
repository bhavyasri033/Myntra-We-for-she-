"""
Brand Normalizer Module for ml_intelligence
Normalizes merchant brand titles, splits branch/locality names, and cleans punctuation.
"""

import re
from typing import Tuple
from rapidfuzz import fuzz


class BrandNormalizer:
    """Provides utility methods for brand title normalization and branch splitting."""

    @staticmethod
    def split_brand_and_branch(raw_name: str) -> Tuple[str, str]:
        """Separates brand title from branch/locality in parentheses or hyphens."""
        raw_name = raw_name.strip()
        
        match_paren = re.search(r'^(.*?)\s*\((.*?)\)$', raw_name)
        if match_paren:
            brand = match_paren.group(1).strip()
            branch = match_paren.group(2).strip()
            return brand, branch

        if " - " in raw_name:
            parts = raw_name.split(" - ", 1)
            return parts[0].strip(), parts[1].strip()

        return raw_name, "General"

    @staticmethod
    def normalize_brand_spelling(brand_name: str) -> str:
        """Removes duplicate spaces or trailing whitespace."""
        return re.sub(r"\s+", " ", brand_name).strip()

    @staticmethod
    def are_brands_similar(name1: str, name2: str, threshold: float = 0.85) -> bool:
        """Computes RapidFuzz ratio to check if two brand names represent the same merchant."""
        ratio = fuzz.ratio(name1.lower(), name2.lower()) / 100.0
        return ratio >= threshold
