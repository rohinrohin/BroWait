Prerequisites
-------------
+ [zmq](http://zeromq.org/ "ZeroMQ home page")
+ [mongodb](http://www.mongodb.org/ "MongoDB home page")

Python Libraries Used
---------------------
+ numpy
+ scipy
+ pyzmq
+ pymongo

Database Structure
------------------
+ prediction 
  + pnr : md5 of pnr number
  + boarding_time : time of boarding in ISO date format
  + class : Class of Travel
  + from : from station code
  + to : To station code
  + train : train number
  + waiting_list : Waiting list at the time of prediction
  + hours_before : number of hours before the departure of train from the from station at the time of prediction
  + prediction : number, positive value means ticket will be confirmed and negative value means the opposite, zero is undecided
  + quota : Quota in Indian railways
  + status" : Whether the prediction was success or not, possible values "success" and "failure"
  
+ pnr change
  + date : date in string format, example "03-11-2013"
  + x_val : array of time of checking(number of hours before departure)[  0,  3,  23,  47,  71,  95,  119,  145 ]
  + y_val : array of waiting list at time of checking [  43,  51,  59,  83,  99,  111,  122,  127 ]
  + pnr : md5 of pnr number
  + class : Class of Travel
  + from : from station code
  + to : To station code
  + train : train number
  + quota : Quota in Indian railways

Setting up database
-------------------
Download the .bson files in the db folder and add it to the database.

    mongorestore -h localhost:port -d pnr -c prediction path/to/prediction.bson
    mongorestore -h localhost:port -d pnr -c pnr_change path/to/pnr_change.bson

Suggested installation using virtualenv
---------------------------------------

    virtualenv ~/path/to/virtualenv/folder
    source ~/path/to/virtualenv/folder/bin/activate
    pip install numpy scipy pyzmq pymongo
  
Development
-----------
make changes to the function, run the prediction accuracy job and track whether it has improved accuracy or not

Current Accuracy
----------------
Success in 1765, Failure in 434
Original Success in 1613, Original Failure in 587
