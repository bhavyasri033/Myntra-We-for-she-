"""
Configuration Module for Fashion Passport Engine (Upgraded)
============================================================
Contains configurable point rules mapped to point categories (Discovery, Engagement, Shopping),
Region Metadata, Rich Regional Badge definitions, National Rewards, Store Loyalty Tiers,
and Passport User Level thresholds.
"""

from typing import Dict, List, Any

# Point Category Rules
# Points are classified into: Discovery, Engagement, and Shopping
POINT_RULES: Dict[str, Dict[str, Any]] = {
    "VIEW_STORE": {"points": 1, "category": "discovery"},
    "VIEW_PRODUCT": {"points": 1, "category": "discovery"},
    "SEARCH_REGIONAL_STORE": {"points": 1, "category": "discovery"},
    "WISHLIST_PRODUCT": {"points": 2, "category": "engagement"},
    "SHARE_PRODUCT": {"points": 2, "category": "engagement"},
    "FOLLOW_STORE": {"points": 3, "category": "engagement"},
    "VERIFIED_REVIEW": {"points": 4, "category": "engagement"},
    "COMPLETE_PROFILE": {"points": 2, "category": "engagement"},
    "PURCHASE_PRODUCT": {"points": 5, "category": "shopping"}
}

# Rich Region Metadata for themed frontend UI cards & India Map visualization
REGION_METADATA: Dict[str, Dict[str, Any]] = {
    "Hyderabad": {
        "city": "Hyderabad",
        "state": "Telangana",
        "theme_color": "#8B5CF6",  # Royal Purple
        "landmark": "Charminar",
        "badge_name": "Hyderabad Explorer",
        "badge_icon": "hyderabad_explorer.png",
        "description": "Royal Zardozi, Pearls & Pochampally Handlooms"
    },
    "Bengaluru": {
        "city": "Bengaluru",
        "state": "Karnataka",
        "theme_color": "#10B981",  # Emerald Green
        "landmark": "Vidhana Soudha",
        "badge_name": "Bengaluru Trendsetter",
        "badge_icon": "bengaluru_trendsetter.png",
        "description": "Indie Fusion & Sustainable Boutique Hubs"
    },
    "Vijayawada": {
        "city": "Vijayawada",
        "state": "Andhra Pradesh",
        "theme_color": "#F59E0B",  # Sunburst Amber
        "landmark": "Prakasam Barrage",
        "badge_name": "Vijayawada Style Scout",
        "badge_icon": "vijayawada_stylescout.png",
        "description": "Mangalagiri Handloom & Kalamkari Weaves"
    },
    "Visakhapatnam": {
        "city": "Visakhapatnam",
        "state": "Andhra Pradesh",
        "theme_color": "#06B6D4",  # Ocean Cyan
        "landmark": "Dolphin's Nose",
        "badge_name": "Vizag Coastal Icon",
        "badge_icon": "vizag_coastal.png",
        "description": "Breezy Coastal Resortwear & Etikoppaka Craft"
    },
    "Indore": {
        "city": "Indore",
        "state": "Madhya Pradesh",
        "theme_color": "#EC4899",  # Malwa Rose
        "landmark": "Rajwada Palace",
        "badge_name": "Indore Textile Enthusiast",
        "badge_icon": "indore_textile.png",
        "description": "Maheshwari Tissue & Chanderi Silk Heritage"
    }
}

SUPPORTED_REGIONS: List[str] = list(REGION_METADATA.keys())

