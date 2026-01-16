from uuid import UUID
from typing import List
from sqlalchemy.orm import Session

from app.repository.portfolio import PortfolioRepository
from app.schemas.portfolio import Share


class PortfolioService:
    def __init__(self, portfolio_repository: PortfolioRepository) -> None:
        self.portfolio_repository = portfolio_repository

    def portfolio_creation(
        self,
        db: Session,
        name: str,
        description: str,
        user_id: UUID,
        stocks: List[Share],
    ):
        pass
