from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    product_id: int
    quantity: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):  # This might be used for internal operations or requests
    id: int
    buyer_id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class TransactionResponse(BaseModel):  # New class for transaction responses
    id: int
    product_id: int
    buyer_id: int
    quantity: int
    timestamp: datetime

    class Config:
        orm_mode = True
