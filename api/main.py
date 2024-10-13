from typing import Union
from dotenv import load_dotenv, dotenv_values
import os
from fastapi import FastAPI
from user import LoginForm, User
from user_handler import UserHandler, UsernameTakenException
from secret import Secret
from loguru import logger

app = FastAPI()
from pydantic import BaseModel

load_dotenv()
user_handler = UserHandler()


class RaceResult(BaseModel):
    char_and_time: list[str]

@app.get("/text-to-type")
def get_text_to_type(item_id: int, q: Union[str, None] = None):
    #TODO: link to another function that calls the db
    return {}

@app.post("/users")
def create_user(user: User):
    exception = user_handler.handle_create_user(user)
    if exception:
        return {"error" : f"{str(exception)}"}
    return {"success" : f"new user created with username {user.username}"}

@app.post("/result")
def store_result(result: RaceResult):
    return {}

@app.get("/secret")
def get_secret():
    return Secret.get_secret()


@app.post("/token")
def get_access_token_for_login(user: User):
    user = user_handler.authenticate_user(user)
    if user:
        authenticated = True
    else:
        authenticated = False
    return {"Authenticated" : authenticated}

@app.post("/change_password")
def change_password(dict : dict):
    return {"success" : user_handler.change_password(dict.username, dict.old_password, dict.new_password)}
