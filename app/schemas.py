from pydantic import BaseModel, EmailStr, conint
from datetime import date


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PersonalInformation(BaseModel):
    firstname: str
    lastname: str
    phone: str
    date_of_birth: date
    address: str


class PersonalInformationOut(PersonalInformation):
    user: UserOut

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    owner: UserOut


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool


class PostOut(BaseModel):
    Post: Post

    votes: int

    class Config:
        from_attributes = True


class VoteCreate(BaseModel):
    post_id: int
    dir: conint(le=1)
