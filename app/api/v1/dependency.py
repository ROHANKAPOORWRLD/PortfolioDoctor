from app.services.auth import AuthService
from app.repository.auth import AuthRepository

from app.services.portfolio import PortfolioService
from app.repository.portfolio import PortfolioRepository


def get_auth_service():
    auth_repo = AuthRepository()
    return AuthService(auth_repo)


def get_portfolio_service():
    portfolio_repo = PortfolioRepository()
    return PortfolioService(portfolio_repo)
