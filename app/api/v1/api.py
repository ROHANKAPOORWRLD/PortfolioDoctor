from fastapi import APIRouter

from .endpoints.auth.local import local_router
from .endpoints.auth.google import google_router
from .endpoints.portfolio.portfolio import portfolio_router
from .endpoints.portfolio.lookup import lookup_router

api_router = APIRouter(prefix="/v1/api")

api_router.include_router(local_router, tags=["Authentication"])
api_router.include_router(google_router, tags=["Authentication"])
api_router.include_router(portfolio_router, tags=["Assets Management"])
api_router.include_router(lookup_router, tags=["Assets Management"])
