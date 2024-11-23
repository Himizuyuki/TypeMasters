from uuid import UUID
from orm_user import ORMUser
from sqlalchemy.orm import Session
from sqlalchemy import insert, update
from orm_user_data import ORMPost


class PostRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_post_by_userid(self, post: str, user_id: UUID):
        self.session.execute(insert(ORMPost).values(user_id=user_id, post=post))
        self.session.commit()

    def set_password_hash_by_username(self, username: str, hashed_password: str):
        self.session.execute(
            update(ORMUser)
            .where(ORMUser.username == username)
            .values(hashed_password=hashed_password)
        )
        self.session.commit()
