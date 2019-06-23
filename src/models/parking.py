from mongoengine import *
from .parkinglevel import ParkingLevel

class Parking(Document):
    name = StringField(max_length=100)
    area = FloatField(required=True, default=0)
    occupiedArea = FloatField(required=True, default=0)
    state = StringField(max_length=30, default="EMPTY")
    levels = ListField(ReferenceField(ParkingLevel))