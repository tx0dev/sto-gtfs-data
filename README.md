STO GTFS data
===============

This is an attempt a building a GTFS data set for the STO network since it is not publish at the moment.

Ceci est une tentative pour batîr un set de fichiers GTFS pour le réseau de la STO vus que cette information n'est pas disponible en ce moment.


Scripts
=======

routes.py
---------

Will download the route information. Still working out how to get it to work correctly

stops.py
--------

Used the json file created by the `route.py` to get all the stops in the network. Looking into the `working-data` folder for an export.

times.py
--------

Gather the stop time for a given route at a given stop.

It parse the html using BeautifulSoup

Copyright
=========

All data create base on the STO data available at their websites:

- [http://m.sto.ca](http://m.sto.ca)
- [http://planibus.sto.ca](http://planibus.sto.ca)

Comme aucune données est utilisées a des fins commerciales ou lucratives, aucune autorisation est nécessaire:

> ©2012 Société de transport de l'Outaouais. Tous droits réservés. Les informations et données qui apparaissent sur ce site ne peuvent être utilisées à des fins commerciales ou lucratives sans autorisation de la STO.
