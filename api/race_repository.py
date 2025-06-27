from typing import Optional, List
from orm_race import ORMRace, RaceState, RaceVisibility
from orm_user import ORMUser
from sqlalchemy.orm import Session
from sqlalchemy import Sequence, case, insert, select, func, text, update
from loguru import logger
from uuid import UUID, uuid4


class RaceRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_public_race_with_most_availability(self) -> ORMRace | None:
        querry = select(ORMRace).join(target = ORMUser, onclause = ORMRace.id == ORMUser.race_id) \
                .where(ORMRace.visibility == RaceVisibility.PUBLIC, ORMRace.state == RaceState.PENDING). \
                group_by(ORMRace.id, ORMRace.max_players).having(func.count(ORMUser.race_id) < ORMRace.max_players ) \
                .order_by(func.count(ORMUser.race_id)).limit(1)
        result = self.session.execute(querry).scalars().one_or_none()
        return result
    
    def join_race(self,user_id : UUID, race_id : UUID):
        query = update(ORMUser).where(ORMUser.id == user_id, ORMUser.race_id == None)\
    .values(race_id = race_id)
        result = self.session.execute(query)
        if result.rowcount == 0:
            self.session.rollback()
            raise Exception("You cannot join a race while you are already in a race.")
        self.session.commit()

    def create_and_join_race(self,user_id: UUID) -> UUID:
        result = self.session.execute(insert(ORMRace).values(id = uuid4()))
        orm_user = self.session.execute(select(ORMUser).where(ORMUser.id == user_id)).scalar()
        if orm_user and result.inserted_primary_key[0]:
            orm_user.race_id = result.inserted_primary_key[0]
        else:
            raise Exception("User not found.")
        self.session.commit()
        return result.inserted_primary_key



