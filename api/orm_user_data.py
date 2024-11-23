from typing import TYPE_CHECKING
import sqlalchemy
from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from uuid import UUID, uuid4
from base import Base

if TYPE_CHECKING:
    from orm_user import ORMUser


class ORMPost(Base):
    __tablename__ = "post"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4())
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    post: Mapped[str] = mapped_column(Text)
    time_generated: Mapped[str] = mapped_column(
        TIMESTAMP, default=sqlalchemy.func.now()
    )
    user: Mapped["ORMUser"] = relationship(back_populates="posts")
