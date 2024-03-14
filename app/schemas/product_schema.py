from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    price: float

class ProductCreate(ProductBase):
    seller_id: str

class Product(ProductBase):  # This might be used for internal operations
    id: str
    seller_id: str

    class Config:
        orm_mode = True
        
class UserResponse(BaseModel):
    id: str
    username: str
    email: str

class ProductResponse(BaseModel):  # New class for product responses
    id: str
    name: str
    description: str
    price: float
    seller: UserResponse

    class Config:
        orm_mode = True
