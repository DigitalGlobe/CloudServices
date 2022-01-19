# dgcs-examples

This Git repository contains some simple examples of how you can integrate the DGCS WMS and WMTS OGC services into 
a web application using the [Leaflet](http://leafletjs.com/reference-1.1.0.html) or [Openlayers](http://openlayers.org/en/latest/apidoc/)
APIs.

The [Leaflet](http://leafletjs.com/reference-1.1.0.html) and [Openlayers](http://openlayers.org/en/latest/apidoc/)
APIs offer a wide variety of features.  As the examples provided here are very rudimentary, please refer to the respective
[Leaflet](http://leafletjs.com/reference-1.1.0.html) and [Openlayers](http://openlayers.org/en/latest/apidoc/) API 
documentation for more thorough documentation of what can be done with these tools.

In order to access the DGCS OGC services, you will need a CONNECTID and, depending on how your account is set up, you 
may also need to authenticate with a username and password.  The CONNECTID used in these examples does not require 
authentication and only has access to very low resolution terra color imagery.

This Git repository also has an OGC SDK included for python. This package can be installed via pip from your console and provides
two methods for authentication.  The first method requires a config file as detailed in the README for the package. The second 
method requires passing in username, password, connectid and base url as arguments for the package and is used if the config 
file is not present.