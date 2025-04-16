from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    name: str = Field(None, min_length=3)


class User(UserCreate):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str
