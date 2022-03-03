**Download Image**
=================

Args that can be passed in:

 *bbox (str)*

  A ``bbox`` (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate) for
  projection EPSG:4326 or minx,miny,maxx,maxy,EPSG:3857 for projection EPSG:3857. Other projections are not supported at this time

   **Example:**
     ``download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912")``

     ``download_image(bbox="-11688123.519228712,4830113.564872338,-11687566.921774745,4830837.565406834,EPSG:3857")``

 *height and width (int)*

  Desired image ``height`` in pixels. Maximum is 8000.

   **Example:**
     ``download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512)``

 *img_format (str)*

  The ``img_format`` is the desired format of the returned object. Available options include **jpeg**, **png**, or **geotiff**

   **Example:**
     ``download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512, img_format='png')``

 *identifier and gridoffsets (str)*

  The ``identifier`` is the online id of the desired image feature. The ``gridoffsets`` are the desired output resolution in units of GridCRS

   **Example:**
     ``download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", identifier='d330c2f9486b4b5b0798b142fd1e6388', gridoffsets='.0000045,.0000045', img_format='png')``

   **Notes:**
     Currently only works with EPSG:4326

 *zoom_level (int)*

  The ``zoom_level`` is the desired scale of the image

   **Example:**
     ``download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", zoom_level=15, img_format='png')``

   **Notes:**
     Currently only works with EPSG:4326

 *download (bool) and outputpath (str)*

  The ``download`` is a boolean of whether or not the desired image should be downloaded. ``download`` defaults to true. The ``outputpath`` is the desired location for the image to be downloaded. ``outputpath`` defaults to root directory and defaults name of file to download (ex: C:\Users\<user>\download.jpeg). File extension is also needed in outputpath if declared (ex: ``r'C:\Users\<user>\image.jpeg'``)

   **Example:**
     ``download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512, img_format='png', download=True, outputpath=r'C:\Users\<user>\image.jpeg')``

Kwargs that can be passed in:

 *legacyid (str)*

  The ``legacyid`` is the archive identifier of the desired browse image

   **Example:**
     ``download_image(legacyid='104001007396EC00')``

 *crs (str)*

  The ``crs`` is the desired projection for spatial imagery rendered in either EPSG (European Petroleum Survey Group) 4326 or EPSG 
  3857. If a ``crs`` is not declared the default will be set to EPSG 4326. EPSG 4326 is represented in decimal degrees while 
  EPSG 3857 is represented in meters northing and meters easting. Other projections are not supported at this time

   **Example:**
     ``download_image("39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512, img_format='png', crs='EPSG:4326')``