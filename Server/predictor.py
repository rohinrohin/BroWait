import zmq
import logging
from settings import LOG_FILE, PREDICTOR_SERVER, DB_URL, DB, COLLECTION
from pymongo import MongoClient, DESCENDING
import json
from functions import prediction, getRelevantData

#Connecting to mongodb and selecting the right collection
client = MongoClient(DB_URL)
db = client[DB]
collection = db[COLLECTION]

#This decides how to sort the result
sort_by = {
    "column" : "_id",
    "type" : DESCENDING
}

logging.basicConfig(filename=LOG_FILE,level=logging.DEBUG, format='%(asctime)s %(message)s')
context = zmq.Context()


socket = context.socket(zmq.REP)
socket.bind(PREDICTOR_SERVER)

while True:

    print "Started"
    s = socket.recv()
    message = json.loads(s)
    #sanity check the input
    data = getRelevantData(collection,message["conditions"], sort_by, 20)
    result = prediction(message["hours_before"], message["waiting_list"], data)
    logging.info(message)

    #  Send the reply.
    socket.send (json.dumps(result))
