from flask import *
app = Flask(__name__)
# import pandas as pd
import requests
import csv
from settings import PREDICTOR_CLIENT, DB_URL, DB
from functions import getPrediction
from pymongo import MongoClient
import zmq
from flask_cors import CORS, cross_origin

context = zmq.Context()
CORS(app)
#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect (PREDICTOR_CLIENT)
client = MongoClient(DB_URL)
db = client[DB]
prediction_db = db.prediction

with open('train.csv') as f:
    reader = csv.reader(f, skipinitialspace=True,delimiter=',', quoting=csv.QUOTE_NONE)
    mydict = dict(reader)


@app.route('/')
def index():
    return 'Server is okay!'

@app.route('/all', methods=['GET', 'POST'])
def allparam():
    data = request.get_json()
    print(data)
    print type(data)
    train_number = int(data['conditions'][0]['train'])
    train_class = data['conditions'][1]['class']
    quota = data['conditions'][2]['quota']
    hours = int(data['hours_before'])
    waiting_list = int(data['waiting_list'])
    indv_prediction = getPrediction([{'train': train_number}, {'class': train_class}, {'quota' : quota}], hours, waiting_list, socket)
    a = indv_prediction
    del a['data']
    del a['message']
    del a['prediction_val']
    a['index'] = data['index']

    print(a['probability'])

    if a['probability']<41:
        print("Reached")
        orig = data['from']
        source = data['to']
        origIATA = mydict[orig]
        sourceIATA = mydict[source]

        surl = 'http://api.sandbox.amadeus.com/v1.2/airports/autocomplete?apikey=u24iOTgpuRfGjF0SOSAhJyYKAj7myKPu&term=' + sourceIATA
        ourl = 'http://api.sandbox.amadeus.com/v1.2/airports/autocomplete?apikey=u24iOTgpuRfGjF0SOSAhJyYKAj7myKPu&term=' + origIATA

        s =  requests.get(surl)
        o = requests.get(ourl)

        print s.content
        print o.content

        s = json.loads(s.content)
        o = json.loads(o.content)
        s = s[0]['value']
        o = o[0]['value']
        date = data['date']
        url = 'http://api.sandbox.amadeus.com/v1.2/flights/extensive-search?origin=' + o + '&destination=' + s + '&departure_date=' + date + '&one-way=true&apikey=u24iOTgpuRfGjF0SOSAhJyYKAj7myKPu'
        print(url)
        f = requests.get(url)
        a['flight'] = json.loads(f.content)

    # resp = Response(jsonify(**a))
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    return jsonify(**a)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')