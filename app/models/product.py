from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.utils.helpers import PyObjectId

class ProductDB(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    store_id: PyObjectId
    name: str
    description: Optional[str] = None
    price: float
    discount_price: Optional[float] = None
    category: str
    sub_category: Optional[str] = None
    sizes: List[str] = []
    images: List[str] = []
    stock: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "store_id": "60c72b2f9b1d8e1f5c6b4567",
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
        }
    }
