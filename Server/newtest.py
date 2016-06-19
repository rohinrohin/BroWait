import csv
from settings import PREDICTOR_CLIENT, DB_URL, DB
from functions import getPrediction
from pymongo import MongoClient
import zmq

context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect (PREDICTOR_CLIENT)
client = MongoClient(DB_URL)
db = client[DB]
prediction_db = db.prediction


#ofile  = open('/tmp/ttest.csv', "wb")
#writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
#writer.writerow(['pnr', 'train', 'class', 'quota', 'hours', 'wl', 'original status', 'original prediction', 'new prediction', 'new status'])

train_number = 12610
train_class = 'CC'
quota = 'GNWL'
hours = 24
waiting_list = 19
indv_prediction = getPrediction([{'train': train_number}, {'class': train_class}, {'quota' : quota}], hours, waiting_list, socket)
print indv_prediction
