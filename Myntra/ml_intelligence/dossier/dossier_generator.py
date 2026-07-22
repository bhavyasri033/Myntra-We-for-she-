"""
Retailer Summary Generator Module for ml_intelligence
Synthesizes structured Retailer Profiles and briefing summaries.
"""

from typing import Dict, Any
from ml_intelligence.api.schemas import (
    DossierGenerationInput, 
    SellerDossierOutput, 
    DossierStructuredPayload
)
from ml_intelligence.dossier.prompt_templates import DOSSIER_MARKDOWN_TEMPLATE
from ml_intelligence.utils.logger import get_logger

logger = get_logger("ml_intelligence.dossier")


class DossierGenerator:
    """Synthesizes Retailer Summaries and Retailer Profiles."""

    def __init__(self):
        pass

    def generate(self, input_dto: DossierGenerationInput, store_payload: Dict[str, Any]) -> SellerDossierOutput:
        """Renders retailer profile markdown and structured JSON DTO."""
        sid = input_dto.store_id
        canonical_name = store_payload.get("canonical_name", "Regional Merchant")
        city = store_payload.get("city", "India").title()
        state = store_payload.get("state", "")
        trust_score = float(store_payload.get("trust_score", store_payload.get("aggregate_trust_score", 85.0)))
        badge = store_payload.get("trust_badge", "Tier-1 Trusted Anchor")
        why_found = store_payload.get("why_found", "Trusted regional fashion retailer.")
        categories = store_payload.get("categories", ["Family Shopping"])
        cat = categories[0] if categories else "Ethnic Wear"

        exec_summary = f"{canonical_name} is a premier fashion destination located in {city}, {state}. " \
                       f"Renowned locally for {why_found.lower()}, this merchant represents a high-value anchor seller candidate for Myntra's regional fashion catalog expansion."

        trust_evidence_list = [
            f"Verified aggregate trust index of {trust_score}/100 ({badge})",
            f"High regional brand equity & customer demand in {city}",
            f"Specialized craft authority in {cat}"
        ]
        trust_ev_text = "\n".join([f"• {e}" for e in trust_evidence_list])

        opportunity = f"Onboard {canonical_name} as a Key Regional Partner for Myntra's Tier-2/3 {cat} expansion."
        pitch_script = f"\"Namaste! Myntra recognizes {canonical_name} as one of {city}'s leading destinations for {cat}. " \
                       f"We are inviting top-tier regional brand leaders to present their authentic collection to 50M+ fashion shoppers across India with zero upfront listing fees.\""

        objection_concern = "We don't have digital photography or e-commerce catalog staff."
        objection_resp = "Myntra provides automated smartphone catalog digitisation. Simply snap photos of your stock, and our AI pipeline converts them into live Myntra product listings!"

        structured = DossierStructuredPayload(
            executive_summary=exec_summary,
            trust_evidence_summary=trust_evidence_list,
            strengths=["Strong regional brand recall", "Vast festive & ethnic inventory", "High footfall density"],
            weaknesses=["Unorganized digital catalog presence"],
            business_opportunity=opportunity,
            suggested_myntra_category=f"Ethnic & Festive Wear ({cat})",
            tailored_bd_pitch=pitch_script,
            objection_handling={
                "concern": objection_concern,
                "bd_response": objection_resp
            }
        )

        md_text = DOSSIER_MARKDOWN_TEMPLATE.format(
            canonical_name=canonical_name,
            city=city,
            state=state,
            trust_score=trust_score,
            badge=badge,
            executive_summary=exec_summary,
            trust_evidence=trust_ev_text,
            suggested_category=f"Ethnic & Festive Wear ({cat})",
            business_opportunity=opportunity,
            bd_pitch_script=pitch_script,
            objection_concern=objection_concern,
            objection_response=objection_resp
        )

        logger.info(f"Generated Retailer Summary for store ID: '{sid}'")

        return SellerDossierOutput(
            store_id=sid,
            canonical_name=canonical_name,
            dossier_markdown=md_text,
            structured_dossier=structured
        )
