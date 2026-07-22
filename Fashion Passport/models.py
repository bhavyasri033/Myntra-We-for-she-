"""
Models Module for Fashion Passport Engine (Upgraded)
===================================================
Defines enriched domain data models for User Passport, Regional Store, Product,
Badge, Reward, Timeline Events, Store Loyalty, and Progress Objects.
Designed for 1-to-1 mapping to PostgreSQL tables, Pydantic schemas, or OpenAPI spec.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from enum import Enum


class ActionType(str, Enum):
    """Supported user action types within the Fashion Passport system."""
    VIEW_STORE = "VIEW_STORE"
    VIEW_PRODUCT = "VIEW_PRODUCT"
    SEARCH_REGIONAL_STORE = "SEARCH_REGIONAL_STORE"
    WISHLIST_PRODUCT = "WISHLIST_PRODUCT"
    SHARE_PRODUCT = "SHARE_PRODUCT"
    FOLLOW_STORE = "FOLLOW_STORE"
    PURCHASE_PRODUCT = "PURCHASE_PRODUCT"
    VERIFIED_REVIEW = "VERIFIED_REVIEW"
    COMPLETE_PROFILE = "COMPLETE_PROFILE"


@dataclass
class ProgressObject:
    """Standardized Progress Object for clean frontend progress bar renderers."""
    current_points: int
    required_points: int
    remaining_points: int
    progress_percentage: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RegionalStore:
    """Represents a Regional Fashion Icon store registered on Myntra."""
    store_id: str
    store_name: str
    region: str
    city: str
    state: str
    description: str
    rating: float = 4.5
    logo_icon: str = "store_default.png"
    banner_image: str = "banner_default.jpg"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Product:
    """Represents a regional fashion product linked to a specific store and region."""
    product_id: str
    product_name: str
    store_id: str
    store_name: str
    region: str
    category: str
    price: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Badge:
    """Represents a rich regional milestone badge."""
    badge_id: str
    badge_name: str
    region: str
    badge_description: str
    badge_icon: str
    badge_color: str
    rarity: str
    required_points: int
    tier: int = 1
    unlocked_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Reward:
    """Represents a national milestone reward."""
    reward_id: str
    title: str
    description: str
    reward_icon: str
    required_badges: int
    coupon_code: str
    unlocked_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TimelineEvent:
    """Chronological event entry in the user's Passport Timeline."""
    timeline_id: str
    title: str
    description: str
    event_type: str
    icon: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class StoreLoyalty:
    """Tracks user loyalty, engagement, and tier progression for a specific Regional Store."""
    store_id: str
    store_name: str
    region: str
    visits: int = 0
    purchases: int = 0
    wishlists: int = 0
    shares: int = 0
    reviews: int = 0
    points_earned: int = 0
    loyalty_level: str = "Bronze"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ActivityLog:
    """Logs individual point-earning interactions for auditing & user activity feed."""
    activity_id: str
    user_id: str
    action_type: str
    category: str
    region: str
    store_name: Optional[str]
    points_earned: int
    details: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UserPassport:
    """
    Core User Passport Data Model.
    Maintains total points as well as 3 independent point categories (Discovery, Engagement, Shopping).
    """
    user_id: str
    passport_points: int = 0  # Total Cumulative Points
    discovery_points: int = 0
    engagement_points: int = 0
    shopping_points: int = 0
    region_points: Dict[str, int] = field(default_factory=dict)
    badges: List[Dict[str, Any]] = field(default_factory=list)
    rewards: List[Dict[str, Any]] = field(default_factory=list)
    store_loyalty: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    timeline: List[Dict[str, Any]] = field(default_factory=list)
    purchase_history: List[Dict[str, Any]] = field(default_factory=list)
    activity_history: List[Dict[str, Any]] = field(default_factory=list)
    visited_regions: List[str] = field(default_factory=list)
    joined_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_activity: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
