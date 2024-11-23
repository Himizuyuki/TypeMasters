from datetime import datetime, timedelta, timezone
from typing import Annotated
from dotenv import load_dotenv
import os
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from authentification import create_access_token, get_current_user
from constants import JWT_ALGORITHM
from user import CreateUser, LoginForm, Username
from user_handler import USER_HANDLER, UserHandler
from loguru import logger

from pydantic import BaseModel

app = FastAPI()


load_dotenv()


class Token(BaseModel):
    access_token: str
    token_type: str


@app.post("/users")
def create_user(user: CreateUser):
    exception = USER_HANDLER.handle_create_user(
        username=user.username, password=user.password
    )
    if exception:
        return {"error": f"{str(exception)}"}
    return {"success": f"new user created with username {user.username}"}


@app.post("/token")
def get_access_token_for_login(login_form: LoginForm):
    user = USER_HANDLER.authenticate_user(
        username=login_form.username, password=login_form.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(
        access_token=create_access_token({"sub": user.username}), token_type="bearer"
    )


@app.get("/users/me")
def get_user(username: Annotated[Username, Depends(get_current_user)]):
    return username
