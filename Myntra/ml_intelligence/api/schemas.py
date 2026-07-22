"""
Pydantic Data Transfer Objects (DTOs) and API Contracts for ml_intelligence
Defines clean Pydantic V2 input/output models for public and internal service interfaces.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# DISCOVERY & ENTITY RESOLUTION SCHEMAS
# ============================================================================

class StoreRawRecord(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    raw_store_name: str = Field(..., description="Raw uncleaned merchant name")
    region: str = Field(..., description="City or region name")
    source_found: str = Field(..., description="Provenance source text")
    why_found: str = Field(..., description="Business evidence narrative text")


class StoreDiscoveryInput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    raw_source_path: str = Field(..., description="File path to raw dataset file")
    source_tag: str = Field("MANUAL_CURATED_SEED", description="Provenance tag")
    schema_version: str = Field("1.0.0", description="Contract version")


class StoreDiscoveryOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    schema_version: str = Field("1.0.0", description="Contract version")
    records_ingested: int = Field(..., ge=0, description="Total ingested rows")
    regions_found: List[str] = Field(..., description="Extracted regional cities")
    raw_stores: List[StoreRawRecord] = Field(..., description="Validated raw store records")


class StoreCanonicalRecord(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    store_id: str = Field(..., description="Canonical store identifier")
    brand_name: str = Field(..., description="Normalized brand title")
    branch_name: str = Field("General", description="Branch or locality title")
    canonical_name: str = Field(..., description="Combined canonical display name")
    city: str = Field(..., description="Standardized city name")
    state: str = Field("", description="Standardized state name")
    zone: str = Field("Pan-India", description="Geographic zone")
    why_found: str = Field("", description="Raw evidence text")
    source_found: str = Field("", description="Raw source text")


class EntityResolutionInput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    raw_stores: List[StoreRawRecord] = Field(..., description="Raw store records")
    similarity_threshold: float = Field(0.85, ge=0.0, le=1.0, description="Matching threshold")
    schema_version: str = Field("1.0.0", description="Contract version")


class EntityResolutionOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    schema_version: str = Field("1.0.0", description="Contract version")
    duplicate_clusters_found: int = Field(0, ge=0, description="Merged duplicate clusters count")
    resolved_stores: List[StoreCanonicalRecord] = Field(..., description="Canonical store entities")


# ============================================================================
# STORE INTELLIGENCE & EVIDENCE SCHEMAS
# ============================================================================

class StoreIntelligenceInput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    canonical_store: StoreCanonicalRecord = Field(..., description="Canonical entity DTO")
    taxonomy_version: str = Field("1.0.0", description="Taxonomy version tag")
    schema_version: str = Field("1.0.0", description="Contract version")


class StoreIntelligenceOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    schema_version: str = Field("1.0.0", description="Contract version")
    store_id: str = Field(..., description="Matching canonical store ID")
    primary_category: str = Field(..., description="Classified primary fashion category")
    specializations: List[str] = Field(default_factory=list, description="Extracted micro-specializations")
    search_tags: List[str] = Field(default_factory=list, description="Hashtags for search indexing")
    classification_confidence: float = Field(..., ge=0.0, le=1.0, description="Classification confidence")


class EvidenceAspectFlags(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    is_legacy: bool = Field(False, description="Has local legacy / household name signal")
    is_authentic: bool = Field(False, description="Has authentic craft signal")
    is_handloom: bool = Field(False, description="Has handloom weaver signal")
    is_bridal: bool = Field(False, description="Has wedding / bridal signal")
    is_government: bool = Field(False, description="Has government / state outlet signal")
    is_family_shopping: bool = Field(False, description="Has family shopping signal")
    price_segment: str = Field("Mid-Premium", description="Inferred price segment")


class EvidenceSnippet(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    aspect: str = Field(..., description="Aspect category name")
    snippet: str = Field(..., description="Exact matching substring")


class EvidenceExtractionInput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    store_id: str = Field(..., description="Canonical store ID")
    why_found: str = Field(..., description="Unstructured description narrative")
    schema_version: str = Field("1.0.0", description="Contract version")


class EvidenceExtractionOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    schema_version: str = Field("1.0.0", description="Contract version")
    store_id: str = Field(..., description="Matching canonical store ID")
    aspects: EvidenceAspectFlags = Field(..., description="Extracted aspect flags")
    evidence_snippets: List[EvidenceSnippet] = Field(default_factory=list, description="Matched text snippets")


# ============================================================================
# TRUST MATRIX SCHEMAS
# ============================================================================

class TrustDimensionScores(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    source_reliability: float = Field(..., ge=0.0, le=100.0)
    reputation: float = Field(..., ge=0.0, le=100.0)
    specialization: float = Field(..., ge=0.0, le=100.0)
    verifiability: float = Field(..., ge=0.0, le=100.0)
    catalog_capacity: float = Field(..., ge=0.0, le=100.0)


class TrustEvaluationInput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    store_id: str = Field(..., description="Canonical store ID")
    source_found: str = Field(..., description="Source provenance string")
    aspects: EvidenceAspectFlags = Field(..., description="Extracted aspects")
    why_found: str = Field(..., description="Raw text string")
    schema_version: str = Field("1.0.0", description="Contract version")


class TrustEvaluationOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    schema_version: str = Field("1.0.0", description="Contract version")
    store_id: str = Field(..., description="Matching canonical store ID")
    aggregate_trust_score: float = Field(..., ge=0.0, le=100.0, description="Aggregate Trust Score")
    trust_badge: str = Field(..., description="Assigned Trust Badge")
    dimension_scores: TrustDimensionScores = Field(..., description="5-Dimension Trust Matrix")
    supporting_evidence: List[str] = Field(..., description="Itemized explainability bullet points")
    risk_flags: List[str] = Field(default_factory=list, description="Detected risk flags")


# ============================================================================
# ELASTICSEARCH HYBRID SEARCH SCHEMAS
# ============================================================================

class GeoPoint(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    lat: float = Field(..., ge=-90.0, le=90.0)
    lon: float = Field(..., ge=-180.0, le=180.0)


class HybridSearchInput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    query: str = Field(..., description="Search intent text string")
    city_filter: Optional[str] = Field(None, description="City filter")
    min_trust_score: float = Field(0.0, ge=0.0, le=100.0, description="Min trust score filter")
    geo_location: Optional[GeoPoint] = Field(None, description="Geo coordinates")
    max_distance_km: float = Field(25.0, ge=0.0, description="Max search radius in km")
    top_k: int = Field(10, ge=1, le=100, description="Top K candidates requested")
    schema_version: str = Field("1.0.0", description="Contract version")


class SearchCandidateHit(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    store_id: str = Field(..., description="Candidate store ID")
    canonical_name: str = Field(..., description="Canonical merchant name")
    city: str = Field(..., description="City name")
    trust_score: float = Field(..., description="Aggregate Trust Score")
    rrf_score: float = Field(..., description="Reciprocal Rank Fusion score")
    dense_similarity_score: float = Field(0.0, description="Cosine vector similarity score")
    bm25_score: float = Field(0.0, description="BM25 text score")
    categories: List[str] = Field(default_factory=list, description="Categories")


class HybridSearchOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    schema_version: str = Field("1.0.0", description="Contract version")
    took_ms: int = Field(..., ge=0, description="Execution time in ms")
    total_hits: int = Field(..., ge=0, description="Total matching candidates")
    hits: List[SearchCandidateHit] = Field(..., description="Ranked hit results")


# ============================================================================
# PERSONALIZED RECOMMENDATION SCHEMAS (CORE FEATURE)
# ============================================================================

class PersonalizedRecommendationInput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    user_location: str = Field(..., description="User city or location e.g. Hyderabad")
    preferred_categories: List[str] = Field(default_factory=list, description="User preferred fashion categories")
    shopping_intent: str = Field("", description="Shopping intent e.g. wedding shopping for bridal silk sarees")
    user_preferences: Optional[Dict[str, Any]] = Field(None, description="User preference map (price_segment, favorite_styles, etc.)")
    top_k: int = Field(10, ge=1, le=50, description="Maximum recommendations requested")
    schema_version: str = Field("1.0.0", description="Contract version")


class RecommendedStoreProfile(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    store_id: str = Field(..., description="Canonical Store ID")
    canonical_name: str = Field(..., description="Canonical merchant name")
    city: str = Field(..., description="City name")
    state: str = Field("", description="State name")
    zone: str = Field("Pan-India", description="Geographic zone")
    primary_category: str = Field(..., description="Primary category")
    specializations: List[str] = Field(default_factory=list, description="Extracted store specializations")
    trust_score: float = Field(..., ge=0.0, le=100.0, description="Aggregate Trust Score")
    trust_badge: str = Field(..., description="Trust Badge tier")
    recommendation_score: float = Field(..., ge=0.0, le=100.0, description="Composite multi-signal recommendation score")
    explanation_reasons: List[str] = Field(..., description="Human-readable explanation bullet points")
    why_found: str = Field("", description="Verified business summary narrative")


class PersonalizedRecommendationOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    schema_version: str = Field("1.0.0", description="Contract version")
    user_location: str = Field(..., description="User location context")
    total_recommendations: int = Field(..., ge=0, description="Total store recommendations returned")
    recommendations: List[RecommendedStoreProfile] = Field(..., description="Ranked store recommendations")


# ============================================================================
# STORE PROFILE & RECOMMENDATION EXPLANATION SCHEMAS
# ============================================================================

class StoreProfileOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    schema_version: str = Field("1.0.0", description="Contract version")
    store_id: str = Field(..., description="Canonical Store ID")
    store_name: str = Field(..., description="Canonical merchant display name")
    city: str = Field(..., description="City name")
    region: str = Field(..., description="State or Geographic Zone")
    primary_categories: List[str] = Field(..., description="Primary fashion categories")
    specializations: List[str] = Field(default_factory=list, description="Store specializations")
    trust_badge: str = Field(..., description="Trust Badge tier")
    trust_score: float = Field(..., ge=0.0, le=100.0, description="Aggregate Trust Score")
    evidence_summary: List[str] = Field(..., description="Itemized supporting evidence bullets")
    recommendation_score: float = Field(..., ge=0.0, le=100.0, description="General regional recommendation equity score")
    short_business_summary: str = Field(..., description="Short business overview text")


class StoreReasonOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    schema_version: str = Field("1.0.0", description="Contract version")
    store_id: str = Field(..., description="Canonical Store ID")
    store_name: str = Field(..., description="Canonical merchant name")
    city: str = Field(..., description="City name")
    recommendation_score: float = Field(..., ge=0.0, le=100.0, description="Composite recommendation score")
    explanation_summary: str = Field(..., description="Overall recommendation summary sentence")
    contributing_signals: Dict[str, float] = Field(..., description="Score breakdown across the 6 recommendation signals")
    explanation_reasons: List[str] = Field(..., description="Itemized human-readable explanations")


# ============================================================================
# DOSSIER & INDEXING SCHEMAS
# ============================================================================

class DossierGenerationInput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    store_id: str = Field(..., description="Target store ID")
    include_bd_script: bool = Field(True, description="Flag to render BD pitch script")
    schema_version: str = Field("1.0.0", description="Contract version")


class DossierStructuredPayload(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    executive_summary: str = Field(..., description="Executive summary text")
    trust_evidence_summary: List[str] = Field(..., description="Trust bullet points")
    strengths: List[str] = Field(..., description="Store business strengths")
    weaknesses: List[str] = Field(..., description="Digital/Store weaknesses")
    business_opportunity: str = Field(..., description="Strategic Myntra opportunity")
    suggested_myntra_category: str = Field(..., description="Suggested catalog category")
    tailored_bd_pitch: str = Field(..., description="Opening sales pitch script")
    objection_handling: Dict[str, str] = Field(..., description="Objection handling dictionary")


class SellerDossierOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    schema_version: str = Field("1.0.0", description="Contract version")
    store_id: str = Field(..., description="Target store ID")
    canonical_name: str = Field(..., description="Canonical merchant name")
    dossier_markdown: str = Field(..., description="Full rendered markdown briefing")
    structured_dossier: DossierStructuredPayload = Field(..., description="Structured JSON dossier DTO")


class IndexDatasetInput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    raw_source_path: Optional[str] = Field(None, description="Optional raw seed dataset path")
    source_tag: str = Field("MANUAL_CURATED_SEED", description="Provenance tag")


class IndexDatasetOutput(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    schema_version: str = Field("1.0.0", description="Contract version")
    indexed_count: int = Field(..., description="Total store records indexed")
    regions_indexed: List[str] = Field(..., description="Distinct regional cities indexed")
    sample_store_ids: List[str] = Field(..., description="Sample store IDs indexed")
    message: str = Field(..., description="Index operation result message")


class MLServiceError(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    schema_version: str = Field("1.0.0", description="Contract version")
    error_code: int = Field(..., description="Unique numeric error code")
    error_type: str = Field(..., description="Error category string")
    message: str = Field(..., description="Human-readable error description")
    details: Optional[Dict[str, Any]] = Field(None, description="Contextual error details")
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp")
