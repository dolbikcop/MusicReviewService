from pydantic import BaseModel, ConfigDict


def UserCreate(BaseModel):
    email: str
    password: str
    username: str

    model_config = ConfigDict(from_attributes=True)

