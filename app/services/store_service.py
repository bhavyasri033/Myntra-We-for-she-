import math
from typing import List, Optional, Dict, Any
from bson import ObjectId
from database.database import get_database
from app.config import settings

class StoreService:
    @staticmethod
    def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two coordinates in km using the Haversine formula.
        """
        R = 6371.0  # Earth's radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    @staticmethod
    def calculate_distance_score(distance: float, radius: float) -> float:
        """
        Distance Score = max(0.0, (radius - distance) / radius)
        """
        if radius <= 0:
            return 0.0
        return max(0.0, (radius - distance) / radius)

    @staticmethod
    def calculate_final_score(normalized_trust: float, distance_score: float) -> float:
        """
        Final Score = w_trust * Normalized Trust Score + w_dist * Distance Score
        """
        w_trust = settings.RANKING_TRUST_WEIGHT
        w_dist = settings.RANKING_DISTANCE_WEIGHT
        return (w_trust * normalized_trust) + (w_dist * distance_score)

    @staticmethod
    def sort_stores(stores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sort stores by final_score (Descending).
        """
        return sorted(stores, key=lambda s: s.get("final_score", 0.0), reverse=True)

    @staticmethod
    async def get_all_stores() -> List[Dict[str, Any]]:
        db = get_database()
        cursor = db.stores.find()
        return await cursor.to_list(length=200)

    @staticmethod
    async def get_store_by_id(store_id: str) -> Optional[Dict[str, Any]]:
        db = get_database()
        if not ObjectId.is_valid(store_id):
            return None
        return await db.stores.find_one({"_id": ObjectId(store_id)})

    # ==========================================
    # SEARCH DISCOVERY ENGINE HELPER METHODS
    # ==========================================

    @staticmethod
    def normalize_query(query: str) -> str:
        """
        Normalize query string by removing surrounding padding and lowercasing.
        """
        return query.strip().lower()

    @staticmethod
    def search_store_name(name: str, query: str) -> float:
        """
        Calculate store name match score.
        Exact Match = 100 points, Substring Match = 50 points.
        """
        name_lower = name.lower()
        if name_lower == query:
            return 100.0
        elif query in name_lower:
            return 50.0
        return 0.0

    @staticmethod
    def search_city(city: str, query: str) -> float:
        """
        Calculate city match score (40 points if matched).
        """
        if query in city.lower():
            return 40.0
        return 0.0

    @staticmethod
    def search_state(state: str, query: str) -> float:
        """
        Calculate state match score (10 points if matched).
        """
        if query in state.lower():
            return 10.0
        return 0.0

    @staticmethod
    def search_category(categories: List[str], query: str) -> float:
        """
        Calculate category match score (30 points if matched).
        """
        if any(query in cat.lower() for cat in categories):
            return 30.0
        return 0.0

    @staticmethod
    def search_description(description: Optional[str], query: str) -> float:
        """
        Calculate description match score (20 points if matched).
        """
        if description and query in description.lower():
            return 20.0
        return 0.0

    @staticmethod
    def calculate_relevance_score(store: Dict[str, Any], query: str) -> float:
        """
        Calculate cumulative relevance match score using structured weights.
        """
        score = 0.0
        
        name = store.get("name", "")
        city = store.get("city", "")
        state = store.get("state", "")
        categories = store.get("categories", [])
        description = store.get("description", "")
        
        # 1. Exact or partial store name match
        score += StoreService.search_store_name(name, query)
        # 2. City match
        score += StoreService.search_city(city, query)
        # 3. Category match
        score += StoreService.search_category(categories, query)
        # 4. Description match
        score += StoreService.search_description(description, query)
        # 5. State match
        score += StoreService.search_state(state, query)
        
        # Fallback to keyword split evaluation for multi-term query checks
        if score == 0.0:
            words = [w for w in query.split() if w]
            if len(words) > 1:
                for word in words:
                    # Grant fractional points for separate word terms matches
                    if word in name.lower():
                        score += 30.0
                    if word in city.lower():
                        score += 25.0
                    if any(word in cat.lower() for cat in categories):
                        score += 20.0
                    if description and word in description.lower():
                        score += 5.0
                    if word in state.lower():
                        score += 2.0
                        
        return score

    @staticmethod
    def sort_search_results(
        stores: List[Dict[str, Any]],
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Sort results by Relevance (Descending), then Trust Score (Descending) and optionally Distance (Ascending).
        """
        def get_sort_key(s: Dict[str, Any]):
            rel_score = s.get("relevance_score", 0.0)
            trust = s.get("trust_score", 0.0)
            dist = s.get("distance_km", 0.0) if lat is not None and lon is not None else 0.0
            # Sort order priority:
            # 1. Relevance Score Descending (-rel_score)
            # 2. Trust Score Descending (-trust)
            # 3. Distance Ascending (dist)
            return (-rel_score, -trust, dist)

        return sorted(stores, key=get_sort_key)

    @staticmethod
    async def search_stores(
        query: str,
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Intelligent fashion search discovery across name, location, and description fields.
        """
        norm_query = StoreService.normalize_query(query)
        if not norm_query:
            return []
            
        db = get_database()
        cursor = db.stores.find()
        all_stores = await cursor.to_list(length=1000)
        
        matched_stores = []
        for store in all_stores:
            rel_score = StoreService.calculate_relevance_score(store, norm_query)
            if rel_score > 0:
                store_copy = dict(store)
                store_copy["relevance_score"] = rel_score
                
                # Optional distance computation if customer location is logged
                if lat is not None and lon is not None:
                    store_lat = store.get("latitude")
                    store_lon = store.get("longitude")
                    if store_lat is not None and store_lon is not None:
                        dist = StoreService.haversine(lat, lon, store_lat, store_lon)
                        store_copy["distance_km"] = round(dist, 2)
                        
                matched_stores.append(store_copy)
                
        return StoreService.sort_search_results(matched_stores, lat, lon)

    # Legacy method compatibility
    @staticmethod
    async def search_stores_by_name(query: str) -> List[Dict[str, Any]]:
        return await StoreService.search_stores(query)

    @staticmethod
    async def get_nearby_stores(lat: float, lon: float, radius_km: float) -> List[Dict[str, Any]]:
        db = get_database()
        cursor = db.stores.find()
        all_stores = await cursor.to_list(length=1000)

        nearby = []
        for store in all_stores:
            store_lat = store.get("latitude")
            store_lon = store.get("longitude")
            if store_lat is None or store_lon is None:
                continue
            
            dist = StoreService.haversine(lat, lon, store_lat, store_lon)
            if dist <= radius_km:
                store_copy = dict(store)
                store_copy["distance_km"] = round(dist, 2)
                nearby.append(store_copy)

        if not nearby:
            return []

        max_trust = max((s.get("trust_score", 0.0) for s in nearby), default=0.0)
        if max_trust <= 0:
            max_trust = 10.0

        for store in nearby:
            trust = store.get("trust_score", 0.0)
            norm_trust = trust / max_trust
            dist = store.get("distance_km", 0.0)
            dist_score = StoreService.calculate_distance_score(dist, radius_km)
            final_score = StoreService.calculate_final_score(norm_trust, dist_score)

            store["normalized_trust_score"] = round(norm_trust, 4)
            store["distance_score"] = round(dist_score, 4)
            store["final_score"] = round(final_score, 4)

        return StoreService.sort_stores(nearby)
