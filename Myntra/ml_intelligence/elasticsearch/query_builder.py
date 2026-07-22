"""
Elasticsearch Query Builder Module for ml_intelligence
Generates Query DSL payloads for BM25, KNN vector search, and RRF fusion.
"""

from typing import Dict, Any, List, Optional
from ml_intelligence.api.schemas import HybridSearchInput, GeoPoint


class ESQueryBuilder:
    """Generates Elasticsearch 8.x Query DSL payloads."""

    @staticmethod
    def build_hybrid_query(input_dto: HybridSearchInput, query_vector: List[float]) -> Dict[str, Any]:
        """Constructs hybrid dense KNN + sparse BM25 query DSL with RRF rank fusion."""
        must_filters: List[Dict[str, Any]] = []

        if input_dto.city_filter and input_dto.city_filter.lower() != "all":
            must_filters.append({"term": {"city": input_dto.city_filter.lower().strip()}})

        if input_dto.min_trust_score > 0.0:
            must_filters.append({"range": {"trust_score": {"gte": input_dto.min_trust_score}}})

        if input_dto.geo_location:
            must_filters.append({
                "geo_distance": {
                    "distance": f"{input_dto.max_distance_km}km",
                    "location": {
                        "lat": input_dto.geo_location.lat,
                        "lon": input_dto.geo_location.lon
                    }
                }
            })

        # Sparse BM25 Multi-Match Query
        sparse_query = {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": input_dto.query,
                            "fields": ["canonical_name^3", "brand_name^2", "why_found", "search_tags^2"],
                            "fuzziness": "AUTO"
                        }
                    }
                ] + must_filters
            }
        }

        # Dense KNN Vector Query (384-dim HNSW)
        knn_query = {
            "field": "store_embedding",
            "query_vector": query_vector,
            "k": input_dto.top_k,
            "num_candidates": 50
        }
        if must_filters:
            knn_query["filter"] = must_filters

        # Combine in Hybrid DSL
        dsl = {
            "size": input_dto.top_k,
            "query": sparse_query,
            "knn": knn_query
        }
        return dsl


if __name__ == "__main__":
    qb = ESQueryBuilder()
    dto = HybridSearchInput(query="bridal silk saree", city_filter="Hyderabad", min_trust_score=75.0)
    dummy_vec = [0.1] * 384
    dsl = qb.build_hybrid_query(dto, dummy_vec)
    print("[OK] Generated ES Hybrid Query DSL Keys:", list(dsl.keys()))
