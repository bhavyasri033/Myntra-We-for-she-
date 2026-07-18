from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Union
from app.schemas.store import StoreResponse, StoreNearbyResponse, StoreDetailsResponse
from app.services.store_service import StoreService

router = APIRouter(prefix="/stores", tags=["stores"])

@router.get("", response_model=List[StoreResponse], status_code=status.HTTP_200_OK)
async def get_stores():
    """
    Get all trusted regional stores.
    """
    return await StoreService.get_all_stores()

@router.get("/search", response_model=List[Union[StoreNearbyResponse, StoreResponse]], status_code=status.HTTP_200_OK)
async def search_stores(query: str, latitude: Optional[float] = None, longitude: Optional[float] = None):
    """
    Search stores by store name, city, state, categories or description with relevance ranking.
    """
    return await StoreService.search_stores(query, latitude, longitude)

@router.get("/nearby", response_model=List[StoreNearbyResponse], status_code=status.HTTP_200_OK)
async def get_nearby_stores(latitude: float, longitude: float, radius: float):
    """
    Find stores within the given radius (in km) sorted by Trust Score (descending) and Distance (ascending).
    """
    return await StoreService.get_nearby_stores(latitude, longitude, radius)

@router.get("/{id}", response_model=StoreDetailsResponse, status_code=status.HTTP_200_OK)
async def get_store_by_id(id: str):
    """
    Get a single trusted store by its MongoDB ObjectId.
    """
    store = await StoreService.get_store_by_id(id)
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Store not found with id {id}"
        )
    return store
