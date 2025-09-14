from pydantic import BaseModel


class User(BaseModel):
    username: str


class LoginForm(User):
    password: str


class CreateUser(User):
    password: str


class Username(BaseModel):
    username: str
