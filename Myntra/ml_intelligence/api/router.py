"""
FastAPI Service Router Module for ml_intelligence
Exposes ONLY business-facing REST API endpoints for Developer 2 FastAPI Gateway integration and Developer 3 consumption.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from ml_intelligence.api.schemas import (
    HybridSearchInput, HybridSearchOutput,
    PersonalizedRecommendationInput, PersonalizedRecommendationOutput,
    StoreProfileOutput, StoreReasonOutput,
    IndexDatasetInput, IndexDatasetOutput
)
from ml_intelligence.api.dependencies import MLServiceContainer, get_service_container
from ml_intelligence.utils.logger import get_logger

logger = get_logger("ml_intelligence.api")

ml_router = APIRouter(prefix="/api/v1/ml", tags=["ML Intelligence Service"])


# ============================================================================
# PUBLIC BUSINESS-FACING ENDPOINTS
# ============================================================================

@ml_router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Health check endpoint for service monitoring."""
    return {"status": "HEALTHY", "service": "ml-intelligence", "version": "1.0.0"}


@ml_router.post("/index", response_model=IndexDatasetOutput)
def index_dataset(
    input_dto: Optional[IndexDatasetInput] = None, 
    container: MLServiceContainer = Depends(get_service_container)
):
    """Indexes enriched regional retailer dataset."""
    try:
        raw_path = input_dto.raw_source_path if input_dto else None
        count = container.index_seed_dataset(raw_path=raw_path)
        
        index_map = container.indexer.in_memory_index
        regions = sorted(list(set(str(s.get("city", "")).title() for s in index_map.values() if s.get("city"))))
        sample_ids = list(index_map.keys())[:5]

        return IndexDatasetOutput(
            schema_version="1.0.0",
            indexed_count=count,
            regions_indexed=regions,
            sample_store_ids=sample_ids,
            message=f"Successfully indexed {count} enriched store records across {len(regions)} regions."
        )
    except Exception as e:
        logger.error(f"Index dataset error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@ml_router.post("/search", response_model=HybridSearchOutput)
def search_retailers(
    input_dto: HybridSearchInput, 
    container: MLServiceContainer = Depends(get_service_container)
):
    """Semantic regional retailer search using dense vector + sparse BM25 search with RRF rank fusion."""
    try:
        if len(container.indexer.in_memory_index) == 0:
            raise HTTPException(status_code=400, detail="Search index is empty. Execute POST /api/v1/ml/index first.")
        return container.retriever.search(input_dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@ml_router.post("/recommend", response_model=PersonalizedRecommendationOutput)
def recommend_regional_stores(
    input_dto: PersonalizedRecommendationInput, 
    container: MLServiceContainer = Depends(get_service_container)
):
    """Returns personalized regional store recommendations powered by 6 fashion signals and human-readable explanations."""
    try:
        index_data = container.indexer.in_memory_index
        if not index_data:
            raise HTTPException(status_code=400, detail="Search index is empty. Execute POST /api/v1/ml/index first.")
            
        return container.match_engine.recommend_personalized(input_dto, index_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@ml_router.get("/store/{store_id}", response_model=StoreProfileOutput)
def get_store_profile(
    store_id: str, 
    container: MLServiceContainer = Depends(get_service_container)
):
    """Returns Store Profile DTO for frontend rendering."""
    try:
        store = container.indexer.in_memory_index.get(store_id)
        if not store:
            raise HTTPException(status_code=404, detail=f"Store with ID '{store_id}' not found in index.")

        evidence_list = store.get("supporting_evidence", [
            f"Verified aggregate trust rating of {store.get('trust_score', 85.0)}/100.",
            f"Established merchant brand equity in {store.get('city', 'India')}."
        ])

        categories = store.get("categories", [store.get("primary_category", "Family Shopping")])
        rec_score = float(store.get("recommendation_score", store.get("trust_score", 85.0)))

        return StoreProfileOutput(
            schema_version="1.0.0",
            store_id=store_id,
            store_name=str(store.get("canonical_name", "")),
            city=str(store.get("city", "")).title(),
            region=str(store.get("zone", store.get("state", "Pan-India"))),
            primary_categories=categories,
            specializations=store.get("specializations", []),
            trust_badge=str(store.get("trust_badge", "Tier-1 Trusted Anchor")),
            trust_score=float(store.get("trust_score", 85.0)),
            evidence_summary=evidence_list,
            recommendation_score=rec_score,
            short_business_summary=str(store.get("why_found", ""))
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get store profile error for '{store_id}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


@ml_router.get("/store/{store_id}/reason", response_model=StoreReasonOutput)
def get_recommendation_explanation(
    store_id: str, 
    container: MLServiceContainer = Depends(get_service_container)
):
    """Returns Recommendation Explanation detailing why this retailer was recommended and its signal contributions."""
    try:
        store = container.indexer.in_memory_index.get(store_id)
        if not store:
            raise HTTPException(status_code=404, detail=f"Store with ID '{store_id}' not found in index.")

        return container.match_engine.get_recommendation_explanation(store_id, store)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get recommendation explanation error for '{store_id}': {e}")
        raise HTTPException(status_code=500, detail=str(e))
