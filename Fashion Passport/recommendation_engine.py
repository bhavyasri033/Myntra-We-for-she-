"""
Recommendation Engine Module for Fashion Passport (New)
======================================================
Lightweight Recommendation Helper that integrates Fashion Passport progress
with Myntra's 'Regional Fashion Icons' core recommendation system.
Provides recommendations for next regions to explore, top stores to visit, and badge targets.
"""

from typing import Dict, List, Any, Optional
from models import UserPassport
from config import SUPPORTED_REGIONS, REGION_METADATA, REGIONAL_BADGES
from sample_data import InMemoryRepository


class PassportRecommendationEngine:
    """
    Generates contextual recommendations for user exploration.
    Can be imported by Myntra's primary recommendation service.
    """

    def __init__(self, repository: Optional[InMemoryRepository] = None):
        self.repository = repository if repository is not None else InMemoryRepository()

    def recommend_next_region(self, user_id: str) -> Dict[str, Any]:
        """
        Recommends the next regional fashion hub for the user to explore.
        Based on unvisited regions and regional fashion style complements.
        """
        user = self.repository.get_or_create_user(user_id)
        visited = set(user.visited_regions)
        unvisited = [r for r in SUPPORTED_REGIONS if r not in visited]

        if not unvisited:
            return {
                "recommended_region": None,
                "reason": "All 5 regional fashion hubs fully explored! Keep earning points to unlock master badges.",
                "region_metadata": None
            }

        # Select highest-priority unvisited region
        target_region = unvisited[0]
        meta = REGION_METADATA.get(target_region, {})

        last_visited = user.visited_regions[-1] if user.visited_regions else "India"
        reason = f"Since you explored {last_visited}, discover {target_region}'s {meta.get('description', 'trusted regional boutiques')}."

        return {
            "recommended_region": target_region,
            "city": meta.get("city", target_region),
            "state": meta.get("state", ""),
            "theme_color": meta.get("theme_color", "#8B5CF6"),
            "landmark": meta.get("landmark", ""),
            "reason": reason,
            "badge_target": meta.get("badge_name", f"{target_region} Explorer")
        }

    def recommend_stores(self, user_id: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Recommends Regional Fashion Icon stores that the user has not yet interacted with.
        Prioritizes top-rated regional stores in user's favorite region or recommended next region.
        """
        user = self.repository.get_or_create_user(user_id)
        rec_region = self.recommend_next_region(user_id).get("recommended_region")

        target_regions = [rec_region] if rec_region else SUPPORTED_REGIONS
        interacted_stores = set(user.store_loyalty.keys())

        all_stores = self.repository.list_all_stores()
        recommended: List[Dict[str, Any]] = []

        for store in all_stores:
            if store.store_name not in interacted_stores:
                if store.region in target_regions or not rec_region:
                    recommended.append({
                        "store_id": store.store_id,
                        "store_name": store.store_name,
                        "region": store.region,
                        "city": store.city,
                        "state": store.state,
                        "description": store.description,
                        "rating": store.rating,
                        "logo_icon": store.logo_icon,
                        "reason": f"Top-rated regional icon store in {store.region}"
                    })

        # Return top N stores sorted by rating
        recommended.sort(key=lambda s: s["rating"], reverse=True)
        return recommended[:limit]

    def recommend_badge(self, user_id: str) -> Dict[str, Any]:
        """
        Identifies the closest locked badge for the user to target.
        Calculates minimum points needed to unlock the next milestone.
        """
        user = self.repository.get_or_create_user(user_id)
        unlocked_badge_ids = {b["badge_id"] for b in user.badges}

        candidate_badges = []

        for region, badges in REGIONAL_BADGES.items():
            current_points = user.region_points.get(region, 0)
            for badge in badges:
                if badge["badge_id"] not in unlocked_badge_ids:
                    pts_needed = max(0, badge["required_points"] - current_points)
                    candidate_badges.append({
                        "badge_id": badge["badge_id"],
                        "badge_name": badge["badge_name"],
                        "region": region,
                        "badge_icon": badge["badge_icon"],
                        "badge_color": badge["badge_color"],
                        "rarity": badge["rarity"],
                        "current_points": current_points,
                        "required_points": badge["required_points"],
                        "points_needed": pts_needed
                    })

        if not candidate_badges:
            return {
                "target_badge": None,
                "message": "All regional badges unlocked!"
            }

        # Select badge closest to completion
        closest_badge = min(candidate_badges, key=lambda b: b["points_needed"])
        closest_badge["message"] = (
            f"Earn only {closest_badge['points_needed']} more points in {closest_badge['region']} "
            f"to unlock the '{closest_badge['badge_name']}' badge!"
        )

        return closest_badge
