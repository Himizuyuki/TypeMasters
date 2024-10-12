from pydantic import BaseModel, field_validator

class User(BaseModel):
    username: str
    password: str
