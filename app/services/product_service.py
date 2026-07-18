from typing import List, Dict, Any, Optional
from bson import ObjectId

class ProductService:
    @staticmethod
    def parse_store_ids(store_ids_csv: Optional[str]) -> List[ObjectId]:
        """
        Utility parsing helper that splits a comma-separated query parameter string for store IDs,
        validates each token is a valid MongoDB ObjectId, and compiles them into a List of ObjectIds.
        Allows the frontend to query statelessly.
        """
        if not store_ids_csv:
            return []
        
        parsed = []
        for raw_id in store_ids_csv.split(","):
            clean_id = raw_id.strip()
            if clean_id and ObjectId.is_valid(clean_id):
                parsed.append(ObjectId(clean_id))
        return parsed

    @staticmethod
    async def get_dummy_product() -> Dict[str, Any]:
        return {
            "_id": ObjectId("60c72b2f9b1d8e1f5c6b4569"),
            "store_id": ObjectId("60c72b2f9b1d8e1f5c6b4567"),
            "name": "Traditional Silk Saree",
            "description": "Exquisite Kanchipuram silk saree with zari border",
            "price": 7500.00,
            "discount_price": 6999.00,
            "category": "Ethnic Wear",
            "sub_category": "Sarees",
            "sizes": ["FS"],
            "images": ["https://example.com/saree.jpg"],
            "stock": 10
        }

    @staticmethod
    async def get_products_by_store_ids(store_ids_csv: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves products list optionally filtered by a comma-separated query parameter string of store IDs.
        Stateless implementation mapping directly to react zustand selectedStores arrays.
        """
        store_object_ids = ProductService.parse_store_ids(store_ids_csv)
        
        # Seed dummy items mapping to specific store IDs for testing
        dummies = [
            {
                "_id": ObjectId("60c72b2f9b1d8e1f5c6b4569"),
                "store_id": ObjectId("60c72b2f9b1d8e1f5c6b4567"),
                "name": "Traditional Silk Saree",
                "description": "Exquisite Kanchipuram silk saree with zari border",
                "price": 7500.00,
                "discount_price": 6999.00,
                "category": "Ethnic Wear",
                "sub_category": "Sarees",
                "sizes": ["FS"],
                "images": ["https://example.com/saree.jpg"],
                "stock": 10
            },
            {
                "_id": ObjectId("60c72b2f9b1d8e1f5c6b457a"),
                "store_id": ObjectId("60c72b2f9b1d8e1f5c6b4568"),
                "name": "Designer Lehenga Choli",
                "description": "Premium silk designer lehenga with embroidery work",
                "price": 12000.00,
                "discount_price": 10500.00,
                "category": "Ethnic Wear",
                "sub_category": "Lehengas",
                "sizes": ["S", "M", "L"],
                "images": ["https://example.com/lehenga.jpg"],
                "stock": 5
            },
            {
                "_id": ObjectId("60c72b2f9b1d8e1f5c6b457b"),
                "store_id": ObjectId("6a5907bc7ebfa83801f378f9"),  # Matches Coimbatore Chennai Silks from seed summary!
                "name": "Organic Cotton Kurta",
                "description": "Made from genuine organic Coimbatore cotton",
                "price": 1800.00,
                "discount_price": 1500.00,
                "category": "Men's Wear",
                "sub_category": "Kurtas",
                "sizes": ["M", "L", "XL"],
                "images": ["https://example.com/cotton_kurta.jpg"],
                "stock": 20
            }
        ]
        
        if not store_object_ids:
            return dummies
            
        target_ids = set(store_object_ids)
        return [p for p in dummies if p["store_id"] in target_ids]
