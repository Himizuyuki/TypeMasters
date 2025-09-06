from dotenv import load_dotenv
load_dotenv()
import uuid
from race_handler import RACE_HANDLER
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from authentification import create_access_token, get_current_user
from user import CreateUser, LoginForm, User
from user_handler import USER_HANDLER
from pydantic import BaseModel
from loguru import logger

app = FastAPI()



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
def get_user(User: Annotated[User, Depends(get_current_user)]):
    return User


class Form(BaseModel):
    data: str

@app.post("/public-race")
def join_or_create_race(user: Annotated[User, Depends(get_current_user)]):
    if user:
        orm_user = USER_HANDLER.get_user_by_username(user.username)
        if orm_user:
            user_id = orm_user.id
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        user_id = uuid.uuid4()
    try:
        race_id = RACE_HANDLER.handle_public_race(user_id)
    except Exception as e:
        logger.error(f"Error joining or creating race: {e}")
        raise HTTPException(status_code = 503, detail="Temporary error joining/creating race; please try again",
        headers={"Retry-After": "5"})
    return {"race_id" : race_id}
