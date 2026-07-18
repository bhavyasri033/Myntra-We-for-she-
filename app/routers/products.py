from fastapi import APIRouter, Query, status
from typing import List, Optional
from app.schemas.product import ProductResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/test")
async def test_endpoint():
    return {"message": "Products Router Working"}

@router.get("", response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
async def get_products(
    store_ids: Optional[str] = Query(
        None,
        description="Comma-separated list of store ObjectIds (e.g. '60c72b2f9b1d8e1f5c6b4567,60c72b2f9b1d8e1f5c6b4568'). "
                    "Note: Store selection is managed statelessly in the React frontend (e.g., in Zustand state) "
                    "and never saved to the MongoDB database. The backend simply filters products statelessly matching this parameter."
    )
):
    """
    Retrieve products. Optionally filter by a list of selected store IDs.
    
    **Stateless Frontend Alignment Note:**
    - Store selection is maintained entirely in the client UI state.
    - Pass selected store IDs as a comma-separated query string (`store_ids=id1,id2,id3`).
    - If empty, all products from all stores are retrieved (default browse catalog).
    """
    return await ProductService.get_products_by_store_ids(store_ids)
