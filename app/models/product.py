from mongoengine import Document, StringField, FloatField, ReferenceField
from .user import User

class Product(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    price = FloatField(required=True)
    seller = ReferenceField(User, required=True)
