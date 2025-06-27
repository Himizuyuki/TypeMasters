from typing import TYPE_CHECKING
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from uuid import UUID, uuid4
from orm_user import ORMUser
from base import Base
import enum

class RaceState(enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"

class RaceVisibility(enum.Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"

class ORMRace(Base):
    __tablename__ = "race"

    id: Mapped[UUID] = mapped_column(String(36), primary_key=True, default=uuid4())
    state: Mapped[str] = mapped_column(Enum(RaceState, name='race_state'))
    visibility: Mapped[str] = mapped_column(Enum(RaceVisibility, name='race_visibility'))
    max_players: Mapped[int] = mapped_column(default=4)
    users: Mapped[ORMUser] = relationship()

