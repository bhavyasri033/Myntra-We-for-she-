"""
Main Demo Runner for Fashion Passport Backend Engine (Upgraded)
================================================================
Simulates 20+ user interactions across regional fashion icon stores,
demonstrating 3 point scores (Discovery, Engagement, Shopping), Store Loyalty level ups,
Chronological Timeline events, Recommendation Engine, India Map Status, and JSON dashboard output.
"""

import sys
import json

# Ensure UTF-8 output encoding for cross-platform terminal compatibility
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from passport_engine import PassportEngine
from recommendation_engine import PassportRecommendationEngine


def print_header(title: str):
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)


def print_step(step_num: int, action_title: str, response: dict):
    print(f"\n[Step {step_num:02d}] Action: {action_title}")
    print(f"  + Points Earned     : +{response['points_earned']} [{response['category'].upper()}]")
    print(f"  + Total Passport Pts: {response['total_passport_points']} "
          f"(Discovery: {response['discovery_points']}, "
          f"Engagement: {response['engagement_points']}, "
          f"Shopping: {response['shopping_points']})")

    if response.get("newly_unlocked_badges"):
        for b in response["newly_unlocked_badges"]:
            print(f"  🎉 BADGE UNLOCKED!  : [{b['region']}] {b['badge_name']} ({b['rarity']}) (Req: {b['required_points']} pts)")

    if response.get("newly_unlocked_rewards"):
        for r in response["newly_unlocked_rewards"]:
            print(f"  🎁 REWARD UNLOCKED! : {r['title']} (Coupon: {r['coupon_code']})")