# Rich Badge Definitions with metadata (icon, color, rarity, tier)
REGIONAL_BADGES: Dict[str, List[Dict[str, Any]]] = {
    "Hyderabad": [
        {
            "badge_id": "hyd_explorer",
            "badge_name": "Hyderabad Explorer",
            "badge_description": "Explored regional royal heritage & weaves of Pearl City Hyderabad!",
            "badge_icon": "badge_hyd_explorer.svg",
            "badge_color": "#8B5CF6",
            "rarity": "Rare",
            "required_points": 25,
            "tier": 1
        },
        {
            "badge_id": "hyd_connoisseur",
            "badge_name": "Hyderabad Fashion Connoisseur",
            "badge_description": "Mastered the regal zardozi & silk collections of Hyderabad!",
            "badge_icon": "badge_hyd_master.svg",
            "badge_color": "#6D28D9",
            "rarity": "Epic",
            "required_points": 50,
            "tier": 2
        }
    ],
    "Bengaluru": [
        {
            "badge_id": "blr_trendsetter",
            "badge_name": "Bengaluru Trendsetter",
            "badge_description": "Discovered indie fusion and modern sustainable hubs in Bengaluru!",
            "badge_icon": "badge_blr_trendsetter.svg",
            "badge_color": "#10B981",
            "rarity": "Rare",
            "required_points": 25,
            "tier": 1
        },
        {
            "badge_id": "blr_icon",
            "badge_name": "Bengaluru Fashion Icon",
            "badge_description": "Ultimate style curator of Garden City's premier boutiques!",
            "badge_icon": "badge_blr_icon.svg",
            "badge_color": "#047857",
            "rarity": "Epic",
            "required_points": 50,
            "tier": 2
        }
    ],
    "Vijayawada": [
        {
            "badge_id": "vja_style_scout",
            "badge_name": "Vijayawada Style Scout",
            "badge_description": "Uncovered traditional Mangalagiri weaves and artisanal fashion of Vijayawada!",
            "badge_icon": "badge_vja_scout.svg",
            "badge_color": "#F59E0B",
            "rarity": "Rare",
            "required_points": 25,
            "tier": 1
        }
    ],
    "Visakhapatnam": [
        {
            "badge_id": "vizag_coastal_icon",
            "badge_name": "Vizag Coastal Icon",
            "badge_description": "Dipped into coastal vibes & breezy ethnic fusion from Visakhapatnam!",
            "badge_icon": "badge_vizag_icon.svg",
            "badge_color": "#06B6D4",
            "rarity": "Rare",
            "required_points": 25,
            "tier": 1
        }
    ],
    "Indore": [
        {
            "badge_id": "ind_textile_enthusiast",
            "badge_name": "Indore Textile Enthusiast",
            "badge_description": "Explored Maheshwari & Chanderi heritage craft traditions of Indore!",
            "badge_icon": "badge_ind_textile.svg",
            "badge_color": "#EC4899",
            "rarity": "Rare",
            "required_points": 25,
            "tier": 1
        }
    ]
}

# National Rewards based on cumulative badge milestones
NATIONAL_REWARDS: List[Dict[str, Any]] = [
    {
        "reward_id": "reward_1_badge",
        "title": "₹50 Regional Welcome Voucher",
        "description": "Unlock ₹50 off on your next purchase from any regional store.",
        "reward_icon": "reward_voucher_50.svg",
        "required_badges": 1,
        "coupon_code": "PASSPORT50"
    },
    {
        "reward_id": "reward_3_badges",
        "title": "₹100 Coupon",
        "description": "Unlock ₹100 off on regional fashion orders across India.",
        "reward_icon": "reward_coupon_100.svg",
        "required_badges": 3,
        "coupon_code": "PASSPORT100"
    },
    {
        "reward_id": "reward_5_badges",
        "title": "₹250 Coupon",
        "description": "Unlock ₹250 discount voucher for tier-1 regional icon stores.",
        "reward_icon": "reward_coupon_250.svg",
        "required_badges": 5,
        "coupon_code": "PASSPORT250"
    },
    {
        "reward_id": "reward_8_badges",
        "title": "Free Shipping",
        "description": "Enjoy lifetime Free Express Shipping on all regional artisan stores.",
        "reward_icon": "reward_freeship.svg",
        "required_badges": 8,
        "coupon_code": "FREESHIPREGIONAL"
    },
    {
        "reward_id": "reward_10_badges",
        "title": "Fashion Explorer Status",
        "description": "VIP Status: Early access to limited regional artisan drops & VIP events.",
        "reward_icon": "reward_vip_status.svg",
        "required_badges": 10,
        "coupon_code": "VIPEXPLORER"
    }
]

# Store Loyalty Tiers
STORE_LOYALTY_TIERS: List[Dict[str, Any]] = [
    {"level": "Bronze", "min_points": 0, "next_tier_points": 15},
    {"level": "Silver", "min_points": 15, "next_tier_points": 35},
    {"level": "Gold", "min_points": 35, "next_tier_points": 70},
    {"level": "Platinum", "min_points": 70, "next_tier_points": None}
]

# Passport User Levels
PASSPORT_LEVELS: List[Dict[str, Any]] = [
    {"level": 1, "title": "Novice Regional Explorer", "min_points": 0, "max_points": 25},
    {"level": 2, "title": "Regional Fashion Scout", "min_points": 26, "max_points": 60},
    {"level": 3, "title": "Regional Fashion Connoisseur", "min_points": 61, "max_points": 120},
    {"level": 4, "title": "National Fashion Icon", "min_points": 121, "max_points": 999999}
]
