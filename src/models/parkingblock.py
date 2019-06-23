from mongoengine import *
from helpers.mongo import mongo_to_dict
from .parkingspot import ParkingSpot

class ParkingBlock(Document):
    location = StringField(max_length=100)
    area = FloatField(required=True, default=0)
    occupiedArea = FloatField(required=True, default=0)
    state = StringField(max_length=30, default="EMPTY")
    shape = ListField()
    spots = ListField(ReferenceField(ParkingSpot))

    def to_dict(self):
        block = mongo_to_dict(self, ["spots"])
        spots = list(map(lambda x: mongo_to_dict(x), self.spots))
        block["spots"] = spots
        return block