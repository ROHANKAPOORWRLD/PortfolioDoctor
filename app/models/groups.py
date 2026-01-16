from datetime import datetime
import uuid

from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped
from app.db.base import Base


class Groups(Base):

    __tablename__ = "groups"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    member_id: Mapped[uuid.UUID] = mapped_column(UUID)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID)

class GroupMembers(Base):

    __tablename__="group_members"
    id: Mapped[uuid.UUID] = mapped_column()