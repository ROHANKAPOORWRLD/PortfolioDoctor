from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.core.config import settings


engine = create_engine(settings.DB_URL, future=True)

local_session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db: Session = local_session()
    try:
        yield db
    finally:
        db.close()
