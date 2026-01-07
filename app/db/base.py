from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.users import User
from app.models.portfolio import Portfolio