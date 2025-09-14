from typing import Optional
from orm.orm_user import ORMUser
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update
from loguru import logger
from user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_username(self, username: str) -> Optional[ORMUser]:
        orm_user = (
            self.session.execute(select(ORMUser).where(ORMUser.username == username))
            .scalars()
            .one_or_none()
        )
        return orm_user

    def add_user(self, user: ORMUser):
        self.session.add(user)
        self.session.commit()

    def set_password_hash_by_username(self, username: str, hashed_password: str):
        self.session.execute(
            update(ORMUser)
            .where(ORMUser.username == username)
            .values(hashed_password=hashed_password)
        )
        self.session.commit()