def run_demo():
    print_header("FASHION PASSPORT ENGINE - PRODUCTION SIMULATION DEMO")

    # Initialize Engine & Recommendation Helper
    passport_service = PassportEngine()
    recommender = PassportRecommendationEngine(repository=passport_service.repository)
    user_id = "USER_MYNTRA_99"

    print(f"Initialized Fashion Passport Session for User: {user_id}\n")

    # 20+ User Activities across 3 Regions & Regional Stores
    activities = [
        # --- PHASE 1: User Onboarding & Hyderabad Regional Icon Stores ---
        ("Complete Profile", lambda: passport_service.complete_profile(user_id)),
        ("View Store: Charminar Heritage Silks (Hyderabad)", lambda: passport_service.view_store(user_id, "Charminar Heritage Silks", "Hyderabad")),
        ("Follow Store: Charminar Heritage Silks (Hyderabad)", lambda: passport_service.follow_store(user_id, "Charminar Heritage Silks", "Hyderabad")),
        ("View Product: Royal Zardozi Silk Saree (Hyderabad)", lambda: passport_service.view_product(user_id, "PROD_HYD_01")),
        ("Wishlist Product: Royal Zardozi Silk Saree (Hyderabad)", lambda: passport_service.wishlist_product(user_id, "PROD_HYD_01")),
        ("Share Product: Royal Zardozi Silk Saree (Hyderabad)", lambda: passport_service.share_product(user_id, "PROD_HYD_01")),
        ("Purchase Product: Royal Zardozi Silk Saree (Hyderabad)", lambda: passport_service.purchase_product(user_id, "PROD_HYD_01")),
        ("Review Product: Royal Zardozi Silk Saree (Hyderabad)", lambda: passport_service.review_product(user_id, "PROD_HYD_01", is_verified=True)),
        ("Wishlist Product: Handcrafted Pearl Nizam Sherwani (Hyderabad)", lambda: passport_service.wishlist_product(user_id, "PROD_HYD_02")),
        ("Purchase Product: Handcrafted Pearl Nizam Sherwani (Hyderabad)", lambda: passport_service.purchase_product(user_id, "PROD_HYD_02")),
        ("View Store: Pochampally Weaves Hub (Hyderabad)", lambda: passport_service.view_store(user_id, "Pochampally Weaves Hub", "Hyderabad")),
        ("Purchase Product: Telia Rumal Designer Kurta (Hyderabad)", lambda: passport_service.purchase_product(user_id, "PROD_HYD_03")),

        # --- PHASE 2: Bengaluru Regional Icon Stores ---
        ("View Store: Indiranagar Sustainable Studio (Bengaluru)", lambda: passport_service.view_store(user_id, "Indiranagar Sustainable Studio", "Bengaluru")),
        ("Follow Store: Indiranagar Sustainable Studio (Bengaluru)", lambda: passport_service.follow_store(user_id, "Indiranagar Sustainable Studio", "Bengaluru")),
        ("View Product: Eco-Linen Indie Trench Jacket (Bengaluru)", lambda: passport_service.view_product(user_id, "PROD_BLR_01")),
        ("Wishlist Product: Eco-Linen Indie Trench Jacket (Bengaluru)", lambda: passport_service.wishlist_product(user_id, "PROD_BLR_01")),
        ("Share Product: Eco-Linen Indie Trench Jacket (Bengaluru)", lambda: passport_service.share_product(user_id, "PROD_BLR_01")),
        ("Purchase Product: Eco-Linen Indie Trench Jacket (Bengaluru)", lambda: passport_service.purchase_product(user_id, "PROD_BLR_01")),
        ("Review Product: Eco-Linen Indie Trench Jacket (Bengaluru)", lambda: passport_service.review_product(user_id, "PROD_BLR_01", is_verified=True)),
        ("Wishlist Product: Kanjeevaram Fusion Crop Top Set (Bengaluru)", lambda: passport_service.wishlist_product(user_id, "PROD_BLR_02")),
        ("Share Product: Kanjeevaram Fusion Crop Top Set (Bengaluru)", lambda: passport_service.share_product(user_id, "PROD_BLR_02")),
        ("Purchase Product: Kanjeevaram Fusion Crop Top Set (Bengaluru)", lambda: passport_service.purchase_product(user_id, "PROD_BLR_02")),

        # --- PHASE 3: Vijayawada Regional Icon Stores ---
        ("View Store: Krishna River Loom Crafts (Vijayawada)", lambda: passport_service.view_store(user_id, "Krishna River Loom Crafts", "Vijayawada")),
        ("Follow Store: Krishna River Loom Crafts (Vijayawada)", lambda: passport_service.follow_store(user_id, "Krishna River Loom Crafts", "Vijayawada")),
        ("Wishlist Product: Mangalagiri Cotton Handloom Saree (Vijayawada)", lambda: passport_service.wishlist_product(user_id, "PROD_VJA_01")),
        ("Share Product: Mangalagiri Cotton Handloom Saree (Vijayawada)", lambda: passport_service.share_product(user_id, "PROD_VJA_01")),
        ("Purchase Product: Mangalagiri Cotton Handloom Saree (Vijayawada)", lambda: passport_service.purchase_product(user_id, "PROD_VJA_01")),
        ("Review Product: Mangalagiri Cotton Handloom Saree (Vijayawada)", lambda: passport_service.review_product(user_id, "PROD_VJA_01", is_verified=True)),
        ("Wishlist Product: Kalamkari Hand-printed Dupatta (Vijayawada)", lambda: passport_service.wishlist_product(user_id, "PROD_VJA_02")),
        ("Share Product: Kalamkari Hand-printed Dupatta (Vijayawada)", lambda: passport_service.share_product(user_id, "PROD_VJA_02")),
        ("Purchase Product: Kalamkari Hand-printed Dupatta (Vijayawada)", lambda: passport_service.purchase_product(user_id, "PROD_VJA_02"))
    ]

    for idx, (title, func) in enumerate(activities, 1):
        res = func()
        print_step(idx, title, res)

    # Output Recommendations
    print_header("PASSPORT RECOMMENDATION ENGINE OUTPUTS")
    next_region_rec = recommender.recommend_next_region(user_id)
    store_recs = recommender.recommend_stores(user_id, limit=2)
    badge_rec = recommender.recommend_badge(user_id)

    print("\n[Recommended Next Region]")
    print(json.dumps(next_region_rec, indent=2))

    print("\n[Recommended Regional Fashion Stores]")
    print(json.dumps(store_recs, indent=2))

    print("\n[Target Badge Recommendation]")
    print(json.dumps(badge_rec, indent=2))

    # Output Final Passport Summary Dashboard JSON
    print_header("FINAL PASSPORT SUMMARY DASHBOARD (Frontend JSON Payload)")
    final_summary = passport_service.get_passport(user_id)
    print(json.dumps(final_summary, indent=2))

    print_header("SIMULATION COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    run_demo()
