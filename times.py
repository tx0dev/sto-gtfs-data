#!/usr/bin/python
from BeautifulSoup import BeautifulSoup                                                                                                  
import urllib2


URL="http://m.sto.ca/fr/horaires/resultats/?action=getCompletePassingTimes&stop=:1097&route=51_P-O-B+RIVERMEAD&date=2013-10-30"

print "## Opening URL"
#rawStop=urllib2.urlopen(URL).read()
rawStop=open("horairesjson")
print "## Parsing page"
stopSoup = BeautifulSoup(rawStop)
times = stopSoup.findAll("div", attrs={"class" : "timeHoraire"})
route = stopSoup.find("div", attrs={"class" : "horaires-results"}).findAll("p")[0].contents[1].strip()
stop = stopSoup.find("div", attrs={"class" : "horaires-results"}).findAll("p")[1].contents[1].strip()
infobus = stopSoup.find("div", attrs={"class" : "horaires-results"}).findAll("p")[2].contents[1].strip()
print "## results"

print "Stop", stop
print "Route", route
print "Infobus", infobus

# Build array
stopTimes = []

for time in times:
    stopTimes.append(time.contents[0])
print stopTimes
