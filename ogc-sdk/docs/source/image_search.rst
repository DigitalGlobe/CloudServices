**Image Search**
================

Kwargs that can be passed in:

 *bbox (str)*

  A ``bbox`` (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate) for
  projection EPSG:4326 or minx,miny,maxx,maxy,EPSG:3857 for projection EPSG:3857. Other projections are not supported at this time

   **Example:**
     ``search(bbox="39.7530, -104.9962, 39.7580, -104.9912")``

     ``search(bbox="-11688123.519228712,4830113.564872338,-11687566.921774745,4830837.565406834,EPSG:3857")``

 *filter (str)*

  A ``filter`` is a CQL filter using Common Query Language to refine data of search. Further CQL parameters accepted by Maxar can be
  found here: `Filters <https://securewatchdocs.maxar.com/en-us/Miscellaneous/DevGuides/Common_Query_Language/Query.htm?Highlight=cql>`_

   **Example:**
     ``search(filter="(acquisitionDate>='2022-01-01')")``

     ``search(filter="(acquisitionDate>='2022-01-01')AND(cloudCover<0.20)")``

     ``search(bbox="39.7530, -104.9962, 39.7580, -104.9912", filter="(acquisitionDate>='2022-01-01')AND(cloudCover<0.20)")``

   **Notes:** 
      If a bbox is desired, the bbox string is an argument separate from the filter string. This bbox must be in EPSG:4326.
      Search parameters must be wrapped in parentheses within the filter string

 *srsname (str)*

  An ``srsname`` is the desired projection for spatial imagery rendered in either EPSG (European Petroleum Survey Group) 4326 or EPSG 
  3857. If an ``srsname`` is not declared the default will be set to EPSG 4326. EPSG 4326 is represented in decimal degrees while 
  EPSG 3857 is represented in meters northing and meters easting. Other projections are not supported at this time

   **Example:**
     ``search(bbox="39.7530, -104.9962, 39.7580, -104.9912")``
     
     ``search(bbox="-11688123.519228712,4830113.564872338,-11687566.921774745,4830837.565406834,EPSG:3857")``

 *outputformat (str)*

  The ``outputformat`` is the desired format of the returned object. Available options include:

  - atom
  - csv
  - gml2
  - gml3
  - gml32
  - json
  - kml
  - rss
  - shape-zip

   **Example:**
     ``search(filter="(acquisitionDate>='2022-01-01')AND(cloudCover<0.20)", outputformat='json')``

 *featureprofile (str)*

  A ``featureprofile``, or stacking profile, is defined based upon the attributes that are most important to the user. The stacking
  profile is used to assemble the features into a mosaic that best satisfies the desired preference. If a profile is not specified, it 
  will default to Default_Profile. A list of available stacking profiles can be found here: `Stacking Profiles <https://securewatchdocs.maxar.com/en-us/Miscellaneous/DevGuides/Stacking_Profiles/stack_profiles.htm>`_


    **Example:**
      ``search(bbox="39.7530, -104.9962, 39.7580, -104.9912", featureprofile='Cloud_Cover_Profile')``