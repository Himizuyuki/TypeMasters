from typing import List
from typing import Optional
import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from uuid import UUID, uuid4

from base import Base


class ORMUser(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4())
    username: Mapped[str] = mapped_column(String(30))
    hashed_password: Mapped[str] = mapped_column(String(1000))
