
from uuid import UUID
from engine_factory import create_engine_default
from sqlalchemy.orm import Session
from race_repository import RaceRepository


class RaceHandler:
    def __init__(self):
        self.db_engine = create_engine_default()

    def handle_public_race(self, user_id: UUID):
        with Session(self.db_engine) as session:
            race_repository = RaceRepository(session)
            if (race := race_repository.get_public_race_with_most_availability()):
                race_id: UUID = race.id
                race_repository.join_race(user_id, race_id)
            else:
                race_id = race_repository.create_and_join_race(user_id)
            return race_id

RACE_HANDLER = RaceHandler()
