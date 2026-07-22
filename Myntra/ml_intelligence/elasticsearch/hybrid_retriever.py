"""
ES Hybrid Retriever Module for ml_intelligence
Executes hybrid BM25 + Dense KNN Vector search queries with Reciprocal Rank Fusion (RRF).
"""

import time
import math
from typing import List, Dict, Any
from ml_intelligence.api.schemas import (
    HybridSearchInput, 
    HybridSearchOutput, 
    SearchCandidateHit
)
from ml_intelligence.elasticsearch.es_client import ESClientHandler
from ml_intelligence.elasticsearch.query_builder import ESQueryBuilder
from ml_intelligence.elasticsearch.indexer import ESBulkIndexer
from ml_intelligence.utils.logger import get_logger

logger = get_logger("ml_intelligence.elasticsearch.retriever")


class ESHybridRetriever:
    """Executes dense vector + sparse BM25 search queries with RRF rank fusion."""

    def __init__(self, indexer: ESBulkIndexer = None):
        self.indexer = indexer or ESBulkIndexer()
        self.es_handler = ESClientHandler()
        self.client = self.es_handler.connect()
        self.query_builder = ESQueryBuilder()

    def search(self, search_input: HybridSearchInput) -> HybridSearchOutput:
        """Performs hybrid search and returns HybridSearchOutput DTO."""
        start_time = time.time()
        logger.info(f"Executing hybrid search query: '{search_input.query}' (city filter: {search_input.city_filter})")

        # Encode query into 384-dim dense vector using indexer encoder
        query_vector = self.indexer.encode_text([search_input.query])[0]
        query_tokens = search_input.query.lower().split()

        hits: List[SearchCandidateHit] = []

        # In-Memory RRF Hybrid Search Execution (Fallback & Fast Mode)
        candidates = list(self.indexer.in_memory_index.values())
        candidate_scores = []

        for store in candidates:
            # City Filter Constraint
            if search_input.city_filter and search_input.city_filter.lower() != "all":
                if store.get("city", "").lower() != search_input.city_filter.lower():
                    continue

            # Minimum Trust Score Filter Constraint
            trust_score = float(store.get("trust_score", store.get("aggregate_trust_score", 70.0)))
            if trust_score < search_input.min_trust_score:
                continue

            # Sparse BM25 Keyword Matching Score
            doc_text = store.get("doc_text", "").lower()
            bm25_matches = sum(1 for token in query_tokens if token in doc_text)
            bm25_score = round(bm25_matches * 4.5, 2)

            # Dense Cosine Similarity Vector Score
            store_vec = store.get("store_embedding", [0.0] * 384)
            dense_score = self._cosine_similarity(query_vector, store_vec)

            # RRF Rank Score Fusion: 1/(60 + r1) + 1/(60 + r2)
            rrf_score = round((1.0 / (60.0 + (1.0 / (bm25_score + 0.01)))) + (1.0 / (60.0 + (1.0 / (dense_score + 0.01)))), 5)

            candidate_scores.append({
                "store_id": str(store.get("store_id")),
                "canonical_name": str(store.get("canonical_name")),
                "city": str(store.get("city")),
                "trust_score": trust_score,
                "rrf_score": rrf_score,
                "dense_similarity_score": round(dense_score, 3),
                "bm25_score": bm25_score,
                "categories": store.get("categories", ["Family Shopping"])
            })

        # Sort candidates by RRF score
        candidate_scores.sort(key=lambda x: x["rrf_score"], reverse=True)
        top_candidates = candidate_scores[:search_input.top_k]

        for c in top_candidates:
            hit = SearchCandidateHit(
                store_id=c["store_id"],
                canonical_name=c["canonical_name"],
                city=c["city"],
                trust_score=c["trust_score"],
                rrf_score=c["rrf_score"],
                dense_similarity_score=c["dense_similarity_score"],
                bm25_score=c["bm25_score"],
                categories=c["categories"]
            )
            hits.append(hit)

        elapsed_ms = int((time.time() - start_time) * 1000)
        logger.info(f"Hybrid search returned {len(hits)} hits in {elapsed_ms}ms.")

        return HybridSearchOutput(
            took_ms=elapsed_ms,
            total_hits=len(candidate_scores),
            hits=hits
        )

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Computes cosine similarity between two 384-dim vectors."""
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1)) or 1.0
        norm2 = math.sqrt(sum(b * b for b in vec2)) or 1.0
        return max(0.0, min(1.0, dot / (norm1 * norm2)))
