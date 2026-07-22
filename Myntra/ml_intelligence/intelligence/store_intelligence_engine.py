"""
Store Intelligence Engine Module for ml_intelligence
Classifies stores into categories, specializations, and search tags.
"""

import re
from typing import List
from ml_intelligence.api.schemas import (
    StoreCanonicalRecord, 
    StoreIntelligenceInput, 
    StoreIntelligenceOutput
)
from ml_intelligence.intelligence.taxonomy_manager import TaxonomyManager
from ml_intelligence.utils.logger import get_logger

logger = get_logger("ml_intelligence.intelligence")


class StoreIntelligenceEngine:
    """Classifies canonical stores into taxonomy categories and extracts search tags."""

    def __init__(self):
        self.taxonomy_mgr = TaxonomyManager()

    def process(self, intel_input: StoreIntelligenceInput) -> StoreIntelligenceOutput:
        """Classifies canonical store record and returns StoreIntelligenceOutput DTO."""
        store = intel_input.canonical_store
        text = f"{store.brand_name} {store.why_found}".lower()

        primary_category = self._classify_primary_category(text)
        specializations = self._extract_specializations(text)
        search_tags = self._generate_search_tags(primary_category, specializations, store.city)

        return StoreIntelligenceOutput(
            store_id=store.store_id,
            primary_category=primary_category,
            specializations=specializations,
            search_tags=search_tags,
            classification_confidence=0.92
        )

    def _classify_primary_category(self, text: str) -> str:
        """Determines primary fashion category based on text keyword evidence."""
        if any(kw in text for kw in ["family shopping", "family destination", "budget-friendly", "shopping mall"]):
            return "Family Shopping"
        elif any(kw in text for kw in ["bridal", "wedding", "lehenga", "silk saree"]):
            return "Bridal Silk"
        elif any(kw in text for kw in ["handloom", "weaver", "chanderi", "maheshwari", "pattu"]):
            return "Handloom Heritage"
        elif any(kw in text for kw in ["designer", "boutique", "haute"]):
            return "Designer & Boutique"
        elif any(kw in text for kw in ["ethnic", "festive", "kurta", "sherwani"]):
            return "Ethnic & Festive"
        else:
            return "Casual & Everyday"

    def _extract_specializations(self, text: str) -> List[str]:
        """Extracts micro-specializations matching taxonomy whitelist."""
        whitelist = self.taxonomy_mgr.get_specializations()
        extracted = []
        for spec in whitelist:
            if re.search(r'\b' + re.escape(spec.lower()) + r'\b', text):
                extracted.append(spec)
        return extracted if extracted else ["Sarees"]

    def _generate_search_tags(self, category: str, specs: List[str], city: str) -> List[str]:
        """Generates search hashtags for Elasticsearch indexing."""
        tags = [f"#{category.replace(' ', '')}", f"#{city}Fashion"]
        for spec in specs[:3]:
            tags.append(f"#{spec.replace(' ', '')}")
        return tags
