from mongoengine import Document, ReferenceField, DateTimeField, IntField
from .user import User
from .product import Product
from datetime import datetime

class Transaction(Document):
    buyer = ReferenceField(User, required=True)
    product = ReferenceField(Product, required=True)
    timestamp = DateTimeField(default=datetime.utcnow)
    quantity = IntField(required=True)
