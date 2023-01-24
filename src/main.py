import settings
import numpy as np
import cv2
import random

from globals.constants import PARKING_SLOTS

from helpers.parking import draw_parking

from modules.parkingspotdetector import ParkingSpotDetector
from modules.motiondetector import MotionDetector
from modules.vehicle_detector.vehicledetector import VehicleDetectorConfig, detect
from mrcnn import model as modellib, utils

from models.parking import Parking
from models.parkinglevel import ParkingLevel
from models.parkingblock import ParkingBlock
from models.parkingspot import ParkingSpot

from shapely.geometry import Polygon
from shapely.ops import unary_union
import pyproj
from shapely.geometry import shape
from shapely.ops import transform
from functools import partial

import helpers.geometry as geometry

import nodes.server

def parkig_spot_detector_test():
    image_path = '../images/img_1389_crop_empty.jpg'

    psd = ParkingSpotDetector()
    print(psd.detect(image_path))


def motion_detector_test():
    imgs = [
        '../images/motion_1_1.jpg',
        '../images/motion_2_1.jpg',
        '../images/motion_3_1.jpg',
        '../images/motion_4_1.jpg'
    ]

    mtd = MotionDetector()

    for img in imgs:
        print(mtd.detect(cv2.imread(img)))

def drawing_parking_test():
    parking = Parking.objects.get(name="parking")
    draw_parking(parking)

def vehicle_detector_test():
    class InferenceConfig(VehicleDetectorConfig):
        # Set batch size to 1 since we'll be running inference on
        # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1
    config = InferenceConfig()
    config.display()

    model = modellib.MaskRCNN(mode="inference", config=config, model_dir="modules/mask_rcnn/logs")
    weights_path = "modules/mask_rcnn/mask_rcnn_car.h5"
    
    model.load_weights(weights_path, by_name=True)
    images = [
        ("/Users/juanmanuel/Desktop/Images/imagen_1.jpg", 0.4375),
        ("/Users/juanmanuel/Desktop/Images/imagen_2.jpg", 0.4366),
        #("/Users/juanmanuel/Desktop/Images/imagen_3.jpg", 0.6)
        ("/Users/juanmanuel/Desktop/Images/imagen_4.jpg", 0.49)
        #("/Users/juanmanuel/Desktop/Images/imagen_5.jpg", )
    ]
    
    for image, ratio in images:
        r = detect(model, image_path=image, video_path="")
        mask = r["masks"] 
        #print(r)
        #print(r["masks"])
        print(r["masks"][0])
        print(r["masks"][0].shape)
        print(r["masks"][0].shape[0])
        mask = (np.sum(mask, -1, keepdims=True) >= 1)
        print(mask.shape[0])
        print(mask.shape)
        # Copy color pixels from the original color image where mask is set
        print("Puntos")
        if mask.shape[0] > 0:
            pixels = np.where(mask)
            px_0 = pixels[1]
            px_1 = pixels[0]
            points = []
            for i, x in enumerate(px_1):
                points.append((x, px_0[i]))
            
            lp = geometry.get_left_point(points)[0]
            rp = geometry.get_right_point(points)[0]
            tp = geometry.get_top_point(points)[1]
            bp = geometry.get_bottom_point(points)[1]
            area = (rp - lp) * (bp - tp)
            area2 = area * ratio * ratio
            print(area2)
            #poly = Polygon(points)
            #print(Polygon(points).area)

def test_intersection():
    vehicle_shape = [(10, 10), (10,60), (80,60), (80,10)]
    for spot in ParkingSpot.objects():
        (is_intersect, occupied_area) = geometry.intersection(spot.shape, vehicle_shape)
        if is_intersect:
            print(spot.to_json())
            print(occupied_area)
            
        
def test_intersection_2():
    vehicle_shape = [(10, 10), (10,60), (80,60), (80,10)]
    for spot in ParkingSpot.objects():
        spot.check_vehicle(vehicle_shape)    

def check_intersection_of_cars(car_shapes):
    #parkig_spot_detector_test()
    #vehicle_detector_test()
    #test_intersection()
    #test_intersection_2()
    #vehicle_detector_test()

    # SERVER ENTRY POINT
    #import nodes.server
    #pass
   
    car_shape = [[207,42], [243, 42], [241, 123], [206, 123]]
    #car_shape = [[120,160], [195, 200], [150, 300], [95, 245]]
    image_path = '../images/img_1389_crop_2.jpg'
    image = cv2.imread(image_path)
    result = image.copy()
    parking_spots = []

    
    for ps in PARKING_SLOTS:
        p = ParkingSpot()
        p.shape = ps
        parking_spots.append(p)

    for car_shape in car_shapes:
        for ps in parking_spots:
            intersection = ps.check_vehicle(car_shape)

            if intersection:
                color = random.uniform(0, 255),random.uniform(0, 255),random.uniform(0, 255)
                spot_poly = Polygon(ps.shape)
                intersection_poly = Polygon(intersection)
                #print(spot_poly.area)
                #print(intersection_poly.area)
                #print(spot_poly.area - intersection_poly.area)

                diff = spot_poly.difference(intersection_poly)
                
                if diff.geom_type == 'Polygon':
                    diffs = [diff]
                else:
                    diffs = list(diff)
                
                for p in diffs:
                    cv2.polylines(result, np.int_([p.exterior.coords]), True, (0, 0, 255))
                
                cv2.polylines(result, np.int_([intersection]), True, (0, 255, 0))

            #color = random.uniform(0, 255),random.uniform(0, 255),random.uniform(0, 255)
            #cv2.fillPoly(result, np.int_([ps]), color)
            #cv2.polylines(result, np.int_([ps]), True, color)

        #color = random.uniform(0, 255),random.uniform(0, 255),random.uniform(0, 255)
        cv2.polylines(result, np.int_([car_shape]), True, (255, 0, 0))

        #cv2.imshow("Original", image)
        cv2.imshow("Result", result)
        cv2.waitKey()


if __name__ == '__main__':
    image_path = '../images/img_1389_empty_crop_mask_result_2.jpg'
    image = cv2.imread(image_path)
    
    cv2.imshow("Original", cv2.imread('../images/img_1389_crop_2.jpg'))
    cv2.waitKey(0)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    coefficient = 0.02
    car_shapes = []
    for c in cnts:
        poly_hull = cv2.convexHull(c)
        epsilon = coefficient * cv2.arcLength(poly_hull, True)
        poly_approx = cv2.approxPolyDP(poly_hull, epsilon, True)

        #print(epsilon)
        #print(poly_hull)

        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        #cv2.drawContours(image, [poly_approx], -1, (255, 0, 0), 2)

        c_np = np.array(c)
        c_np = np.reshape(c_np, (-1, 2))
        
        left_point_x = geometry.get_left_point(c_np)[0]
        right_point_x = geometry.get_right_point(c_np)[0]
        top_point_y = geometry.get_top_point(c_np)[1]
        bottom_point_y = geometry.get_bottom_point(c_np)[1]

        polyline = [
            [left_point_x, top_point_y],
            [right_point_x, top_point_y],
            [right_point_x, bottom_point_y],
            [left_point_x, bottom_point_y]
        ]

        cv2.polylines(image, np.int_([polyline]), True, (0, 0, 255), 2)
        
        car_shapes.append(polyline)
        #cv2.polylines(image, np.int_([intersection]), True, (0, 255, 0))

        cv2.imshow("Image", image)
        cv2.waitKey(0)

    check_intersection_of_cars(car_shapes)

