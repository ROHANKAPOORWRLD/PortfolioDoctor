from app.services.auth import AuthService
from app.repository.auth import AuthRepository


def get_auth_service():
    auth_repo = AuthRepository()
    return AuthService(auth_repo)
