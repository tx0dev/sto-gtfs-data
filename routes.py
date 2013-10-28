#!/usr/bin/python
import urllib2
import json

# Base URL
URL_ROUTE="http://m.sto.ca/fr/horaires/?action=getRoutes&date=%s"
URL_STOP="http://m.sto.ca/fr/horaires/?action=getStops&date=%s&time=%s&route=%s"

# Variable
DATE="2013-10-28"
TIME = "12%3A00+AM"
ROUTE = "11_C%C3%89GEP+GABRIELLE-ROY+via+PARC+DE+LA+MONTAGNE"

stops= {}

get_route = URL_ROUTE % (DATE,)
get_stop = URL_STOP % (DATE,TIME,ROUTE)

# building the list for a Sunday

print "## Opening route URL"
#rawRoute=urllib2.urlopen(get_route).read()
# Debug, using local file

rawRoute=open("horaire.json")

print "## Parsing JSON"

data = json.load(rawRoute)

print "## Evaluation"
for d in data:
    id = d['Identifier'].replace(':','')

    if id not in stops:
        print "ADDING", id
        stops[id] = {"stop_name": d['Description'], }
    else:
        print "SKIP  ", id


# Print Result
print "## RAW OUTPUT"
print stops