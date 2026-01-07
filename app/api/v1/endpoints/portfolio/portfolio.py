from fastapi import APIRouter
from app.schemas.portfolio import PortfolioCreationRequest, PortfolioCreationResponse
portfolio_router = APIRouter()

@portfolio_router.post("/create-portfolio", response_model=PortfolioCreationResponse)
def create_portolio(data: PortfolioCreationRequest):
    pass