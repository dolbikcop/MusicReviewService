from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    user_id: int
    email: str
    username: str


class UserCreate(BaseModel):
    email: str
    password: str
    username: str

    model_config = ConfigDict(from_attributes=True)
