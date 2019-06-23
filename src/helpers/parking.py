import cv2
import numpy as np

from globals.constants import STATES, COLORS

def draw_parking(parking):
    PARKING_SPOT_WIDTH = 60
    PARKING_SPOT_HEIGHT = 90
    
    for level in parking.levels:
        result = np.zeros((6 * PARKING_SPOT_HEIGHT, 14 * PARKING_SPOT_WIDTH, 3), dtype="uint8")
        i = 0
        for block in level.blocks:
            for spot in block.spots:
                cv2.fillPoly(result, np.int_([spot.shape]), COLORS[i])
                i += 1

        cv2.imshow("Level " + str(level.level), result)

    cv2.waitKey()

def generate_parking_test():
    PARKING_SPOT_WIDTH = 60
    PARKING_SPOT_HEIGHT = 90
    
    p = Parking()
    p.name = "parking"
    
    pl = ParkingLevel()
    p.levels.append(pl)

    blocks = [
        {'location': 'A', 'levels': 1, 'spots_per_level': 7, 'offset': {'left': 0 * PARKING_SPOT_WIDTH, 'top': 0 * PARKING_SPOT_HEIGHT}},
        {'location': 'B', 'levels': 1, 'spots_per_level': 5, 'offset': {'left': 9 * PARKING_SPOT_WIDTH, 'top': 0 * PARKING_SPOT_HEIGHT}},
        {'location': 'C', 'levels': 2, 'spots_per_level': 5, 'offset': {'left': 2 * PARKING_SPOT_WIDTH, 'top': int(2 * PARKING_SPOT_HEIGHT)}},
        {'location': 'D', 'levels': 2, 'spots_per_level': 4, 'offset': {'left': 9 * PARKING_SPOT_WIDTH, 'top': int(2 * PARKING_SPOT_HEIGHT)}},
        {'location': 'E', 'levels': 1, 'spots_per_level': 7, 'offset': {'left': 0 * PARKING_SPOT_WIDTH, 'top': 5 * PARKING_SPOT_HEIGHT}},
        {'location': 'F', 'levels': 1, 'spots_per_level': 5, 'offset': {'left': 9 * PARKING_SPOT_WIDTH, 'top': 5 * PARKING_SPOT_HEIGHT}}
    ]
    
    for block in blocks:
        pb = ParkingBlock()
        pb.location = block['location']
        pb.shape = [
            [block['offset']['left'], block['offset']['top']],
            [block['offset']['left'], block['offset']['top'] + (block['levels'] * PARKING_SPOT_HEIGHT )],
            [block['offset']['left'] + (block['spots_per_level'] * PARKING_SPOT_WIDTH), block['offset']['top'] + (block['levels'] * PARKING_SPOT_HEIGHT)],
            [block['offset']['left'] + (block['spots_per_level'] * PARKING_SPOT_WIDTH), block['offset']['top']],
        ]
        for i in range(block['levels']):
            ofsset_top = block['offset']['top'] + (i * PARKING_SPOT_HEIGHT)
            for j in range(block['spots_per_level']):
                ofsset_left = block['offset']['left'] + (j * PARKING_SPOT_WIDTH)

                ps = ParkingSpot()
                ps.location = str(j)
                ps.shape = [
                    [ofsset_left, ofsset_top],
                    [ofsset_left, ofsset_top + PARKING_SPOT_HEIGHT],
                    [ofsset_left + PARKING_SPOT_WIDTH, ofsset_top + PARKING_SPOT_HEIGHT],
                    [ofsset_left + PARKING_SPOT_WIDTH, ofsset_top],
                ]

                color = random.uniform(0, 255),random.uniform(0, 255),random.uniform(0, 255)
                ps.save()
                pb.spots.append(ps)
        
        pb.save()
        pl.blocks.append(pb)
        
    pl.save()
    p.save()