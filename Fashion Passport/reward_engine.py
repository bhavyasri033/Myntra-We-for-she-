"""
Reward Engine Module for Fashion Passport (Upgraded)
====================================================
Evaluates total earned badges against national reward milestones, unlocks rewards/coupons,
ensures idempotent reward distribution, and outputs frontend-friendly Progress Objects.
"""

from datetime import datetime, timezone
from typing import List, Dict, Any
from models import UserPassport, Reward, ProgressObject
from config import NATIONAL_REWARDS


class RewardEngine:
    """
    Evaluates and distributes National Rewards based on regional badge thresholds.
    Single Responsibility: National Reward evaluation & milestone tracking.
    """

    def __init__(self, reward_config: List[Dict[str, Any]] = None):
        self.reward_config = reward_config if reward_config is not None else NATIONAL_REWARDS

    def evaluate_rewards(self, user_passport: UserPassport) -> List[Dict[str, Any]]:
        """
        Evaluates cumulative unlocked badges and awards national rewards.
        Ensures each reward is issued exactly once.

        Returns a list of newly unlocked reward dictionaries.
        """
        total_badges = len(user_passport.badges)
        unlocked_reward_ids = {r["reward_id"] for r in user_passport.rewards}
        newly_unlocked: List[Dict[str, Any]] = []

        for reward_def in self.reward_config:
            reward_id = reward_def["reward_id"]
            req_badges = reward_def["required_badges"]

            if total_badges >= req_badges and reward_id not in unlocked_reward_ids:
                now_str = datetime.now(timezone.utc).isoformat()
                reward_obj = Reward(
                    reward_id=reward_id,
                    title=reward_def["title"],
                    description=reward_def["description"],
                    reward_icon=reward_def.get("reward_icon", "reward_default.png"),
                    required_badges=req_badges,
                    coupon_code=reward_def["coupon_code"],
                    unlocked_at=now_str
                )
                reward_dict = reward_obj.to_dict()
                user_passport.rewards.append(reward_dict)
                newly_unlocked.append(reward_dict)

        return newly_unlocked

    def get_reward_progress(self, user_passport: UserPassport) -> Dict[str, Any]:
        """
        Calculates progress toward the next National Reward milestone,
        returning a standard Progress Object.
        """
        total_badges = len(user_passport.badges)
        unlocked_reward_ids = {r["reward_id"] for r in user_passport.rewards}

        locked_rewards = [
            r for r in self.reward_config if r["reward_id"] not in unlocked_reward_ids
        ]

        if not locked_rewards:
            progress_obj = ProgressObject(
                current_points=total_badges,
                required_points=total_badges,
                remaining_points=0,
                progress_percentage=100.0
            )
            return {
                "all_rewards_unlocked": True,
                "next_reward_id": None,
                "next_reward_title": None,
                "reward_icon": None,
                "coupon_code": None,
                "progress": progress_obj.to_dict()
            }

        next_reward = min(locked_rewards, key=lambda x: x["required_badges"])
        req_badges = next_reward["required_badges"]
        remaining = max(0, req_badges - total_badges)
        progress_pct = min(100.0, round((total_badges / req_badges) * 100, 1))

        progress_obj = ProgressObject(
            current_points=total_badges,
            required_points=req_badges,
            remaining_points=remaining,
            progress_percentage=progress_pct
        )

        return {
            "all_rewards_unlocked": False,
            "next_reward_id": next_reward["reward_id"],
            "next_reward_title": next_reward["title"],
            "reward_icon": next_reward.get("reward_icon", "reward_default.png"),
            "coupon_code": next_reward["coupon_code"],
            "progress": progress_obj.to_dict()
        }
