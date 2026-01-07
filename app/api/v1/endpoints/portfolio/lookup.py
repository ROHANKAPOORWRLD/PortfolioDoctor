from fastapi import APIRouter, HTTPException, status

from app.schemas.portfolio import ShareRequest, ShareResponse
from app.services.share import fetch_share_price

lookup_router = APIRouter()


@lookup_router.get("/stock/{symbol}", response_model=ShareResponse)
async def get_stock_price(symbol: str):
    try:
        return fetch_share_price(symbol)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Symbol not found. Please try again later",
        )
