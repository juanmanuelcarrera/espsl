from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import settings
import json

from models.parking import Parking
from models.parkinglevel import ParkingLevel
from models.parkingblock import ParkingBlock
from models.parkingspot import ParkingSpot

from helpers.mongo import mongo_to_dict, list_field_to_dict

app = Flask(__name__)
api = Api(app)

# ParkingListController
# shows a list of all parkings, and lets you POST to add new tasks
class ParkingListController(Resource):
    def get(self):
        return Parking.objects.to_json()

# ParkingController
# shows a single parking item
class ParkingController(Resource):
    def get(self, parking_name):
        return Parking.objects.get(name=parking_name).to_json()

# ParkingSpotController
# shows a parking spots of a parking
class ParkingBlockListController(Resource):
    def get(self, parking_name, block_location):
        block = ParkingBlock.objects.get(location=block_location)
        return block.to_dict()

# ParkingBlockController
# shows a parking spots of a parking
class ParkingSpotListController(Resource):
    def get(self, parking_name):
        return Parking.objects.get(name=parking_name).levels[0].to_json()

##
## Actually setup the Api resource routing here
##
api.add_resource(ParkingListController, '/parking')
api.add_resource(ParkingController, '/parking/<parking_name>')
api.add_resource(ParkingBlockListController, '/parking/<parking_name>/block/<block_location>')
api.add_resource(ParkingSpotListController, '/parking/<parking_name>/spot')

if __name__ == '__main__':
    app.run(debug=True)
