from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from orm_user import User
import uuid
from constants import USERNAME_NAMESPACE
import os

engine = create_engine(f"mysql+pymysql://root:{os.environ["MYSQL_LOCAL_PASSWORD"]}@localhost/typemasters")

with Session(engine) as session:
    username = "ryan"
    user = User(id = uuid.uuid5(uuid.NAMESPACE_DNS, username), username = username, hashed_password = "1234", salt = "0000")
    session.add(user)
    session.commit()
