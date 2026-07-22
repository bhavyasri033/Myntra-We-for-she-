"""
API Dependencies and Container Injection Module for ml_intelligence
Instantiates engine singletons for FastAPI dependency injection.
"""

import os
from typing import Dict, Any, List
from ml_intelligence.discovery.dataset_loader import DatasetLoader
from ml_intelligence.entity_resolution.record_linker import RecordLinker
from ml_intelligence.intelligence.store_intelligence_engine import StoreIntelligenceEngine
from ml_intelligence.evidence.aspect_extractor import AspectExtractor
from ml_intelligence.trust.trust_matrix import TrustMatrixCalculator
from ml_intelligence.elasticsearch.indexer import ESBulkIndexer
from ml_intelligence.elasticsearch.hybrid_retriever import ESHybridRetriever
from ml_intelligence.recommendation.match_engine import RecommendationMatchEngine
from ml_intelligence.dossier.dossier_generator import DossierGenerator
from ml_intelligence.api.schemas import EntityResolutionInput, StoreIntelligenceInput, EvidenceExtractionInput, TrustEvaluationInput
from ml_intelligence.utils.logger import get_logger

logger = get_logger("ml_intelligence.dependencies")


class MLServiceContainer:
    """Container holding singletons for backend ML engine services."""

    def __init__(self):
        self.loader = DatasetLoader()
        self.linker = RecordLinker()
        self.intelligence_engine = StoreIntelligenceEngine()
        self.aspect_extractor = AspectExtractor()
        self.trust_calculator = TrustMatrixCalculator()
        self.indexer = ESBulkIndexer()
        self.retriever = ESHybridRetriever(indexer=self.indexer)
        self.match_engine = RecommendationMatchEngine()
        self.dossier_generator = DossierGenerator()

    def index_seed_dataset(self, raw_path: str = None) -> int:
        """Loads and indexes the seed dataset into the search engine when triggered."""
        target_file = raw_path or "Master Candidate Dataset v1.xlsx"
        if not os.path.exists(target_file):
            # Fallback to root path if nested
            target_file = os.path.join(os.path.dirname(__file__), "..", "..", target_file)
            if not os.path.exists(target_file):
                logger.error(f"Seed dataset file not found at '{raw_path or 'Master Candidate Dataset v1.xlsx'}'.")
                raise FileNotFoundError(f"Seed dataset file not found.")

        logger.info(f"Indexing ML Intelligence dataset from '{target_file}'...")
        try:
            self.loader.raw_source_path = target_file
            discovery_out = self.loader.load()

            er_out = self.linker.resolve(EntityResolutionInput(raw_stores=discovery_out.raw_stores))
            
            payloads: List[Dict[str, Any]] = []

            for canon in er_out.resolved_stores:
                intel_out = self.intelligence_engine.process(StoreIntelligenceInput(canonical_store=canon))
                ev_out = self.aspect_extractor.extract(EvidenceExtractionInput(store_id=canon.store_id, why_found=canon.why_found))
                trust_out = self.trust_calculator.evaluate(TrustEvaluationInput(
                    store_id=canon.store_id,
                    source_found=canon.source_found,
                    aspects=ev_out.aspects,
                    why_found=canon.why_found
                ))

                store_payload = {
                    "store_id": canon.store_id,
                    "brand_name": canon.brand_name,
                    "branch_name": canon.branch_name,
                    "canonical_name": canon.canonical_name,
                    "city": canon.city,
                    "state": canon.state,
                    "zone": canon.zone,
                    "primary_category": intel_out.primary_category,
                    "specializations": intel_out.specializations,
                    "search_tags": intel_out.search_tags,
                    "trust_score": trust_out.aggregate_trust_score,
                    "trust_badge": trust_out.trust_badge,
                    "dimension_scores": trust_out.dimension_scores.model_dump(),
                    "supporting_evidence": trust_out.supporting_evidence,
                    "risk_flags": trust_out.risk_flags,
                    "why_found": canon.why_found,
                    "source_found": canon.source_found,
                    "categories": [intel_out.primary_category] + intel_out.specializations
                }
                payloads.append(store_payload)

            count, _ = self.indexer.index_store_payloads(payloads)
            logger.info(f"Indexing complete! Indexed {count} enriched store records.")
            return count

        except Exception as e:
            logger.error(f"Indexing error: {e}")
            raise


_container_instance = None


def get_service_container() -> MLServiceContainer:
    """Returns singleton instance of MLServiceContainer."""
    global _container_instance
    if _container_instance is None:
        _container_instance = MLServiceContainer()
    return _container_instance
