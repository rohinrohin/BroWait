import csv
import requests
import json

with open('train.csv') as f:
    reader = csv.reader(f, skipinitialspace=True,delimiter=',', quoting=csv.QUOTE_NONE)
    mydict = dict(reader)

orig = 'SBC'
source = 'MAS'
origIATA = mydict[orig]
sourceIATA = mydict[source]

# url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + place + '&key=AIzaSyACxVd-ZjGJv67m4WvzvUdXkEtRwEQifg0'
import requests
# r = requests.get(url)
# cont = json.loads(r.content)
# lat = cont['results'][0]['geometry']['location']['lat']
# long = cont['results'][0]['geometry']['location']['long']

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
# s = s[]
date = '2016-06-16'
url = 'http://api.sandbox.amadeus.com/v1.2/flights/extensive-search?origin=' + o + '&destination=' + s + '&departure_date=' + date + '&one-way=true&apikey=u24iOTgpuRfGjF0SOSAhJyYKAj7myKPu'
print(url)
f = requests.get(url)
print(f.content)