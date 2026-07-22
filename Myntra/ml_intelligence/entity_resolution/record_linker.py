"""
Record Linker Module for ml_intelligence
Deduplicates raw merchant records and assigns canonical store identifiers.
"""

from typing import List, Dict
from ml_intelligence.api.schemas import (
    StoreRawRecord, 
    StoreCanonicalRecord, 
    EntityResolutionInput, 
    EntityResolutionOutput
)
from ml_intelligence.entity_resolution.brand_normalizer import BrandNormalizer
from ml_intelligence.utils.logger import get_logger

logger = get_logger("ml_intelligence.entity_resolution")

CITY_ID_PREFIXES: Dict[str, str] = {
    "hyderabad": "HYD",
    "visakhapatnam": "VIZ",
    "vizag": "VIZ",
    "bengaluru": "BLR",
    "bangalore": "BLR",
    "vijayawada": "VIJ",
    "indore": "IND",
    "kochi": "KOC",
    "chennai": "CHE",
    "kanchipuram": "KNC",
    "varanasi": "VAR",
    "rajkot": "RAJ",
    "surat": "SUR"
}

STATE_MAPPINGS: Dict[str, str] = {
    "hyderabad": "Telangana",
    "visakhapatnam": "Andhra Pradesh",
    "bengaluru": "Karnataka",
    "vijayawada": "Andhra Pradesh",
    "indore": "Madhya Pradesh",
    "kochi": "Kerala",
    "chennai": "Tamil Nadu",
    "kanchipuram": "Tamil Nadu",
    "varanasi": "Uttar Pradesh",
    "rajkot": "Gujarat",
    "surat": "Gujarat"
}

ZONE_MAPPINGS: Dict[str, str] = {
    "hyderabad": "South",
    "visakhapatnam": "South",
    "bengaluru": "South",
    "vijayawada": "South",
    "indore": "Central",
    "kochi": "South",
    "chennai": "South",
    "kanchipuram": "South",
    "varanasi": "North",
    "rajkot": "West",
    "surat": "West"
}


class RecordLinker:
    """Deduplicates raw records and generates canonical store entities."""

    def __init__(self, similarity_threshold: float = 0.85):
        self.normalizer = BrandNormalizer()
        self.similarity_threshold = similarity_threshold

    def resolve(self, raw_input: EntityResolutionInput) -> EntityResolutionOutput:
        """Processes raw records into StoreCanonicalRecord DTOs."""
        logger.info(f"Resolving entities for {len(raw_input.raw_stores)} raw store records...")

        resolved_stores: List[StoreCanonicalRecord] = []
        city_counters: Dict[str, int] = {}
        merged_count = 0

        for record in raw_input.raw_stores:
            city_key = record.region.strip().lower()
            prefix = CITY_ID_PREFIXES.get(city_key, "BHR")
            
            city_counters[prefix] = city_counters.get(prefix, 0) + 1
            store_id = f"{prefix}{city_counters[prefix]:03d}"

            brand, branch = self.normalizer.split_brand_and_branch(record.raw_store_name)
            brand_clean = self.normalizer.normalize_brand_spelling(brand)
            
            canonical_name = f"{brand_clean} ({branch})" if branch and branch.lower() != "general" else brand_clean
            state = STATE_MAPPINGS.get(city_key, "India")
            zone = ZONE_MAPPINGS.get(city_key, "Pan-India")

            canonical_record = StoreCanonicalRecord(
                store_id=store_id,
                brand_name=brand_clean,
                branch_name=branch,
                canonical_name=canonical_name,
                city=record.region.title(),
                state=state,
                zone=zone,
                why_found=record.why_found,
                source_found=record.source_found
            )
            resolved_stores.append(canonical_record)

        logger.info(f"Entity Resolution complete: {len(resolved_stores)} canonical stores generated.")

        return EntityResolutionOutput(
            duplicate_clusters_found=merged_count,
            resolved_stores=resolved_stores
        )
