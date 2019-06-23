from mongoengine import *

from .parkingblock import ParkingBlock

class ParkingLevel(Document):
    level = IntField(required=True, default=1)
    priority = IntField(required=True, default=0)
    area = FloatField(required=True, default=0)
    occupiedArea = FloatField(required=True, default=0)
    state = StringField(max_length=30, default="EMPTY")
    blocks = ListField(ReferenceField(ParkingBlock))