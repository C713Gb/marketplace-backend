from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BidBase(BaseModel):
    product_id: str
    amount: float

class BidCreate(BidBase):
    pass

class BidUpdate(BaseModel):
    amount: Optional[float] = None
    status: Optional[str] = None

class BidResponse(BaseModel):
    id: str
    product_id: str
    buyer_id: str
    seller_id: str
    amount: float
    status: str
    timestamp: datetime

    class Config:
        orm_mode = True
