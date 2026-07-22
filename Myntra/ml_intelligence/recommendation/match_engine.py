"""
Recommendation Match Engine Module for ml_intelligence
Powers Myntra's Regional Fashion Recommendation engine using 6 core signals:
1. Regional relevance
2. Category match
3. Shopping intent fit
4. Personalization alignment
5. Fashion specialization
6. Trust score
"""

from typing import List, Dict, Any, Optional
from ml_intelligence.api.schemas import (
    PersonalizedRecommendationInput,
    PersonalizedRecommendationOutput,
    RecommendedStoreProfile,
    StoreReasonOutput
)
from ml_intelligence.utils.logger import get_logger

logger = get_logger("ml_intelligence.recommendation")


class RecommendationMatchEngine:
    """Multi-factor recommendation engine combining 6 distinct fashion signals."""

    def __init__(self):
        pass

    def recommend_personalized(
        self, 
        input_dto: PersonalizedRecommendationInput, 
        store_index: Dict[str, Dict[str, Any]]
    ) -> PersonalizedRecommendationOutput:
        """
        Ranks enriched regional retailer index using 6 core signals:
        1. Regional relevance
        2. Category match
        3. Shopping intent fit
        4. Personalization alignment
        5. Fashion specialization
        6. Trust score
        """
        user_loc = input_dto.user_location.strip().lower()
        pref_cats = [c.strip().lower() for c in input_dto.preferred_categories if c.strip()]
        intent_lower = input_dto.shopping_intent.lower()
        pref_map = input_dto.user_preferences or {}

        candidates: List[RecommendedStoreProfile] = []

        for sid, store in store_index.items():
            signals = self._compute_signals(store, user_loc, pref_cats, intent_lower, pref_map)

            # Composite 6-Signal Score:
            # 0.20*Regional + 0.20*Category + 0.20*Intent + 0.15*Personalization + 0.15*Specialization + 0.10*Trust = 1.00
            rec_score = round(
                (0.20 * signals["regional_relevance"]) +
                (0.20 * signals["category_match"]) +
                (0.20 * signals["shopping_intent_fit"]) +
                (0.15 * signals["personalization"]) +
                (0.15 * signals["fashion_specialization"]) +
                (0.10 * signals["trust_score"]),
                1
            )

            # Generate Human-Readable Explanation Reasons
            explanation_reasons = self._generate_explanation_reasons(
                store=store,
                user_location=input_dto.user_location,
                pref_cats=input_dto.preferred_categories,
                shopping_intent=input_dto.shopping_intent,
                signals=signals
            )

            profile = RecommendedStoreProfile(
                store_id=sid,
                canonical_name=str(store.get("canonical_name", f"Store {sid}")),
                city=str(store.get("city", "")).title(),
                state=str(store.get("state", "")),
                zone=str(store.get("zone", "Pan-India")),
                primary_category=str(store.get("primary_category", "Family Shopping")),
                specializations=store.get("specializations", []),
                trust_score=signals["trust_score"],
                trust_badge=str(store.get("trust_badge", "Tier-2 Verified Regional Retailer")),
                recommendation_score=rec_score,
                explanation_reasons=explanation_reasons,
                why_found=str(store.get("why_found", ""))
            )
            candidates.append(profile)

        # Rank candidates by composite recommendation score descending
        candidates.sort(key=lambda x: x.recommendation_score, reverse=True)
        top_recommendations = candidates[:input_dto.top_k]

        logger.info(f"Generated {len(top_recommendations)} recommendations for user location '{input_dto.user_location}'.")

        return PersonalizedRecommendationOutput(
            user_location=input_dto.user_location,
            total_recommendations=len(top_recommendations),
            recommendations=top_recommendations
        )

    def get_recommendation_explanation(
        self, 
        store_id: str, 
        store: Dict[str, Any], 
        user_location: str = "Hyderabad"
    ) -> StoreReasonOutput:
        """Returns Recommendation Explanation DTO detailing the 6 signal contributions."""
        signals = self._compute_signals(
            store=store,
            user_loc=user_location.lower(),
            pref_cats=["bridal silk", "ethnic & festive"],
            intent_lower="wedding shopping",
            pref_map={}
        )

        rec_score = round(
            (0.20 * signals["regional_relevance"]) +
            (0.20 * signals["category_match"]) +
            (0.20 * signals["shopping_intent_fit"]) +
            (0.15 * signals["personalization"]) +
            (0.15 * signals["fashion_specialization"]) +
            (0.10 * signals["trust_score"]),
            1
        )

        city = str(store.get("city", "")).title()
        store_name = str(store.get("canonical_name", f"Store {store_id}"))

        explanation_reasons = self._generate_explanation_reasons(
            store=store,
            user_location=city,
            pref_cats=["Bridal Silk", "Ethnic Wear"],
            shopping_intent="regional fashion shopping",
            signals=signals
        )

        summary_sentence = f"{store_name} was recommended with a score of {rec_score}/100 based on strong {store.get('primary_category', 'fashion')} specialization and regional presence in {city}."

        return StoreReasonOutput(
            schema_version="1.0.0",
            store_id=store_id,
            store_name=store_name,
            city=city,
            recommendation_score=rec_score,
            explanation_summary=summary_sentence,
            contributing_signals=signals,
            explanation_reasons=explanation_reasons
        )

    def _compute_signals(
        self, 
        store: Dict[str, Any], 
        user_loc: str, 
        pref_cats: List[str], 
        intent_lower: str, 
        pref_map: Dict[str, Any]
    ) -> Dict[str, float]:
        """Computes score (0-100) across the 6 recommendation signals."""
        store_city = str(store.get("city", "")).strip().lower()
        trust = float(store.get("trust_score", store.get("aggregate_trust_score", 70.0)))
        why_text = str(store.get("why_found", "")).lower()
        specs = [s.lower() for s in store.get("specializations", [])]
        cats = [c.lower() for c in store.get("categories", [store.get("primary_category", "Family Shopping")])]
        primary_cat = str(store.get("primary_category", "")).lower()

        # 1. Regional Relevance
        if store_city == user_loc:
            reg_score = 100.0
        elif store.get("zone", "").lower() == "south" and any(c in user_loc for c in ["hyderabad", "bengaluru", "kochi", "chennai", "vijayawada"]):
            reg_score = 75.0
        else:
            reg_score = 50.0

        # 2. Category Match
        cat_score = 50.0
        if pref_cats:
            matches = sum(1 for pc in pref_cats if any(pc in sc or sc in pc for sc in cats + [primary_cat]))
            if matches > 0:
                cat_score = min(100.0, 70.0 + (matches * 15.0))

        # 3. Shopping Intent Fit
        intent_score = 60.0
        if intent_lower:
            tokens = [t for t in intent_lower.split() if len(t) > 3]
            matches = sum(1 for t in tokens if t in why_text or any(t in s for s in specs))
            if matches > 0:
                intent_score = min(100.0, 65.0 + (matches * 12.5))

        # 4. Personalization Alignment
        pref_segment = str(pref_map.get("price_segment", "")).lower()
        person_score = 65.0
        if pref_segment and pref_segment in why_text:
            person_score += 20.0
        if pref_cats and any(pc in why_text for pc in pref_cats):
            person_score += 15.0
        person_score = min(100.0, person_score)

        # 5. Fashion Specialization
        spec_score = 60.0
        if specs:
            spec_score = min(100.0, 70.0 + (len(specs) * 10.0))
        if any(k in why_text for k in ["handloom", "bridal", "pattu", "chanderi", "heritage", "boutique"]):
            spec_score = min(100.0, spec_score + 15.0)

        # 6. Trust Score
        t_score = min(100.0, max(0.0, trust))

        return {
            "regional_relevance": round(reg_score, 1),
            "category_match": round(cat_score, 1),
            "shopping_intent_fit": round(intent_score, 1),
            "personalization": round(person_score, 1),
            "fashion_specialization": round(spec_score, 1),
            "trust_score": round(t_score, 1)
        }

    def _generate_explanation_reasons(
        self,
        store: Dict[str, Any],
        user_location: str,
        pref_cats: List[str],
        shopping_intent: str,
        signals: Dict[str, float]
    ) -> List[str]:
        """Generates itemized human-readable rationale bullet points."""
        reasons = []
        city = str(store.get("city", "")).title()
        primary_cat = str(store.get("primary_category", "Regional Fashion"))
        badge = str(store.get("trust_badge", "Tier-2 Verified Regional Retailer"))
        why_text = str(store.get("why_found", ""))
        specs = store.get("specializations", [])

        # Location Signal
        if city.lower() == user_location.lower():
            reasons.append(f"Trusted regional retailer in {city} ({badge}).")
        else:
            reasons.append(f"Highly rated regional fashion destination in {city} ({badge}).")

        # Specialization Signal
        if specs:
            reasons.append(f"Strong specialization in {', '.join(specs[:2])}.")
        else:
            reasons.append(f"Strong regional authority in {primary_cat}.")

        # Intent Match Signal
        if shopping_intent:
            reasons.append(f"Matches your '{shopping_intent}' shopping intent.")
        elif "bridal" in why_text.lower():
            reasons.append(f"Matches high-intent wedding and festive shopping needs.")

        # Category Signal
        if pref_cats:
            reasons.append(f"Matches your preferred fashion categories ({', '.join(pref_cats[:2])}).")
        else:
            reasons.append(f"Popular choice among local shoppers for authentic regional ethnic wear.")

        return reasons
