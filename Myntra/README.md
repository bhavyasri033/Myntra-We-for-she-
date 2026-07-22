# 🛍️ Myntra Regional Fashion ML Intelligence Service

> **AI Backend Intelligence Microservice powering Myntra's Regional Fashion Recommendation Feature**

---

## 📌 Problem Statement

Myntra's expansion into Tier-2 and Tier-3 cities in India ("The Bharat Opportunity") requires connecting 50M+ regional shoppers with verified, trusted offline fashion merchants. Traditional e-commerce recommendation systems suffer from cold-start issues when surfacing non-standardized regional supply (e.g. authentic bridal silk weavers in Kanchipuram, handloom clusters in Varanasi, or family shopping anchors in Hyderabad).

The **Myntra Regional Fashion ML Intelligence Service** solves this by providing a backend AI microservice that ingests regional supply data, normalizes merchant entities, evaluates multi-dimensional trust ratings, and delivers **personalized, explainable regional fashion recommendations** based on user location, shopping intent, and category preferences.

---

## 🏛️ System Architecture

The microservice consists of 10 frozen backend modules inside `ml_intelligence/`:

1. **`discovery/`**: Ingests raw regional merchant candidate datasets (`Master Candidate Dataset v1.xlsx`).
2. **`entity_resolution/`**: Normalizes merchant titles, resolves branches/localities, and deduplicates canonical store entities.
3. **`intelligence/`**: Classifies merchants into regional fashion categories, specializations, and search hashtags.
4. **`evidence/`**: Extracts structured business aspects (legacy, authentic craft, handloom, bridal, price segment) from unstructured narrative text.
5. **`trust/`**: Calculates a 5-dimension Trust Matrix (Reputation, Source Reliability, Specialization, Verifiability, Catalog Capacity) and assigns Trust Badges.
6. **`elasticsearch/`**: Executes 384-dim dense KNN vector search + sparse BM25 text search fused via Reciprocal Rank Fusion (RRF).
7. **`recommendation/`**: Multi-factor candidate scoring combining 6 core signals:
   - **Regional Relevance**: User city & local market popularity.
   - **Category Match**: Preferred fashion categories.
   - **Shopping Intent Fit**: Intent alignment (wedding, festive, daily wear, handloom, budget).
   - **Personalization**: User style & price segment preferences.
   - **Fashion Specialization**: Merchant expertise & craft authority.
   - **Trust Score**: Regional reputation & evidence consistency.
8. **`dossier/`**: Synthesizes structured retailer summaries and briefings.
9. **`api/`**: Pydantic V2 DTOs, dependency injection container, and FastAPI router.
10. **`utils/`**: Lightweight standard logger.

---

## 📁 Repository Directory Structure

```
repository/
├── main.py                             # FastAPI gateway entrypoint
├── setup.py                            # Python package setup script
├── requirements.txt                    # Backend dependencies
├── Master Candidate Dataset v1.xlsx   # 282-store regional seed dataset
├── README.md                           # Microservice documentation
├── ml_intelligence/                    # Backend Intelligence Package
│   ├── api/                            # REST Router, DTO Schemas & Container
│   ├── configs/                        # Taxonomy, aspect rules & ES mappings
│   ├── discovery/                      # Raw dataset loader
│   ├── entity_resolution/              # Brand normalizer & record linker
│   ├── intelligence/                   # Store taxonomy classifier
│   ├── evidence/                       # Unstructured aspect extractor
│   ├── trust/                          # 5-Dimension Trust Matrix & explainability
│   ├── elasticsearch/                  # Hybrid KNN + BM25 search & RRF fusion
│   ├── recommendation/                 # Multi-factor 6-signal recommendation engine
│   ├── dossier/                        # Retailer summary & briefing generator
│   └── utils/                          # Standard logging utility
├── scripts/
│   └── index_seed.py                   # Standalone seed dataset indexer script
└── tests/
    ├── __init__.py
    └── test_api.py                     # Pytest suite for all 6 REST endpoints
```

---

## 🔌 Public REST API Endpoints

