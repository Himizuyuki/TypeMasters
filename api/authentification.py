from datetime import datetime, timedelta, timezone
from typing import Annotated
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from constants import JWT_ALGORITHM
from user import Username
from loguru import logger
from user_handler import USER_HANDLER

from constants import JWT_ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


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


def get_current_user(token: Annotated[str | None, Depends(oauth2_scheme)]):
    if token is None:
        logger.info("No token provided, defaulting to guest user")
        return None

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
            raise credentials_exception

    except InvalidTokenError:
        logger.info("Invalid token")
        raise credentials_exception
    user = USER_HANDLER.get_user_by_username(username)
    if not user:
        raise credentials_exception
    return user
