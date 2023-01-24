from matplotlib import pyplot
from shapely.geometry import LineString, Point, Polygon
from shapely.figures import SIZE
import numpy as np

import helpers.geometry as geometry

class IntersectionDetector:
	def __init__(self):
		pass

    def detect(self, spot, vehicle):
        vehicle = Polygon(vehicle.shape)
        spot = Polygon(spot.shape)

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

            # (intersect, occupied_area)
            return True, final_intersection.area

        return False, 0