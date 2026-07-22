"""
Passport Engine Module for Fashion Passport (Upgraded)
======================================================
Main service orchestrator handling user actions, 3 point categories (Discovery,
Engagement, Shopping), Store Loyalty tracking, Timeline event generation,
India Map status generation, Analytics computation, and Dashboard Summary building.
"""

from datetime import datetime, timezone
import uuid
from typing import Dict, List, Any, Optional

from models import (
    UserPassport, ActivityLog, Product, RegionalStore, ActionType,
    TimelineEvent, StoreLoyalty, ProgressObject
)
from config import (
    POINT_RULES, SUPPORTED_REGIONS, REGION_METADATA, REGIONAL_BADGES,
    NATIONAL_REWARDS, STORE_LOYALTY_TIERS, PASSPORT_LEVELS
)
from badge_engine import BadgeEngine
from reward_engine import RewardEngine
from sample_data import InMemoryRepository


class PassportEngine:
    """
    Core backend orchestrator service for Fashion Passport.
    Integrates directly with Myntra's 'Regional Fashion Icons' store network.
    """

    def __init__(self, repository: Optional[InMemoryRepository] = None):
        self.repository = repository if repository is not None else InMemoryRepository()
        self.badge_engine = BadgeEngine()
        self.reward_engine = RewardEngine()
        self.point_rules = POINT_RULES

    # -------------------------------------------------------------------
    # Core Engine Primitive Functions
    # -------------------------------------------------------------------

    def add_points(
        self,
        user_id: str,
        action_type: str,
        region: str,
        details: str,
        store_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Adds points across 3 independent categories (Discovery, Engagement, Shopping).
        Updates Store Loyalty and logs Activity & Timeline events.
        """
        if action_type not in self.point_rules:
            raise ValueError(f"Invalid action_type: {action_type}")

        if region not in SUPPORTED_REGIONS and region != "Global":
            raise ValueError(f"Unsupported region: {region}")

        user = self.repository.get_or_create_user(user_id)
        rule = self.point_rules[action_type]
        pts_earned = rule["points"]
        category = rule["category"]

        # 1. Update total & categorical point balances
        user.passport_points += pts_earned
        if category == "discovery":
            user.discovery_points += pts_earned
        elif category == "engagement":
            user.engagement_points += pts_earned
        elif category == "shopping":
            user.shopping_points += pts_earned

        # 2. Update region points & visited regions
        if region != "Global":
            user.region_points[region] = user.region_points.get(region, 0) + pts_earned
            if region not in user.visited_regions:
                user.visited_regions.append(region)
                # Log region discovery timeline event
                self._record_timeline_event(
                    user,
                    title=f"Explored {region} Fashion Hub",
                    description=f"First time exploring regional fashion icon stores in {region}!",
                    event_type="REGION_EXPLORED",
                    icon="timeline_region.png"
                )

        # 3. Update Store Loyalty if action is store-linked
        if store_name and store_name != "Global":
            self._update_store_loyalty(user, store_name, region, action_type, pts_earned)

        # 4. Record Activity Log
        activity = ActivityLog(
            activity_id=f"ACT_{uuid.uuid4().hex[:8].upper()}",
            user_id=user_id,
            action_type=action_type,
            category=category,
            region=region,
            store_name=store_name,
            points_earned=pts_earned,
            details=details,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        user.activity_history.insert(0, activity.to_dict())
        user.last_activity = activity.timestamp

        # 5. Check for badge and reward unlocks
        new_badges = self.check_badges(user_id, region) if region != "Global" else []
        new_rewards = self.check_rewards(user_id)

        # 6. Save updated user state
        self.repository.save_user(user)

        return {
            "success": True,
            "user_id": user_id,
            "action_type": action_type,
            "category": category,
            "region": region,
            "store_name": store_name,
            "points_earned": pts_earned,
            "total_passport_points": user.passport_points,
            "discovery_points": user.discovery_points,
            "engagement_points": user.engagement_points,
            "shopping_points": user.shopping_points,
            "newly_unlocked_badges": new_badges,
            "newly_unlocked_rewards": new_rewards
        }

    def check_badges(self, user_id: str, region: str) -> List[Dict[str, Any]]:
        """Evaluates regional points and logs timeline events for new badge unlocks."""
        user = self.repository.get_or_create_user(user_id)
        newly_unlocked = self.badge_engine.evaluate_badges_for_region(user, region)

        for badge in newly_unlocked:
            self._record_timeline_event(
                user,
                title=f"Unlocked {badge['badge_name']} Badge",
                description=f"Earned {badge['required_points']} points in {region}! {badge['badge_description']}",
                event_type="BADGE_UNLOCK",
                icon=badge["badge_icon"]
            )

        if newly_unlocked:
            self.repository.save_user(user)
        return newly_unlocked

    def check_rewards(self, user_id: str) -> List[Dict[str, Any]]:
        """Evaluates national badge count and logs timeline events for new reward unlocks."""
        user = self.repository.get_or_create_user(user_id)
        newly_unlocked = self.reward_engine.evaluate_rewards(user)

        for reward in newly_unlocked:
            self._record_timeline_event(
                user,
                title=f"Unlocked Reward: {reward['title']}",
                description=f"Reached {reward['required_badges']} regional badges milestone! Coupon: {reward['coupon_code']}",
                event_type="REWARD_UNLOCK",
                icon=reward["reward_icon"]
            )

        if newly_unlocked:
            self.repository.save_user(user)
        return newly_unlocked

    # -------------------------------------------------------------------
    # Higher-Level User Actions (Called by Frontend / API)
    # -------------------------------------------------------------------

    def view_store(self, user_id: str, store_name: str, region: str) -> Dict[str, Any]:
        """User views a regional store page."""
        details = f"Visited regional icon store '{store_name}' in {region}"
        res = self.add_points(user_id, ActionType.VIEW_STORE.value, region, details, store_name=store_name)
        res["passport_summary"] = self.get_passport(user_id)
        return res

    def view_product(self, user_id: str, product_id: str) -> Dict[str, Any]:
        """User views a regional product."""
        product = self.repository.get_product(product_id)
        if not product:
            raise ValueError(f"Product '{product_id}' not found.")

        details = f"Viewed '{product.product_name}' from {product.store_name} ({product.region})"
        res = self.add_points(user_id, ActionType.VIEW_PRODUCT.value, product.region, details, store_name=product.store_name)
        res["passport_summary"] = self.get_passport(user_id)
        return res

    def wishlist_product(self, user_id: str, product_id: str) -> Dict[str, Any]:
        """User wishlists a regional product."""
        product = self.repository.get_product(product_id)
        if not product:
            raise ValueError(f"Product '{product_id}' not found.")

        details = f"Wishlisted '{product.product_name}' from {product.store_name} ({product.region})"
        res = self.add_points(user_id, ActionType.WISHLIST_PRODUCT.value, product.region, details, store_name=product.store_name)
        res["passport_summary"] = self.get_passport(user_id)
        return res

    def share_product(self, user_id: str, product_id: str) -> Dict[str, Any]:
        """User shares a regional product on social platforms."""
        product = self.repository.get_product(product_id)
        if not product:
            raise ValueError(f"Product '{product_id}' not found.")

        details = f"Shared '{product.product_name}' from {product.store_name} ({product.region})"
        res = self.add_points(user_id, ActionType.SHARE_PRODUCT.value, product.region, details, store_name=product.store_name)
        res["passport_summary"] = self.get_passport(user_id)
        return res

    def follow_store(self, user_id: str, store_name: str, region: str) -> Dict[str, Any]:
        """User follows a regional artisan store."""
        details = f"Followed regional store '{store_name}' in {region}"
        res = self.add_points(user_id, ActionType.FOLLOW_STORE.value, region, details, store_name=store_name)
        res["passport_summary"] = self.get_passport(user_id)
        return res

    def purchase_product(self, user_id: str, product_id: str) -> Dict[str, Any]:
        """User purchases a regional fashion product."""
        product = self.repository.get_product(product_id)
        if not product:
            raise ValueError(f"Product '{product_id}' not found.")

        user = self.repository.get_or_create_user(user_id)
        purchase_entry = {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "store_id": product.store_id,
            "store_name": product.store_name,
            "region": product.region,
            "category": product.category,
            "price": product.price,
            "purchased_at": datetime.now(timezone.utc).isoformat()
        }
        user.purchase_history.insert(0, purchase_entry)

        # Log timeline purchase milestone
        self._record_timeline_event(
            user,
            title=f"Purchased from {product.store_name}",
            description=f"Bought '{product.product_name}' (₹{product.price}) from {product.region}!",
            event_type="PURCHASE",
            icon="timeline_purchase.png"
        )
        self.repository.save_user(user)

        details = f"Purchased '{product.product_name}' (₹{product.price}) from {product.store_name} ({product.region})"
        res = self.add_points(user_id, ActionType.PURCHASE_PRODUCT.value, product.region, details, store_name=product.store_name)
        res["passport_summary"] = self.get_passport(user_id)
        return res

    def review_product(self, user_id: str, product_id: str, is_verified: bool = True) -> Dict[str, Any]:
        """User reviews a regional product."""
        product = self.repository.get_product(product_id)
        if not product:
            raise ValueError(f"Product '{product_id}' not found.")

        details = f"Posted verified review for '{product.product_name}' in {product.region}"
        res = self.add_points(user_id, ActionType.VERIFIED_REVIEW.value, product.region, details, store_name=product.store_name)
        res["passport_summary"] = self.get_passport(user_id)
        return res

    def complete_profile(self, user_id: str) -> Dict[str, Any]:
        """User completes regional style preferences profile."""
        details = "Completed regional fashion taste profile"
        res = self.add_points(user_id, ActionType.COMPLETE_PROFILE.value, "Global", details)

        user = self.repository.get_or_create_user(user_id)
        self._record_timeline_event(
            user,
            title="Completed Regional Profile",
            description="Configured regional fashion preferences and style goals.",
            event_type="PROFILE_COMPLETE",
            icon="timeline_profile.png"
        )
        self.repository.save_user(user)

        res["passport_summary"] = self.get_passport(user_id)
        return res

    # -------------------------------------------------------------------
    # Helper & Analytics Computations
    # -------------------------------------------------------------------

    def _update_store_loyalty(
        self, user: UserPassport, store_name: str, region: str, action_type: str, pts_earned: int
    ) -> None:
        """Updates Store Loyalty record and evaluates Store Loyalty level up."""
        if store_name not in user.store_loyalty:
            store_obj = self.repository.get_store_by_name(store_name)
            store_id = store_obj.store_id if store_obj else f"STORE_{store_name.upper().replace(' ', '_')}"
            user.store_loyalty[store_name] = StoreLoyalty(
                store_id=store_id,
                store_name=store_name,
                region=region
            ).to_dict()

        sl = user.store_loyalty[store_name]
        sl["points_earned"] += pts_earned

        if action_type in (ActionType.VIEW_STORE.value, ActionType.VIEW_PRODUCT.value):
            sl["visits"] += 1
        elif action_type == ActionType.PURCHASE_PRODUCT.value:
            sl["purchases"] += 1
        elif action_type == ActionType.WISHLIST_PRODUCT.value:
            sl["wishlists"] += 1
        elif action_type == ActionType.SHARE_PRODUCT.value:
            sl["shares"] += 1
        elif action_type == ActionType.VERIFIED_REVIEW.value:
            sl["reviews"] += 1

        # Calculate new loyalty tier
        current_tier = sl["loyalty_level"]
        new_tier = "Bronze"
        next_pts = 15

        for tier in STORE_LOYALTY_TIERS:
            if sl["points_earned"] >= tier["min_points"]:
                new_tier = tier["level"]
                next_pts = tier["next_tier_points"]

        sl["loyalty_level"] = new_tier

        # Calculate progress to next tier
        if next_pts is not None:
            rem = max(0, next_pts - sl["points_earned"])
            pct = min(100.0, round((sl["points_earned"] / next_pts) * 100, 1))
            sl["progress_to_next_tier"] = ProgressObject(
                current_points=sl["points_earned"],
                required_points=next_pts,
                remaining_points=rem,
                progress_percentage=pct
            ).to_dict()
        else:
            sl["progress_to_next_tier"] = ProgressObject(
                current_points=sl["points_earned"],
                required_points=sl["points_earned"],
                remaining_points=0,
                progress_percentage=100.0
            ).to_dict()

        # Log store loyalty level up event if tier upgraded
        if new_tier != current_tier:
            self._record_timeline_event(
                user,
                title=f"Reached {new_tier} Loyalty at {store_name}",
                description=f"Unlocked {new_tier} tier benefits with {store_name} ({region})!",
                event_type="STORE_LOYALTY_LEVELUP",
                icon="timeline_loyalty.png"
            )

    def _record_timeline_event(
        self, user: UserPassport, title: str, description: str, event_type: str, icon: str
    ) -> None:
        """Records an event into user's chronological Passport Timeline."""
        event = TimelineEvent(
            timeline_id=f"TL_{uuid.uuid4().hex[:8].upper()}",
            title=title,
            description=description,
            event_type=event_type,
            icon=icon,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        user.timeline.insert(0, event.to_dict())  # Newest first

    def _build_india_map_status(self, user: UserPassport) -> Dict[str, Any]:
        """
        Builds status for all supported regions for interactive frontend India Map visualization.
        """
        unlocked_badge_regions = {b["region"] for b in user.badges}
        map_status = {}

        for region in SUPPORTED_REGIONS:
            meta = REGION_METADATA.get(region, {})
            current_pts = user.region_points.get(region, 0)
            target_pts = 25  # Base regional badge requirement
            explored = region in user.visited_regions
            badge_unlocked = region in unlocked_badge_regions
            pct = min(100.0, round((current_pts / target_pts) * 100, 1))

            map_status[region] = {
                "city": meta.get("city", region),
                "state": meta.get("state", ""),
                "landmark": meta.get("landmark", ""),
                "theme_color": meta.get("theme_color", "#8B5CF6"),
                "badge_name": meta.get("badge_name", f"{region} Explorer"),
                "badge_icon": meta.get("badge_icon", ""),
                "explored": explored,
                "badge_unlocked": badge_unlocked,
                "current_points": current_pts,
                "required_points": target_pts,
                "progress_percentage": pct
            }
        return map_status

    def _calculate_user_level(self, total_points: int) -> Dict[str, Any]:
        """Calculates Passport User Level and level progress object."""
        current_lvl = PASSPORT_LEVELS[0]
        next_lvl = PASSPORT_LEVELS[1]

        for idx, lvl in enumerate(PASSPORT_LEVELS):
            if total_points >= lvl["min_points"]:
                current_lvl = lvl
                if idx + 1 < len(PASSPORT_LEVELS):
                    next_lvl = PASSPORT_LEVELS[idx + 1]
                else:
                    next_lvl = None

        if next_lvl:
            req_pts = next_lvl["min_points"]
            rem_pts = max(0, req_pts - total_points)
            pct = min(100.0, round((total_points / req_pts) * 100, 1))
            lvl_progress = ProgressObject(
                current_points=total_points,
                required_points=req_pts,
                remaining_points=rem_pts,
                progress_percentage=pct
            ).to_dict()
        else:
            lvl_progress = ProgressObject(
                current_points=total_points,
                required_points=total_points,
                remaining_points=0,
                progress_percentage=100.0
            ).to_dict()

        return {
            "level": current_lvl["level"],
            "title": current_lvl["title"],
            "progress": lvl_progress
        }

    def _calculate_statistics(self, user: UserPassport) -> Dict[str, Any]:
        """Generates analytics summary for the user."""
        total_purchases = len(user.purchase_history)
        total_spent = sum(p.get("price", 0.0) for p in user.purchase_history)

        # Region frequency analysis
        region_counts: Dict[str, int] = {}
        for act in user.activity_history:
            reg = act.get("region")
            if reg and reg != "Global":
                region_counts[reg] = region_counts.get(reg, 0) + 1

        fav_region = max(region_counts, key=region_counts.get) if region_counts else "None"

        # Store frequency analysis
        store_counts: Dict[str, int] = {}
        for act in user.activity_history:
            st = act.get("store_name")
            if st and st != "Global":
                store_counts[st] = store_counts.get(st, 0) + 1

        fav_store = max(store_counts, key=store_counts.get) if store_counts else "None"

        # Product views count
        prod_views = sum(1 for a in user.activity_history if a.get("action_type") in ("VIEW_PRODUCT", "WISHLIST_PRODUCT"))

        return {
            "total_purchases": total_purchases,
            "total_spent_inr": round(total_spent, 2),
            "favorite_region": fav_region,
            "favorite_store": fav_store,
            "most_visited_region": fav_region,
            "total_stores_explored": len(user.store_loyalty),
            "total_products_viewed": prod_views,
            "badge_count": len(user.badges),
            "reward_count": len(user.rewards)
        }

    # -------------------------------------------------------------------
    # Query & Comprehensive Passport Summary Function
    # -------------------------------------------------------------------

    def get_passport(self, user_id: str) -> Dict[str, Any]:
        """
        Generates comprehensive, frontend-ready JSON Passport Summary.
        Contains profile, level, 3 point scores, map status, badges, rewards,
        timeline, statistics, and store loyalties.
        """
        user = self.repository.get_or_create_user(user_id)
        user_level_info = self._calculate_user_level(user.passport_points)
        region_progress = self.badge_engine.get_overall_next_badge_progress(user)
        reward_progress = self.reward_engine.get_reward_progress(user)
        stats = self._calculate_statistics(user)
        map_status = self._build_india_map_status(user)

        return {
            "user_profile": {
                "user_id": user.user_id,
                "passport_level": user_level_info["level"],
                "passport_title": user_level_info["title"],
                "joined_at": user.joined_at,
                "last_activity": user.last_activity
            },
            "level_progress": user_level_info["progress"],
            "points_summary": {
                "total_passport_points": user.passport_points,
                "discovery_points": user.discovery_points,
                "engagement_points": user.engagement_points,
                "shopping_points": user.shopping_points
            },
            "favorite_region": stats["favorite_region"],
            "favorite_regional_store": stats["favorite_store"],
            "regions_explored_count": len(user.visited_regions),
            "total_regions_count": len(SUPPORTED_REGIONS),
            "points_per_region": user.region_points,
            "india_map_status": map_status,
            "unlocked_badges": user.badges,
            "total_badges_count": len(user.badges),
            "region_badge_progress": region_progress,
            "unlocked_rewards": user.rewards,
            "reward_milestone_progress": reward_progress,
            "store_loyalty": list(user.store_loyalty.values()),
            "timeline": user.timeline[:15],  # Top 15 newest events
            "recent_activities": user.activity_history[:10],
            "statistics": stats
        }

    def get_region_progress(self, user_id: str) -> Dict[str, Any]:
        """Returns region points breakdown and progress objects."""
        user = self.repository.get_or_create_user(user_id)
        return {
            "user_id": user_id,
            "points_per_region": user.region_points,
            "progress_per_region": self.badge_engine.get_overall_next_badge_progress(user)
        }

    def get_activity_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Returns recent activity log entries."""
        user = self.repository.get_or_create_user(user_id)
        return user.activity_history[:limit]
