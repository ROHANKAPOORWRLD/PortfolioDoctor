from sqlalchemy.orm import Session
from app.repository.auth import AuthRepository
from app.core.security import verify_password, hash_password
from app.models.users import User
from app.exception.exceptions import UserAlreadyExists

# TODO: Implement Create Access Token
# def create_access_token(self, )


class AuthService:
    def __init__(self, repo: AuthRepository):
        self.auth_repo = repo

    def authenticate_user(self, db: Session, email: str, password: str) -> User | None:
        user = self.auth_repo.user_email_exists(db, email)
        if not user:
            return None
        if not user.is_active:
            return None
        if not user.hashed_password:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def register_user(self, db: Session, email: str, password: str) -> User:
        print(type(password))
        print(password)
        print(len(password))
        if self.auth_repo.user_email_exists(db, email):
            raise UserAlreadyExists("Bruh!")

        hashed_password = hash_password(password)
        return self.auth_repo.create_user(db, email, hashed_password)
