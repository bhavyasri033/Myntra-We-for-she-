"""
OVI Ranker Module for ml_intelligence
Calculates Onboarding Value Index (OVI) score and assigns onboarding priorities.
"""

from typing import Dict, Any

CATEGORY_DEMAND_GAPS: Dict[str, float] = {
    "Bridal Silk": 95.0,
    "Handloom Heritage": 90.0,
    "Ethnic & Festive": 80.0,
    "Designer & Boutique": 75.0,
    "Family Shopping": 85.0,
    "Casual & Everyday": 60.0
}


class OVIRanker:
    """Calculates OVI score (0-100) and priority level for a candidate store hit."""

    @staticmethod
    def calculate_ovi(trust_score: float, category: str = "Family Shopping", catalog_score: float = 80.0) -> Dict[str, Any]:
        """Formulates OVI score: 0.45*Trust + 0.35*DemandGap + 0.20*Catalog = OVI."""
        gap_score = CATEGORY_DEMAND_GAPS.get(category, 75.0)

        ovi = round(
            (0.45 * trust_score) +
            (0.35 * gap_score) +
            (0.20 * catalog_score),
            1
        )

        if ovi >= 88.0:
            priority = "URGENT TARGET"
            action = "Deploy Senior Territory BD Lead within 48 Hours"
        elif ovi >= 75.0:
            priority = "HIGH PRIORITY"
            action = "Initiate Automated Regional WhatsApp Outreach"
        elif ovi >= 65.0:
            priority = "MEDIUM PRIORITY"
            action = "Include in Regional Digital Nudge Campaign"
        else:
            priority = "MONITOR"
            action = "Re-evaluate after digital footprint expands"

        gmv_range = "₹50L - ₹2.5Cr" if ovi >= 80.0 else "₹20L - ₹50L"

        return {
            "ovi_score": ovi,
            "onboarding_priority": priority,
            "recommended_action": action,
            "estimated_annual_gmv": gmv_range
        }


if __name__ == "__main__":
    ranker = OVIRanker()
    res = ranker.calculate_ovi(92.5, "Bridal Silk")
    print("[OK] Calculated OVI Metrics:", res)
