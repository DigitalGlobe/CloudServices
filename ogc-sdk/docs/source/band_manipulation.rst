**Band Manipulation**
======================

Args that can be passed in:

 *bbox (str) (required)*

  A ``bbox`` (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate) for
  projection EPSG:4326 or minx,miny,maxx,maxy,EPSG:3857 for projection EPSG:3857. Other projections are not supported at this time

   **Example:**
     ``bbox="39.7530, -104.9962, 39.7580, -104.9912"``

     ``bbox="-11688123.519228712,4830113.564872338,-11687566.921774745,4830837.565406834,EPSG:3857"``

 *featureid (str) (required)*

  The ``featureid`` is the online id of the desired image feature

   **Example:**
     ``featureid='d330c2f9486b4b5b0798b142fd1e6388'``

 *band_combination (list) (required)*

  The ``band_combination`` is a list of strings containing the desired band combination of 1-4 items. Available options include:

   * R
   * G
   * B
   * C
   * Y
   * RE
   * N
   * N2
   * S1
   * S2
   * S3
   * S4
   * S5
   * S6
   * S7

  Further information about bands can be found here: `Bands <https://securewatchdocs.maxar.com/en-us/Miscellaneous/DevGuides/WMTS/WMTS_GetTile.htm#TheBandsParameter>`_

   **Example:**
     ``band_combination=['R', 'B', 'G', 'C']``

 *download (bool)*

  The ``download`` is a boolean of whether or not the desired image should be downloaded. ``download`` defaults to ``True``

   **Example:**
     ``download=True``

Kwargs that can be passed in:

 *outputpath (str)*

  The ``outputpath`` is the desired location for the image to be downloaded. ``outputpath`` defaults to root directory and defaults name of file 
  to download (ex: C:\Users\<user>\download.jpeg). File extension is also needed in ``outputpath`` if declared (ex: ``r'C:\Users\ 
  <user>\image.jpeg'``)

   **Example:**
     ``band_manipulation(bbox="39.7530, -104.9962, 39.7580, -104.9912", featureid='d330c2f9486b4b5b0798b142fd1e6388', band_combination=['R', 'B', 'G', 'C'], download=True, outputpath=r'C:\Users\<user>\image.jpeg')``

 *crs (str)*

  The ``crs`` is the desired projection for spatial imagery rendered in either EPSG (European Petroleum Survey Group) 4326 or EPSG 
  3857. If a ``crs`` is not declared the default will be set to EPSG 4326. EPSG 4326 is represented in decimal degrees while 
  EPSG 3857 is represented in meters northing and meters easting. Other projections are not supported at this time

   **Example:**
     ``band_manipulation(bbox="-11688123.519228712,4830113.564872338,-11687566.921774745,4830837.565406834,EPSG:3857", featureid='d330c2f9486b4b5b0798b142fd1e6388', band_combination=['R', 'B', 'G', 'C'], download=True, outputpath=r'C:\Users\<user>\image.jpeg', crs='EPSG:3857')``