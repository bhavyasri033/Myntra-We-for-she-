from typing import List, Optional
from pydantic import BaseModel, Field
from app.utils.helpers import PyObjectId

class StoreCardResponse(BaseModel):
    """
    Customer-facing response schema for rendering store cards.
    Excludes internal fields like trust_score, google_rating, and review_count.
    """
    id: PyObjectId = Field(
        alias="_id",
        description="The unique MongoDB ObjectId identifier of the store"
    )
    shopping_hub_id: Optional[str] = Field(
        default=None,
        description="String ID of the associated Shopping Hub"
    )
    name: str = Field(
        description="The commercial brand name of the regional retailer"
    )
    city: str = Field(
        description="City where the store outlet is located"
    )
    state: str = Field(
        description="State administrative region of the store location"
    )
    banner_image: Optional[str] = Field(
        default=None,
        description="Public URL pointing to the promotional banner of the store"
    )
    categories: List[str] = Field(
        description="Fashion category tags handled by the store (e.g. Sarees, Ethnic Wear)"
    )
    years_in_business: int = Field(
        description="Number of years the store has been active, demonstrating regional trust legacy"
    )
    is_verified: bool = Field(
        default=False,
        description="Indicates whether the store has been verified under Myntra's regional retailer onboarding program"
    )

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "_id": "60c72b2f9b1d8e1f5c6b4567",
                "name": "South India Shopping Mall",
                "city": "Hyderabad",
                "state": "Telangana",
                "banner_image": "https://example.com/banners/sism-hyd.png",
                "categories": ["Sarees", "Lehengas", "Ethnic Wear"],
                "years_in_business": 18,
                "is_verified": True
            }
        }
    }

class NearbyStoreResponse(StoreCardResponse):
    """
    Geographically discovered store card schema extending StoreCardResponse with distance in kilometers.
    Excludes internal fields like trust_score, google_rating, and review_count.
    """
    distance_km: float = Field(
        description="Calculated distance in kilometers from the customer's queried coordinates to the store"
    )

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "_id": "60c72b2f9b1d8e1f5c6b4567",
                "name": "South India Shopping Mall",
                "city": "Hyderabad",
                "state": "Telangana",
                "banner_image": "https://example.com/banners/sism-hyd.png",
                "categories": ["Sarees", "Lehengas", "Ethnic Wear"],
                "years_in_business": 18,
                "is_verified": True,
                "distance_km": 1.25
            }
        }
    }

class StoreDetailsResponse(StoreCardResponse):
    """
    Full profile response schema for a single trusted store.
    Includes location coordinates and address details. Excludes internal scoring parameters.
    """
    description: Optional[str] = Field(
        default=None,
        description="Detailed background narrative, heritage, and brand specialties"
    )
    address: str = Field(
        description="Physical street address details of the store outlet"
    )
    latitude: float = Field(
        description="Geographic latitude coordinate mapping"
    )
    longitude: float = Field(
        description="Geographic longitude coordinate mapping"
    )

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "_id": "60c72b2f9b1d8e1f5c6b4567",
                "name": "South India Shopping Mall",
                "city": "Hyderabad",
                "state": "Telangana",
                "banner_image": "https://example.com/banners/sism-hyd.png",
                "categories": ["Sarees", "Lehengas", "Ethnic Wear"],
                "years_in_business": 18,
                "is_verified": True,
                "description": "South India Shopping Mall offers an unmatched range of silk sarees, designer lehengas, and ethnic fashion.",
                "address": "Kothapet Cross Roads, Hyderabad, Telangana 500035",
                "latitude": 17.385044,
                "longitude": 78.486671
            }
        }
    }

# Backward compatibility mappings for other files/routers if needed
StoreResponse = StoreCardResponse
StoreNearbyResponse = NearbyStoreResponse
