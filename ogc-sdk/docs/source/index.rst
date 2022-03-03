.. Maxar-OGC documentation master file, created by
   sphinx-quickstart on Thu Feb  3 09:09:24 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Maxar-OGC's documentation!
=====================================

**Maxar-OGC*** is a Python library for accessing Maxar's imagery platforms
to search and download imagery. Connection is established using connect id 
and login credentials.

Installation:

	1. pip install Maxar-OGC
	2. Create a credentials file called ``.ogc-config`` in the following format

| [ogc]
| user_name=<your-user-name>
| user_password=<your-password>
| user_tenant=<your-base-url> i.e. https://securewatch.digitalglobe.com
| user_connectid=<your-connectid>
	
.. toctree::
   :maxdepth: 2
   
   image_search
   download_image
   metadata
   discover_browse
   band_manipulation

   sample_usage



