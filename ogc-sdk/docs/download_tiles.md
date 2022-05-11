**Download Tiles**
==================

Args that can be passed in:

##bbox (str)

  A ``bbox`` (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate) for
  projection EPSG:4326Other projections are not supported at this time

   **Example:**
     ``download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912")``

   **Notes:**
     Currently only works with EPSG:4326


##zoom_level (int)

  The ``zoom_level`` is the desired scale of the image

   **Example:**
     ``download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", zoom_level=15, img_format='png')``

   **Notes:**
     Currently only works with EPSG:4326

##img_format (str)

  The ``img_format`` is the desired format of the returned object. Available options include **jpeg**, **png**, or **geotiff**

   **Example:**
     ``download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512, img_format='png')``

##outputpath (str)
 
 The ``outputpath`` is the desired location for the image to be downloaded. ``outputpath`` defaults to root directory and defaults name of file to download . File extension is also needed in outputpath if declared (ex: ``r'C:\Users\<user>\image.jpeg'``)
	
   **Example:**
		``(C:\Users\<user>\download.jpeg)``

##display (bool)

  The ``display`` is a boolean of whether or not the desired image should be dispayed. ``download`` defaults to true. 

   **Example:**
     ``download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512, img_format='png', download=True, outputpath=r'C:\Users\<user>\image.jpeg')``
