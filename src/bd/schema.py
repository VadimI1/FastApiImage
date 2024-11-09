from pydantic import BaseModel

class Name(BaseModel):
    name: str

class Id(BaseModel):
    id: int

class Update(BaseModel):
    id: int
    name: str

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

class UserAuth(BaseModel):

    email: str
    password: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
