from mongoengine import Document, ReferenceField, DateTimeField, IntField
from .user import User
from .product import Product
from datetime import datetime
from .bid import Bid 

class Transaction(Document):
    bid = ReferenceField(Bid, required=True)
    timestamp = DateTimeField(default=datetime.utcnow)
