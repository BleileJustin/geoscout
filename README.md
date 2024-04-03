# GeoScout | A real-time Web Map Dashboard
### Closely follows this [tutorial](https://louisz.medium.com/basic-real-time-web-map-dashboard-using-geoserver-5e944cc1677a) as a foundation. <br/><br/>Further use case functionality in progress.

## Server:
A NodeJS server that uses Postgresql to connect to and update a PostGIS database to emulate an asset moving in real-time

## App:
The Front-End application, handles the WMS connection between GeoServer and OpenLayers as well as rendering and refreshing of the WMSImage to show real-time updates overlayed on an Open Source Map

