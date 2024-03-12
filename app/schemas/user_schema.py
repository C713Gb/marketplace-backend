from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    role: str 

class User(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True
        
class UserResponse(BaseModel):  # New class for user responses
    id: str
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True