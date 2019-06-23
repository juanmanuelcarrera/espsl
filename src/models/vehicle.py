from mongoengine import *
from .parkingspot import ParkingSpot

class Vehicle(Document):
    area = FloatField(required=True, default=0)
    parking_spot = ReferenceField(ParkingSpot)