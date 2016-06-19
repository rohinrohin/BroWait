from flask import *
app = Flask(__name__)
import pandas as pd

import csv
from settings import PREDICTOR_CLIENT, DB_URL, DB
from functions import getPrediction
from pymongo import MongoClient
import zmq

context = zmq.Context()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(PREDICTOR_SERVER)
