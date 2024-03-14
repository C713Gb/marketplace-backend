from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    product_id: str

class TransactionCreate(BaseModel):
    bid_id: str

class Transaction(TransactionBase):
    id: str  
    buyer_id: str
    seller_id: str
    timestamp: datetime

    class Config:
        orm_mode = True

class TransactionResponse(BaseModel):
    id: str  
    bid_id: str 
    timestamp: datetime

    class Config:
        orm_mode = True