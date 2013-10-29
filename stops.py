#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import json
import time

# Base URL
URL_ROUTE="http://m.sto.ca/fr/horaires/?action=getRoutes&date=%s"
URL_STOP="http://m.sto.ca/fr/horaires/?action=getStops&date=%s&time=%s&route=%s"

# Variable
DATE="2013-10-28"
TIME = "12%3A00+AM"
ROUTE = "11_C%C3%89GEP+GABRIELLE-ROY+via+PARC+DE+LA+MONTAGNE"

stops = []

# Open and load routes list
rawRoutes = open("working-data/routes-week.json")
routes = json.load(rawRoutes)

# Because some people are asshole...
print """WARNING!!!
This will hit the STO website for each route and it takes quite some time.
#### DO NOT RUN DURING THE DAY. ####
Are you sure you want to continue?"""
if raw_input("yes/no?") == "yes":
    print "okay then... starting"
    print "There is", len(routes), "routes to process"
    time.sleep(2)
else:
    print "exiting..."
    exit()

# Well... Starting route loop
for route in routes:
    print "Processing route",route["PublicIdentifier"], route["Description"], route["Direction"]

    r = "%s_%s" % (route["PublicIdentifier"], route["DirectionName"])
    get_stop = URL_STOP % (DATE, TIME, r)

    # don't ask about the replace
    url = urllib2.quote(get_stop.encode("utf8"), ":/;?&=%").replace("%27","%2527")

    print "URL:", url
    print "Loading..."
    u = urllib2.urlopen(url)

    # If there is a malform URL it fail
    if u.geturl() == "http://m.sto.ca/fr/maintenance/":
        print "Site maintenance or something broke..."
        exit()
    rawStop = u.read()

    print "Parsing json and checking for existing stops"
    data = json.loads(rawStop)

    # Add the stop to the common array
    stopAdded = 0
    stopSkipped = 0
    for d in data:
        id = d['Identifier'].replace(':','')

        found = False
        for s in stops:
            if s["Identifier"] == d['Identifier']:
                found = True
                stopSkipped = stopSkipped + 1
        if found:
            print "%s-E" % (id,),
        else:
            print "%s-A" % (id,),
            stops.append(d)
            stopAdded = stopAdded + 1
    print ""
    print "## Progress"
    print "Stops:", len(stops), "(%s added, %s skipped)" % (stopAdded, stopSkipped)
    print "Route: index ", routes.index(route), "of", len(routes)
    time.sleep(1)

# Write result to a file
print "Complete!, Writing result to file"
with open("stops.json", "w") as f:
    f.write(json.dumps(stops, sort_keys=True, indent=2, separators=(',', ': ')))
    f.close()
print "There is", len(stops), "stops in total"