The service exposes **ONLY 6 business-facing endpoints** under `/api/v1/ml`:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/ml/health` | Health check endpoint for service monitoring. |
| `POST` | `/api/v1/ml/index` | Triggers indexing of the regional retailer seed dataset. |
| `POST` | `/api/v1/ml/search` | Executes hybrid dense KNN vector + BM25 search with RRF fusion. |
| `POST` | `/api/v1/ml/recommend` | Returns personalized store recommendations with human-readable explanations. |
| `GET` | `/api/v1/ml/store/{store_id}` | Returns enriched Store Profile DTO for frontend rendering. |
| `GET` | `/api/v1/ml/store/{store_id}/reason` | Returns Recommendation Explanation detailing signal contributions. |

---

## 🛠️ Developer Setup & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Index Dataset
Server startup remains lightweight with **zero auto-indexing**. Index the seed dataset by calling:
```bash
python scripts/index_seed.py
```
Or via HTTP API:
```bash
curl -X POST http://localhost:8000/api/v1/ml/index
```

### 3. Launch FastAPI Server
```bash
python main.py
```
Or with Uvicorn:
```bash
uvicorn main:app --reload --port 8000
```
Interactive OpenAPI (Swagger) documentation is available at `http://localhost:8000/docs`.

### 4. Run Pytest Verification Suite
```bash
python -m pytest tests/test_api.py -v
```

---

## 📡 API Calling Examples

### 1. Personalized Regional Recommendation (`POST /api/v1/ml/recommend`)
```bash
curl -X POST "http://localhost:8000/api/v1/ml/recommend" \
     -H "Content-Type: application/json" \
     -d '{
           "user_location": "Hyderabad",
           "preferred_categories": ["Bridal Silk", "Ethnic & Festive"],
           "shopping_intent": "wedding shopping for bridal silk sarees",
           "top_k": 5
         }'
```
**Sample Response**:
```json
{
  "schema_version": "1.0.0",
  "user_location": "Hyderabad",
  "total_recommendations": 5,
  "recommendations": [
    {
      "store_id": "HYD001",
      "canonical_name": "South India Shopping Mall",
      "city": "Hyderabad",
      "state": "Telangana",
      "primary_category": "Bridal Silk",
      "trust_score": 93.8,
      "trust_badge": "Tier-1 Trusted Anchor",
      "recommendation_score": 91.5,
      "explanation_reasons": [
        "Trusted regional retailer in Hyderabad (Tier-1 Trusted Anchor).",
        "Strong specialization in Bridal Silk Sarees, Pattu Sarees.",
        "Matches your 'wedding shopping for bridal silk sarees' shopping intent.",
        "Matches your preferred fashion categories (Bridal Silk, Ethnic & Festive)."
      ]
    }
  ]
}
```

### 2. Semantic Retailer Search (`POST /api/v1/ml/search`)
```bash
curl -X POST "http://localhost:8000/api/v1/ml/search" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "Bridal silk sarees family shopping",
           "city_filter": "Hyderabad",
           "min_trust_score": 60.0,
           "top_k": 5
         }'
```

---

## 🔗 Developer Integration Guides

### Integration with Developer 2 (FastAPI Gateway)
Developer 2 mounts the ML Intelligence router into the main backend gateway application with a single line:

```python
from fastapi import FastAPI
from ml_intelligence.api.router import ml_router

app = FastAPI(title="Myntra Main Gateway")

# Mount ML Intelligence Router
app.include_router(ml_router)
```

### Integration with Developer 3 (Frontend Team)
Developer 3 consumes only the REST endpoints:
- `POST /api/v1/ml/recommend` (Home feed / Regional fashion discovery page)
- `POST /api/v1/ml/search` (Search page)
- `GET /api/v1/ml/store/{store_id}` (Store Profile page)
- `GET /api/v1/ml/store/{store_id}/reason` (Recommendation modal / Why Recommended tooltip)

---

## 🔮 Future Improvements

1. **Real-Time Offline Merchant Footfall Stream**: Ingest real-time store footfall and inventory updates.
2. **Multi-Lingual Intent Parsing**: Support regional Indic languages (Telugu, Tamil, Hindi, Gujarati) for intent classification.
3. **Hyper-Local Geofencing**: Integrate precise GPS distance decay scoring for offline store visits.
