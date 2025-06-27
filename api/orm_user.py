from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from orm_user import ORMPost
from base import Base


class ORMUser(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4())
    username: Mapped[str] = mapped_column(String(36))
    hashed_password: Mapped[str] = mapped_column(String(1000))
    race_id: Mapped[UUID] = mapped_column(String(36), ForeignKey("race.id"), nullable=True )
