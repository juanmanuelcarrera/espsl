import numpy as np
from shapely.geometry import Polygon

def nearest_points(points, point, distance = 40):
    #points = np.asarray(points)
    distances = np.sum((points - point)**2, axis=1)
    distances = np.absolute(np.sqrt(distances))
    return [i for i, dist in enumerate(distances) if dist < distance]

def medium_point(points):
    return np.around(np.mean(points, axis=0)).astype(int)

def simplify_contour(contour):
    processed_points = []
    simple_contour = np.array([])

    for i, point in enumerate(contour):
        if i not in processed_points:
            npoints = nearest_points(contour, point)
            mp = np.array([medium_point(np.take(contour, npoints, 0))])
            simple_contour = mp if simple_contour.size == 0 else np.append(simple_contour, mp, 0)
            processed_points += npoints

    return simple_contour

def sort_points_ttb(points):
    pts = np.array([list(point) for point in points])
    return pts[np.argsort(pts[:, 1]), :]

def get_top_point(points):
    return sort_points_ttb(points)[0]

def get_bottom_point(points):
    return sort_points_ttb(points)[-1]

def sort_points_ltr(points):
    pts = np.array([list(point) for point in points])
    return pts[np.argsort(pts[:, 0]), :]

def get_left_point(points):
    return sort_points_ltr(points)[0]

def get_right_point(points):
    return sort_points_ltr(points)[-1]

def sort_points_ttb(points):
    pts = np.array([list(point) for point in points])
    return pts[np.argsort(pts[:, 1]), :]

def get_top_point(points):
    return sort_points_ttb(points)[0]

def get_bottom_point(points):
    return sort_points_ttb(points)[0]

def sort_points_ltr(points):
    pts = np.array([list(point) for point in points])
    return pts[np.argsort(pts[:, 0]), :]

def get_left_point(points):
    return sort_points_ltr(points)[0]

def get_right_point(points):
    return sort_points_ltr(points)[-1]

def intersection(spot_shape, vehicle_shape):
    vehicle = Polygon(vehicle_shape)
    spot = Polygon(spot_shape)
    if vehicle.intersects(spot):
        intersection = vehicle.intersection(spot)

        # left-most and right-most points of intersection
        left_point = get_left_point(intersection.boundary.coords)[0]
        right_point = get_right_point(intersection.boundary.coords)[0]

        # top-most and bottom-most points of spot
        top_point = get_top_point(spot.boundary.coords)[1]
        bottom_point = get_bottom_point(spot.boundary.coords)[1]

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