from mongoengine import *
from shapely.geometry import Polygon

import helpers.geometry as geometry

class ParkingSpot(Document):
    location = StringField(max_length=100)
    tipe = StringField(max_length=100, default="NORMAL")
    area = FloatField(required=True, default=0)
    occupiedArea = FloatField(required=True, default=0)
    state = StringField(max_length=30, default="EMPTY")
    shape = ListField()

    # Check if vehicle is in a spot
    def intersect(self, vehicle_points):
        vehicle = Polygon(vehicle)
        spot = Polygon(self.shape)
        return vehicle.intersects(spot)

    # Check if vehicle is in a spot
    def check_vehicle(self, vehicle_points):
        vehicle = Polygon(vehicle_points)
        spot = Polygon(self.shape)
        
        if vehicle.intersects(spot):
            intersection = vehicle.intersection(spot)
            
            # left-most and right-most points of intersection
            left_point = geometry.get_left_point(intersection.boundary.coords)[0]
            right_point = geometry.get_right_point(intersection.boundary.coords)[0]

            # top-most and bottom-most points of spot
            top_point = geometry.get_top_point(spot.boundary.coords)[1]
            bottom_point = geometry.get_bottom_point(spot.boundary.coords)[1]

            # final intersection
            final_intersection = Polygon([
                (left_point, top_point), 
                (left_point, bottom_point),
                (right_point, bottom_point),
                (right_point, top_point)
            ])

            final_intersection = [
                (left_point, top_point), 
                (left_point, bottom_point),
                (right_point, bottom_point),
                (right_point, top_point)
            ]

            #print(self.to_json())
            #print(final_intersection)
            #print(final_intersection.area)

            return final_intersection
        
