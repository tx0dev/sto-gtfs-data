#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 20:12:40 2013

@author: elwillow
"""

from BeautifulSoup import BeautifulSoup
import urllib2
import json
import time
import logging

LOCAL = True

# Logging
logger = logging.getLogger("stops")
logger.setLevel(logging.INFO)

file_log = logging.FileHandler("trip-test.log")
logger.addHandler(file_log)
std_log = logging.StreamHandler()
logger.addHandler(std_log)

# Prettify log
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_log.setFormatter(formatter)

# require, in order: stop, route number + route direction and date.
URL_SHED="http://m.sto.ca/fr/horaires/resultats/?action=getCompletePassingTimes&stop=:%s&route=%s&date=%s"
URL_STOPS="http://m.sto.ca/fr/horaires/?action=getStops&date=%s&time=%s&route=%s"
DATE="2013-10-30"
TIME = "12%3A00+AM"

def stoUrl(s):
    # don't ask about the replace
    return urllib2.quote(s.encode("utf8"), ":/;?&=%").replace("%27","%2527")

# For the purpose of testing, the 62 only have 19 stops according to the date pulled from the site.
if LOCAL:
    logger.info("Loading route 62 for testing")
    routes = json.loads("""[{
    	"Identifiers": { "string": ":262"},
    	"PublicIdentifier": "62",
    	"Description": "GR\u00c9BER nord",
    	"Direction": "South",
    	"DirectionName": "STATION LA GAPPE via GR\u00c9BER",
    	"ServiceMode": "Bus",
    	"ServiceType": "Regular",
    	"Site": { "Identifier": ":","Name": "STO"},
    	"InternalIndexes": { "int": [1891, 1143, 2662, 1658, 2048, 3007, 3467, 150, 918, 533 ,3017, 1187, 4647, 3757, 621, 1212, 4398, 1688, 2818, 2774, 2118, 3160, 4321, 11928] },
    	"InternalIndexes2": {	"int": [1891, 3467, 4398, 2774, 11928] }
    }]""")
else:
    routes = json.load(open("working-data/route-week.json"))

logger.info("Loading stops list")

for route in routes:
    logger.info("Processing route %s %s %s",route["PublicIdentifier"], route["Description"], route["Direction"])

    # Getting the stops list for the route
    routeString = "%s_%s" % (route["PublicIdentifier"], route["DirectionName"])
    stopsUrl = URL_STOPS % (DATE, TIME, routeString)


    logger.debug("Stop URL: %s", stopsUrl)
    u = urllib2.urlopen(stoUrl(stopsUrl))
    # If there is a malform URL it fail
    if u.geturl() == "http://m.sto.ca/fr/maintenance/":
        logger.warning("Site maintenance or something broke...")
        exit()

    rawStops = u.read()
    logger.info("Loading JSON for the stop list")
    routeStops = json.loads(rawStops)
    # We have the stop for that route, now let's build the trip schedule

    ## Building the passageTimes array for a given route.
    # It is 2 dimensional array: first level is the stop, second is the passage time.
    routeTimes = []
    routeInfos = []
    for stop in routeStops:
        # Building trips data
        id  = stop['Identifier'].replace(':','')
        infoClean = {"id": id}
        timesClean = []

        logger.info("Looking up stop id %s", id)
        infobusUrl = URL_SHED % (id, routeString,DATE)

        logger.debug("Infobus URL: %s", infobusUrl)

        s = urllib2.urlopen(stoUrl(infobusUrl))
        if u.geturl() == "http://m.sto.ca/fr/maintenance/":
            # In case something broke, quit
            logger.warning("Site maintenance or something broke...")
            exit()

        logger.debug("HTML parsing")
        infoSoup = BeautifulSoup(s.read())

        logger.debug("Building timetable")

        times = infoSoup.findAll("div", attrs={"class" : "timeHoraire"})

        # Clean the result and add it to the main array
        for t in times:
            timesClean.append(t.contents[0])
        routeTimes.append(timesClean)

        logger.debug("Building info")
        infoP = infoSoup.find("div", attrs={"class":"horaires-results"}).findAll("p")
        infoClean["stop"] = infoP[1].contents[1].strip()
        if len(infoP) == 5:
            infoClean["infobus"] = infoP[2].contents[1].strip()
        else:
            infoClean["infobus"] = "None"
        routeInfos.append(infoClean)

        logger.info("Stop complete (%s)", infoClean["stop"])

logger.info("Process complete")
print "#############################"
for r in routeInfos:
    print "%(stop)s (#%(infobus)s)," % r,
print ""
for i in xrange(len(routeTimes)):
    for t in routeTimes:
        print "%s," % (t[i], ),
    print ""


#logger.info("## Parsing page")
#
#stopSoup = BeautifulSoup(rawStop)
#times = stopSoup.findAll("div", attrs={"class" : "timeHoraire"})
#route = stopSoup.find("div", attrs={"class" : "horaires-results"}).findAll("p")[0].contents[1].strip()
#stop = stopSoup.find("div", attrs={"class" : "horaires-results"}).findAll("p")[1].contents[1].strip()
#infobus = stopSoup.find("div", attrs={"class" : "horaires-results"}).findAll("p")[2].contents[1].strip()
#
#print "RESULTS"
#print "Stop", stop
#print "Route", route
#print "Infobus", infobus
#
## Build array
#stopTimes = []
#
#for time in times:
#    stopTimes.append(time.contents[0])
#print stopTimes
