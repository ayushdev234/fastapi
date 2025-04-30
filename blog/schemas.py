from pydantic import BaseModel
from typing import Optional, List

class BlogBase(BaseModel):
    title:str
    body:str
    user_id:int
class Blog(BlogBase):
    class config:
        orm_mode=True

class user (BaseModel):
    name:str
    email:str
    password:str

class showuser(BaseModel):
    name:str
    email:str
    blogs:List[Blog]=[]
    # with orm_mode , pydantic Can accept ORM models (objects)
    #You're using orm_mode = True in the Pydantic model to allow it to work seamlessly with ORM (Object Relational Mapper) models, like SQLAlchemy objects.
    class config:
        orm_mode=True


class showblog(BaseModel):
    title: str
    body: str
    id:int
    user_id:int
    creator:showuser

    class Config:
        orm_mode = True  # Important: Tells Pydantic to treat the ORM model as a dict


class Login(BaseModel):
    username:str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None