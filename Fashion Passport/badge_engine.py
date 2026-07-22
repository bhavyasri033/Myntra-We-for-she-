"""
Badge Engine Module for Fashion Passport (Upgraded)
===================================================
Evaluates regional points against rich badge criteria, unlocks regional badges,
ensures idempotent unlocks, and returns formatted Progress Objects.
"""

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from models import UserPassport, Badge, ProgressObject
from config import REGIONAL_BADGES, SUPPORTED_REGIONS


class BadgeEngine:
    """
    Evaluates and processes regional badges for users.
    Single Responsibility: Badge evaluation & progress calculation.
    """

    def __init__(self, badge_config: Dict[str, List[Dict[str, Any]]] = None):
        self.badge_config = badge_config if badge_config is not None else REGIONAL_BADGES

    def evaluate_badges_for_region(
        self, user_passport: UserPassport, region: str
    ) -> List[Dict[str, Any]]:
        """
        Evaluates regional points for a user and unlocks eligible regional badges.
        Ensures badges unlock only once per user.

        Returns a list of newly unlocked badge dictionaries.
        """
        if region not in self.badge_config:
            return []

        regional_points = user_passport.region_points.get(region, 0)
        unlocked_badge_ids = {b["badge_id"] for b in user_passport.badges}
        newly_unlocked: List[Dict[str, Any]] = []

        for badge_def in self.badge_config[region]:
            badge_id = badge_def["badge_id"]
            req_points = badge_def["required_points"]

            # Unlock badge if user meets required points and hasn't unlocked it yet
            if regional_points >= req_points and badge_id not in unlocked_badge_ids:
                now_str = datetime.now(timezone.utc).isoformat()
                badge_obj = Badge(
                    badge_id=badge_id,
                    badge_name=badge_def["badge_name"],
                    region=region,
                    badge_description=badge_def["badge_description"],
                    badge_icon=badge_def["badge_icon"],
                    badge_color=badge_def["badge_color"],
                    rarity=badge_def["rarity"],
                    required_points=req_points,
                    tier=badge_def.get("tier", 1),
                    unlocked_at=now_str
                )
                badge_dict = badge_obj.to_dict()
                user_passport.badges.append(badge_dict)
                newly_unlocked.append(badge_dict)

        return newly_unlocked

    def evaluate_all_regions(self, user_passport: UserPassport) -> List[Dict[str, Any]]:
        """Evaluates points across all supported regions and unlocks eligible badges."""
        all_newly_unlocked = []
        for region in self.badge_config:
            newly_unlocked = self.evaluate_badges_for_region(user_passport, region)
            all_newly_unlocked.extend(newly_unlocked)
        return all_newly_unlocked

    def get_badge_progress_for_region(
        self, user_passport: UserPassport, region: str
    ) -> Dict[str, Any]:
        """
        Calculates progress toward the next available badge in a specific region,
        returning standard Progress Objects for frontend rendering.
        """
        current_points = user_passport.region_points.get(region, 0)
        unlocked_badge_ids = {b["badge_id"] for b in user_passport.badges}

        region_badges = self.badge_config.get(region, [])
        locked_badges = [
            b for b in region_badges if b["badge_id"] not in unlocked_badge_ids
        ]

        if not locked_badges:
            progress_obj = ProgressObject(
                current_points=current_points,
                required_points=current_points,
                remaining_points=0,
                progress_percentage=100.0
            )
            return {
                "region": region,
                "all_badges_unlocked": True,
                "next_badge_id": None,
                "next_badge_name": None,
                "badge_icon": None,
                "badge_color": None,
                "rarity": None,
                "progress": progress_obj.to_dict()
            }

        next_badge = min(locked_badges, key=lambda x: x["required_points"])
        req_points = next_badge["required_points"]
        remaining = max(0, req_points - current_points)
        progress_pct = min(100.0, round((current_points / req_points) * 100, 1))

        progress_obj = ProgressObject(
            current_points=current_points,
            required_points=req_points,
            remaining_points=remaining,
            progress_percentage=progress_pct
        )

        return {
            "region": region,
            "all_badges_unlocked": False,
            "next_badge_id": next_badge["badge_id"],
            "next_badge_name": next_badge["badge_name"],
            "badge_icon": next_badge["badge_icon"],
            "badge_color": next_badge["badge_color"],
            "rarity": next_badge["rarity"],
            "progress": progress_obj.to_dict()
        }

    def get_overall_next_badge_progress(self, user_passport: UserPassport) -> List[Dict[str, Any]]:
        """Returns badge progress objects across all supported regions."""
        progress_list = []
        for region in SUPPORTED_REGIONS:
            progress_list.append(self.get_badge_progress_for_region(user_passport, region))
        return progress_list
