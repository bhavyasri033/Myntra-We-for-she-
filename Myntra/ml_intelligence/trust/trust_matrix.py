"""
Trust Matrix Calculator Module for ml_intelligence
Computes 5-dimension Trust Score matrix and assigns Trust Badges.
"""

from ml_intelligence.api.schemas import (
    TrustDimensionScores, 
    TrustEvaluationInput, 
    TrustEvaluationOutput
)
from ml_intelligence.trust.explainability import ExplainabilityEngine
from ml_intelligence.utils.logger import get_logger

logger = get_logger("ml_intelligence.trust")


class TrustMatrixCalculator:
    """Calculates 5-dimension Trust Score and generates explainable evidence rationale."""

    def __init__(self):
        self.explainability_engine = ExplainabilityEngine()

    def evaluate(self, input_dto: TrustEvaluationInput) -> TrustEvaluationOutput:
        """Evaluates trust input DTO and returns TrustEvaluationOutput."""
        aspects = input_dto.aspects
        sources = [s.strip() for s in input_dto.source_found.split(",") if s.strip()]

        # 1. Source Reliability (25%)
        source_rel = min(100.0, 70.0 + (len(sources) * 12.5))

        # 2. Reputation Score (30%)
        rep_score = 60.0
        if aspects.is_legacy:
            rep_score += 20.0
        if aspects.is_family_shopping:
            rep_score += 15.0
        rep_score = min(100.0, rep_score)

        # 3. Specialization Score (20%)
        spec_score = 65.0
        if aspects.is_bridal:
            spec_score += 20.0
        if aspects.is_handloom:
            spec_score += 15.0
        spec_score = min(100.0, spec_score)

        # 4. Verifiability Score (15%)
        verif_score = 95.0 if any(s in input_dto.source_found.lower() for s in ["gemini", "chatgpt", "perplexity", "google"]) else 75.0

        # 5. Catalog Capacity Score (10%)
        cat_score = 90.0 if aspects.is_family_shopping else 75.0

        # Weighted Aggregate: 0.30*Rep + 0.25*Source + 0.20*Spec + 0.15*Verif + 0.10*Cat = 1.00
        aggregate_score = round(
            (0.30 * rep_score) +
            (0.25 * source_rel) +
            (0.20 * spec_score) +
            (0.15 * verif_score) +
            (0.10 * cat_score),
            1
        )

        dim_scores = TrustDimensionScores(
            source_reliability=round(source_rel, 1),
            reputation=round(rep_score, 1),
            specialization=round(spec_score, 1),
            verifiability=round(verif_score, 1),
            catalog_capacity=round(cat_score, 1)
        )

        if aggregate_score >= 85.0:
            badge = "Tier-1 Trusted Anchor"
        elif aggregate_score >= 75.0:
            badge = "Tier-2 Verified Regional Retailer"
        else:
            badge = "Tier-3 Emerging Candidate"

        bullets = self.explainability_engine.generate_supporting_evidence(
            input_dto.source_found, 
            aspects, 
            dim_scores.model_dump()
        )
        risk_flags = self.explainability_engine.detect_risk_flags(dim_scores.model_dump())

        return TrustEvaluationOutput(
            store_id=input_dto.store_id,
            aggregate_trust_score=aggregate_score,
            trust_badge=badge,
            dimension_scores=dim_scores,
            supporting_evidence=bullets,
            risk_flags=risk_flags
        )
