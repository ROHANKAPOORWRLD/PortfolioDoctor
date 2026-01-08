from sqlalchemy.orm import Session
from app.models.users import User


class AuthRepository:
    def user_email_exists(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def google_id_exists(self, db: Session, google_id: str) -> User | None:
        return db.query(User).filter(User.google_id == google_id).first()

    def add_google_id(self, db: Session, user: User, google_id: str) -> User:
        user.google_id = google_id
        db.commit()
        db.refresh(user)
        return user

    def create_user(
        self,
        db: Session,
        email: str,
        hashed_password: str | None = None,
        google_id: str | None = None,
    ) -> User:
        user = User(email=email, hashed_password=hashed_password, google_id=google_id)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
