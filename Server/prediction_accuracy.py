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
predictions = prediction_db.find({'status' : {'$in':['failure', 'success']}}).sort([('boarding_time',1)])
i=0
success = 0
failure = 0
orig_succes = 0
orig_failure = 0
for row in predictions:
    print i
    train_number = row['train']
    train_class = row['class']
    quota = row['quota']
    hours = row['hours_before']
    waiting_list = row['waiting_list']
    indv_prediction = getPrediction([{'train': train_number}, {'class': train_class}, {'quota' : quota}], hours, waiting_list, socket)

    if row['status'] == 'failure':
        orig_failure += 1
        if indv_prediction["prediction_val"] == 0 :
            new_prediction = 'na'
        elif indv_prediction["prediction_val"] * row['prediction'] < 0: #in db positive means success, in prediction positive means no chance of booking
            new_prediction = 'success'
            success += 1
        else:
            new_prediction = 'failure'
            failure += 1
    elif row['status'] == 'success':
        orig_succes += 1
        if indv_prediction["prediction_val"] == 0 :
            new_prediction = 'na'
        elif indv_prediction["prediction_val"] * row['prediction'] < 0:
            new_prediction = 'success'
            success += 1
        else:
            new_prediction = 'failure'
            failure += 1
    #writer.writerow([row['pnr'], train_number, train_class, quota, hours, waiting_list, row['status'], row['prediction'], indv_prediction["prediction_val"], new_prediction])
    i += 1

print "Success in " + str(success) + ", Failure in " + str(failure)
print "Original Success in " + str(orig_succes) + ", Original Failure in " + str(orig_failure)
#ofile.close()