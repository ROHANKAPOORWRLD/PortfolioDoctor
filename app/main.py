from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.api.v1.api import api_router

app = FastAPI()

app.include_router(router=api_router)


@app.get("/", tags=["Welcome"])
def hello():
    return "Welcome to the application"


@app.post(
    "/__danger/api/create-required-tables",
    description="Required only on first time setup. "
    "Important Note: This will delete the existing tables then it will create the tables again.",
    tags=["Setup"],
)
def create_required_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
