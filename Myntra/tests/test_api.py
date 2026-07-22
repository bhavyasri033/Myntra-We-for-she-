"""
Automated Pytest API Test Suite for Myntra Regional Fashion ML Intelligence Service.
Verifies all 6 public business endpoints, DTO contracts, 6-signal recommendation scoring, and explainability.
"""

import sys
from pathlib import Path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_01_health_endpoint():
    """Verifies GET /api/v1/ml/health endpoint."""
    response = client.get("/api/v1/ml/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["service"] == "ml-intelligence"
    assert "version" in data


def test_02_index_endpoint():
    """Verifies POST /api/v1/ml/index endpoint."""
    response = client.post("/api/v1/ml/index")
    assert response.status_code == 200
    data = response.json()
    assert data["indexed_count"] > 0
    assert len(data["regions_indexed"]) > 0
    assert len(data["sample_store_ids"]) > 0
    assert "Successfully indexed" in data["message"]


def test_03_search_endpoint():
    """Verifies POST /api/v1/ml/search endpoint."""
    payload = {
        "query": "Bridal silk sarees family shopping",
        "city_filter": "Hyderabad",
        "min_trust_score": 60.0,
        "top_k": 5
    }
    response = client.post("/api/v1/ml/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_hits"] >= 0
    assert "took_ms" in data
    assert len(data["hits"]) <= 5
    if data["hits"]:
        hit = data["hits"][0]
        assert "store_id" in hit
        assert "canonical_name" in hit
        assert "trust_score" in hit


def test_04_recommend_endpoint():
    """Verifies POST /api/v1/ml/recommend personalized endpoint with 6-signal scoring & explainability."""
    payload = {
        "user_location": "Hyderabad",
        "preferred_categories": ["Bridal Silk", "Ethnic & Festive"],
        "shopping_intent": "wedding shopping for bridal silk sarees",
        "user_preferences": {"price_segment": "Mid-Premium"},
        "top_k": 5
    }
    response = client.post("/api/v1/ml/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user_location"] == "Hyderabad"
    assert data["total_recommendations"] > 0
    assert len(data["recommendations"]) <= 5

    top_rec = data["recommendations"][0]
    assert "store_id" in top_rec
    assert "canonical_name" in top_rec
    assert "recommendation_score" in top_rec
    assert 0.0 <= top_rec["recommendation_score"] <= 100.0
    assert "explanation_reasons" in top_rec
    assert len(top_rec["explanation_reasons"]) > 0


def test_05_store_profile_endpoint():
    """Verifies GET /api/v1/ml/store/{store_id} endpoint for frontend rendering."""
    # First index to ensure data present
    idx_data = client.post("/api/v1/ml/index").json()
    sample_id = idx_data["sample_store_ids"][0]

    response = client.get(f"/api/v1/ml/store/{sample_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["store_id"] == sample_id
    assert "store_name" in data
    assert "city" in data
    assert "region" in data
    assert "primary_categories" in data
    assert "specializations" in data
    assert "trust_badge" in data
    assert "trust_score" in data
    assert "evidence_summary" in data
    assert "recommendation_score" in data
    assert "short_business_summary" in data


def test_06_recommendation_explanation_endpoint():
    """Verifies GET /api/v1/ml/store/{store_id}/reason (Recommendation Explanation) endpoint."""
    idx_data = client.post("/api/v1/ml/index").json()
    sample_id = idx_data["sample_store_ids"][0]

    response = client.get(f"/api/v1/ml/store/{sample_id}/reason")
    assert response.status_code == 200
    data = response.json()
    assert data["store_id"] == sample_id
    assert "store_name" in data
    assert "city" in data
    assert "recommendation_score" in data
    assert "explanation_summary" in data
    assert "contributing_signals" in data
    assert "explanation_reasons" in data
    assert len(data["explanation_reasons"]) > 0


def test_07_invalid_store_id_handling():
    """Verifies 404 error handling for non-existent store ID."""
    response = client.get("/api/v1/ml/store/INVALID_ID_999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


if __name__ == "__main__":
    pytest.main(["-v", __file__])
