from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str

class UserLogic(BaseModel):
    username: str
    password: str