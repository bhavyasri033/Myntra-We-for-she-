from typing import List, Optional
from pydantic import BaseModel, Field
from app.utils.helpers import PyObjectId

class ProductBase(BaseModel):
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

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    store_id: Optional[PyObjectId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    discount_price: Optional[float] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    sizes: Optional[List[str]] = None
    images: Optional[List[str]] = None
    stock: Optional[int] = None

class ProductResponse(ProductBase):
    id: PyObjectId = Field(alias="_id")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "_id": "60c72b2f9b1d8e1f5c6b4569",
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
