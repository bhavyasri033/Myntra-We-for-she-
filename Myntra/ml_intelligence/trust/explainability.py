"""
Explainability Engine Module for ml_intelligence
Generates itemized supporting evidence rationale bullets for Trust Scores.
"""

from typing import List, Dict
from ml_intelligence.api.schemas import EvidenceAspectFlags


class ExplainabilityEngine:
    """Generates human-readable supporting evidence bullet points for Trust Scores."""

    @staticmethod
    def generate_supporting_evidence(
        source_found: str, 
        aspects: EvidenceAspectFlags, 
        dim_scores: Dict[str, float]
    ) -> List[str]:
        """Synthesizes structured bullet points explaining trust score."""
        bullets = []

        sources = [s.strip() for s in source_found.split(",") if s.strip()]
        if len(sources) >= 2:
            bullets.append(f"Verified across {len(sources)} independent discovery sources ({', '.join(sources)})")
        elif len(sources) == 1:
            bullets.append(f"Verified via discovery source ({sources[0]})")
        else:
            bullets.append("Verified via regional field discovery audit")

        if aspects.is_legacy and aspects.is_handloom:
            bullets.append("High heritage authority: Verified legacy handloom weaver retailer")
        elif aspects.is_legacy:
            bullets.append("Established local brand equity: Recognized household fashion brand")
        elif aspects.is_handloom:
            bullets.append("Authentic craft specialization in traditional handloom textiles")

        if aspects.is_bridal:
            bullets.append("High market demand alignment: Recognized regional specialist for bridal & wedding wear")
        if aspects.is_family_shopping:
            bullets.append("High catalog capacity: Established regional multi-floor family shopping destination")

        if len(bullets) < 2:
            bullets.append("Verified regional fashion retailer with active local market presence")

        return bullets

    @staticmethod
    def detect_risk_flags(dim_scores: Dict[str, float]) -> List[str]:
        """Identifies potential risk flags based on dimension thresholds."""
        flags = []
        if dim_scores.get("verifiability", 100.0) < 70.0:
            flags.append("Unverified Physical Location Link")
        if dim_scores.get("reputation", 100.0) < 60.0:
            flags.append("Low Digital Evidence Footprint")
        return flags
