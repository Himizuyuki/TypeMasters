from datetime import datetime, timedelta, timezone
from typing import Annotated
from dotenv import load_dotenv
import os
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from constants import JWT_ALGORITHM
from user import CreateUser, LoginForm, Username
from user_handler import UserHandler
from loguru import logger

from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
load_dotenv()
user_handler = UserHandler()


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.environ["SECRET_KEY"], algorithm=JWT_ALGORITHM
    )
    return encoded_jwt


@app.post("/users")
def create_user(user: CreateUser):
    exception = user_handler.handle_create_user(
        username=user.username, password=user.password
    )
    if exception:
        return {"error": f"{str(exception)}"}
    return {"success": f"new user created with username {user.username}"}


@app.post("/token")
def get_access_token_for_login(login_form: LoginForm):
    user = user_handler.authenticate_user(
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


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, os.environ["SECRET_KEY"], algorithms=[JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            logger.info("username is none")
            raise credentials_exception

    except InvalidTokenError:
        logger.info("Invalid token")
        raise credentials_exception
    user = user_handler.get_user_by_username(username)
    if not user:
        logger.info("not user")
        raise credentials_exception
    return Username(username=username)


@app.get("/user")
def get_user(username: Annotated[Username, Depends(get_current_user)]):
    return username
