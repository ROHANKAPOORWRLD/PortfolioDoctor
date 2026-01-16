from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.portfolio import PortfolioCreationRequest, PortfolioCreationResponse
from app.api.v1.dependency import get_portfolio_service
from app.db.session import get_db

portfolio_router = APIRouter()
portfolio_service = get_portfolio_service()


@portfolio_router.post("/portfolios", response_model=PortfolioCreationResponse)
def create_portolio(data: PortfolioCreationRequest, db: Session = Depends(get_db)):
    portfolio_service.portfolio_creation(
        db,
        data.name,
        data.descreption,
        data.user_id,
        data.stocks,
    )
