from mongoengine import Document, ReferenceField, DecimalField, StringField, DateTimeField
from .user import User
from .product import Product
from datetime import datetime

class Bid(Document):
    product = ReferenceField(Product, required=True)
    buyer = ReferenceField(User, required=True)
    seller = ReferenceField(User, required=True)
    amount = DecimalField(required=True)
    status = StringField(choices=('pending', 'accepted', 'rejected', 'counteroffer'), default='pending')
    counterOfferAmount = DecimalField() 
    timestamp = DateTimeField(default=datetime.utcnow)
