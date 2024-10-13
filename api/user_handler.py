from typing import Literal, Optional
from argon2 import PasswordHasher
from engine_factory import create_engine_default
from main import User
from sqlalchemy.orm import Session
from secrets import token_hex

from orm_user import ORMUser
from user_repository import UserRepository
import uuid
from exceptions import UsernameTakenException, UsernameTooLongException, UsernameTooShortException, WeakPasswordException
from string import ascii_lowercase, ascii_uppercase
from loguru import logger


ph = PasswordHasher()#TODO: This should be done in a seperate module


class UserHandler:

    def handle_create_user(self, user: User) -> Optional[str]:
        try:
            self.validate_user_info(user)
            db_engine = create_engine_default()
            with Session(db_engine) as session:
                user_repository = UserRepository(session)
                user_exists = user_repository.get_user_by_username(user.username)
                if not user_exists:
                    user_repository.add_user(self.user_to_orm(user))
                else:
                    raise UsernameTakenException
        except Exception as e:
            return(str(e))

    def authenticate_user(self, user: User) -> User | Literal[False]:
        db_engine = create_engine_default()
        with Session(db_engine) as session:
            user_repository = UserRepository(session)
            orm_user = user_repository.get_user_by_username(user.username)
            if not orm_user:
                return False
            if not ph.verify(orm_user.hashed_password, user.password):
                return False
            if ph.check_needs_rehash(orm_user.hashed_password):
                logger.info(f"Password for user {user.username} was rehashed")
                new_hash = ph.hash(user.password)
                user_repository.set_password_hash_by_username(user.username, new_hash)
        return user


    def change_password(self,username: str, old_password, new_password) -> bool:
        if not self.authenticate_user(User(username = username, password=old_password)):
            return False

        db_engine = create_engine_default()
        with Session(db_engine) as session:
            user_repository = UserRepository(session)

            user_repository.set_password_hash_by_username(username, ph.hash(new_password))
        return True

    def _user_to_orm(self,user: User) -> ORMUser:
        id = uuid.uuid4()

        hashed_password = ph.hash(user.password)
        return ORMUser(id = id, hashed_password = hashed_password, username = user.username)

    def _validate_user_info(self,user: User):
        self.validate_username(user.username)
        self.validate_password(user.password)

    def _validate_username(self,username :str):
        if len(username) > 36:
            raise UsernameTooLongException
        if len(username) < 3:
            raise UsernameTooShortException

    def _validate_password(self,password: str):
        DIGITS = {"1","2","3","4","5","6","7","8","9","0"}
        print(password)
        print(any(char in password for char in ascii_lowercase))
        if (any(char in password for char in ascii_lowercase)
            and any(char in password for char in ascii_uppercase)
            and any(char in password for char in DIGITS)
            and any(char not in DIGITS.union(set(ascii_lowercase).union(set(ascii_uppercase))) for char in password)
            and len(password) > 11):
            return
        raise WeakPasswordException
