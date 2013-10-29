#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import json
import logging

# Logging
logger = logging.getLogger("routes")
logger.setLevel(logging.INFO)

file_log = logging.FileHandler("routes.log")
logger.addHandler(file_log)
std_log = logging.StreamHandler()
logger.addHandler(std_log)

# Prettify log
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_log.setFormatter(formatter)

# Base URL
URL_ROUTE="http://m.sto.ca/fr/horaires/?action=getRoutes&date=%s"

# Variable
DATE="2013-11-02"

logger.info("======= NEW RUN =======")

get_route = URL_ROUTE % (DATE,)

# building the list for a give DATE.

logger.info("Opening route URL for date %s", DATE)
rawRoute=urllib2.urlopen(get_route).read()

logger.info("Parsing JSON")

routes = json.loads(rawRoute)

logger.info("Saving file")
with open("working-data/routes-%s.json" % (DATE,), "w") as f:
    f.write(json.dumps(routes["RouteDirection"], sort_keys=True, indent=2, separators=(',', ': ')))

logger.info("process complete, %s route saved", len(routes["RouteDirection"]))