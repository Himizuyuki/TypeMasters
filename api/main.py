from dotenv import load_dotenv
load_dotenv()
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from post_handler import POST_HANDLER
from authentification import create_access_token, get_current_user
from user import CreateUser, LoginForm, User
from user_handler import USER_HANDLER
from pydantic import BaseModel

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


@app.post("/users/me/posts")
def create_user_data(post_form: Form, user: Annotated[User, Depends(get_current_user)]):
    try:
        user_id = USER_HANDLER.get_user_id_by_username(user.username)
        POST_HANDLER.add_post_by_user_id(post_form.data, user_id)
    except Exception:
        return {
            "error": "An error occured duing post creation. Please check your token, and the formatting of your post data."
        }
    shortened_post = post_form.data
    if len(post_form.data) > 100:
        shortened_post = post_form.data[:100] + "..."
    return {
        "sucess": f"Successfully created post:  '{shortened_post}'  for user {user.username}"
    }


@app.get("/users/me/posts")
def get_user_data(user: Annotated[User, Depends(get_current_user)]):
    posts = USER_HANDLER.get_posts_from_username(user.username)
    return {"posts": posts}
