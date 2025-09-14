from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from orm_user import ORMPost

from orm.base import Base


class ORMUser(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4())
    username: Mapped[str] = mapped_column(String(36))
    hashed_password: Mapped[str] = mapped_column(String(1000))
    race_id: Mapped[UUID] = mapped_column(
        String(36), ForeignKey("race.id"), nullable=True
    )
