from typing import Literal, Optional
from argon2 import PasswordHasher
from loguru import logger
from user import User
from engine_factory import create_engine_default
from sqlalchemy.orm import Session

from orm.orm_user import ORMUser
from user_repository import UserRepository
import uuid
from exceptions import (
    UsernameTakenException,
    UsernameTooLongException,
    UsernameTooShortException,
    WeakPasswordException,
)
from string import ascii_lowercase, ascii_uppercase


ph = PasswordHasher()  # TODO: This should be done in a seperate module


class UserHandler:
    # create engine on initializzation
    def __init__(self):
        self.db_engine = create_engine_default()

    def get_user_by_username(self, username: str) -> ORMUser | None:
        with Session(self.db_engine) as session:
            user_repository = UserRepository(session)
            orm_user = user_repository.get_user_by_username(username)
            if not orm_user:
                return None
            return orm_user

    def handle_create_user(self, username: str, password: str) -> Optional[str]:
        try:
            self._validate_user_info(username, password)
            with Session(self.db_engine) as session:
                user_repository = UserRepository(session)
                user_exists = user_repository.get_user_by_username(username)
                if not user_exists:
                    user_repository.add_user(self._user_to_orm(username, password))
                else:
                    raise UsernameTakenException
        except Exception as e:
            logger.info(
                f"User creation failed: {e}"
            )  # TODO: Don't dump the exception, create an alias
            return str(e)  # TODO: Don't dump the exception, create an alias
        return None

    def authenticate_user(self, username: str, password: str) -> User | Literal[False]:
        with Session(self.db_engine) as session:
            user_repository = UserRepository(session)
            try:
                orm_user = user_repository.get_user_by_username(username)
                if not orm_user:
                    return False
                ph.verify(orm_user.hashed_password, password)
                if ph.check_needs_rehash(orm_user.hashed_password):
                    new_hash = ph.hash(password)
                    user_repository.set_password_hash_by_username(username, new_hash)
            except Exception as e:
                logger.info(
                    f"Authentification failed: {e} "
                )  # TODO: Don't dump the exception, create an alias
                return False

        return User(username=username)

    def change_password(self, username: str, old_password, new_password) -> bool:
        if not self.authenticate_user(username=username, password=old_password):
            return False

        with Session(self.db_engine) as session:
            user_repository = UserRepository(session)
            user_repository.set_password_hash_by_username(
                username, ph.hash(new_password)
            )
        return True

    def _user_to_orm(self, username, password) -> ORMUser:
        hashed_password = ph.hash(password)
        return ORMUser(hashed_password=hashed_password, username=username)

    def _validate_user_info(self, username: str, password: str):
        self._validate_username(username)
        self._validate_password(password)

    def _validate_username(self, username: str):
        if len(username) > 36:
            raise UsernameTooLongException
        if len(username) < 3:
            raise UsernameTooShortException

    def _validate_password(self, password: str):
        DIGITS = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0"}
        if (
            any(char in password for char in ascii_lowercase)
            and any(char in password for char in ascii_uppercase)
            and any(char in password for char in DIGITS)
            and any(
                char
                not in DIGITS.union(set(ascii_lowercase).union(set(ascii_uppercase)))
                for char in password
            )
            and len(password) > 11
        ):
            return
        raise WeakPasswordException

    def get_user_id_by_username(self, username: str) -> uuid.UUID:
        with Session(self.db_engine) as session:
            user_repository = UserRepository(session)
            orm_user = user_repository.get_user_by_username(username)
            if not orm_user:
                raise ValueError("User not found")
            return orm_user.id

    def get_posts_from_username(self, username):
        with Session(self.db_engine) as session:
            user_repository = UserRepository(session)
            orm_user = user_repository.get_user_by_username(username)
            return orm_user.posts

    def create_guest_user(self) -> ORMUser:
        with Session(self.db_engine) as session:
            user_repository = UserRepository(session)
            guest_user = ORMUser(username="guest", hashed_password=ph.hash("guest"))
            user_repository.add_user(guest_user)
            return guest_user

USER_HANDLER = UserHandler()
