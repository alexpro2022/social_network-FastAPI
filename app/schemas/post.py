from datetime import datetime as dt

from pydantic import BaseModel, Extra, Field, validator

from app.validators.post import is_text

from .user import UserRead


class PostCreate(BaseModel):
    title: str = Field(max_length=100, example='New post title.')
    content: str = Field(example='New post content.')

    @validator('title', 'content')
    def field_(cls, field):
        is_text(field)
        return field

    '''class Config:
        extra = Extra.forbid'''


class PostUpdate(BaseModel):
    title: str | None = Field(
        None, max_length=100, example='update for title.')
    content: str | None = Field(None, example='update for content.')

    @validator('title', 'content')
    def field_(cls, field):
        is_text(field)
        return field

    '''class Config:
        extra = Extra.forbid'''


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created: dt
    updated: dt | None = None
    likes: int
    dislikes: int
    author: UserRead

    class Config:
        orm_mode = True
