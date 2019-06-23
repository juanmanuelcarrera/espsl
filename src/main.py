import settings
import numpy as np

from helpers.parking import draw_parking

from modules.parkingspotdetector_capt import ParkingSpotDetector
from modules.motiondetector import MotionDetector
from modules.vehicle_detector.vehicledetector import VehicleDetectorConfig, detect
from mrcnn import model as modellib, utils

from models.parking import Parking
from models.parkinglevel import ParkingLevel
from models.parkingblock import ParkingBlock
from models.parkingspot import ParkingSpot

from shapely.geometry import Polygon
import pyproj
from shapely.geometry import shape
from shapely.ops import transform
from functools import partial

import helpers.geometry as geometry

import nodes.server

def parkig_spot_detector_test():
    image_path = '../images/parking_4.jpg'

    psd = ParkingSpotDetector()
    psd.detect(image_path, 2)


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

if __name__ == '__main__':
    #parkig_spot_detector_test()
    #vehicle_detector_test()
    #test_intersection()
    #test_intersection_2()
    #vehicle_detector_test()

    # SERVER ENTRY POINT
    import nodes.server
    pass

    