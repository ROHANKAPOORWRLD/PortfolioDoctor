from typing import Literal, List
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime, timezone


class Share(BaseModel):
    symbol: str
    price: float
    quantity: int


class ShareRequest(BaseModel):
    symbol: str


class ShareResponse(BaseModel):
    name: str
    symbol: str | None
    price: float
    currency: Literal["INR"] = "INR"
    as_of: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PortfolioCreationRequest(BaseModel):
    name: str
    descreption: str
    user_id: UUID
    stocks: List[Share]

class PortfolioCreationResponse(BaseModel):
    success: str
    id: UUID