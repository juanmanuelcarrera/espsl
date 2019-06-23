from mongoengine import connect, register_connection

MONGO_URL = "mongodb://localhost:27017/parking_butler"

#connect('chatemtbot', host=os.getenv('MONGO_URL'))
register_connection('default', host=MONGO_URL)