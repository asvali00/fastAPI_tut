from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


# class Post(BaseModel):  # definiranje classe Post koje je ekstendirana (nasljeđuje) iz klase BaseModel - pydantic - automatska validacija podataka
#     title: str
#     content: str
#     published: bool = True  # defaults to True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config: # pošto je response sqlalchemy model podataka... moraš ga pretvoriti u dict jer pydantic zna samo raditi sa dict()
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # defaults to True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):  # pooonvno ćemo uz pomoć pydantica i validirati ono što vraćamo klijentu - ovo je ispravno jer ti se može dogoditi da vratiš klijentu nešto šta ne bi smio, npr. lozinku
    id: int
    created_at: datetime
    # owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class PostVoteResponse(BaseModel):
    Post: PostResponse
    likes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None



class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
