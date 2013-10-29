#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import json
import time
import logging

# Logging
logger = logging.getLogger("stops")
logger.setLevel(logging.DEBUG)

file_log = logging.FileHandler("stops.log")
logger.addHandler(file_log)
std_log = logging.StreamHandler()
logger.addHandler(std_log)

# Prettify log
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_log.setFormatter(formatter)

# Base URL
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
if raw_input("yes/no? ") == "yes":
    print "okay then... starting"
    logger.info("There is %s routes to process", len(routes))
    time.sleep(2)
else:
    logger.info("exiting...")
    exit()

# Well... Starting route loop
for route in routes:
    logger.info("Processing route %s %s %s",route["PublicIdentifier"], route["Description"], route["Direction"])

    r = "%s_%s" % (route["PublicIdentifier"], route["DirectionName"])
    get_stop = URL_STOP % (DATE, TIME, r)

    # don't ask about the replace
    url = urllib2.quote(get_stop.encode("utf8"), ":/;?&=%").replace("%27","%2527")

    logger.debug("URL: %s", url)
    u = urllib2.urlopen(url)

    # If there is a malform URL it fail
    if u.geturl() == "http://m.sto.ca/fr/maintenance/":
        logger.warning("Site maintenance or something broke...")
        exit()
    rawStop = u.read()

    logger.info("Parsing json and checking for existing stops")
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
            logger.debug("Stop %s exist, skipped", id)
        else:
            logger.debug("Stop %s added",id)
            stops.append(d)
            stopAdded = stopAdded + 1
    logger.info("Progress: Stop=%s (%s added, %s skipped) | Route: index %s of %s",
                len(stops), stopAdded, stopSkipped, routes.index(route), len(routes))
    time.sleep(1)

# Write result to a file
logger.info("Complete!, Writing result to file")
with open("working-data/stops.json", "w") as f:
    f.write(json.dumps(stops, sort_keys=True, indent=2, separators=(',', ': ')))
    f.close()
logger.info("There is %s stops", len(stops))