from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):  # This might be used for internal operations
    id: int
    seller_id: int

    class Config:
        orm_mode = True

class ProductResponse(BaseModel):  # New class for product responses
    id: int
    name: str
    description: str
    price: float
    seller_id: int

    class Config:
        orm_mode = True
