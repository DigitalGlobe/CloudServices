**Download_image_with_feature_id**
==================

Args that can be passed in:

##bbox (str)

  A ``bbox`` (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate). Other projections are not supported at this time

   **Example:**
     ``download_image_with_feature_id(bbox="39.7530, -104.9962, 39.7580, -104.9912")``
	 
**Notes:**
     Currently only works with EPSG:4326

##identifier (str)

  The ``identifier`` is the online id of the desired image feature
   **Example:**
     ``download_image_with_feature_id(bbox="39.7530, -104.9962, 39.7580, -104.9912", identifier='57d0e26239dde11463d31ff0893ce9ca')``
	 
##gridoffsets (str)

  The ``gridoffsets`` are the desired output resolution in units of GridCRS

   **Example:**
     ``download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", identifier='d330c2f9486b4b5b0798b142fd1e6388', gridoffsets='.0000045,.0000045', img_format='png')``

   **Notes:**
     Currently only works with EPSG:4326

##img_format (str)

  The ``img_format`` is the desired format of the returned object. Available options include **jpeg**, **png**, or **geotiff**

   **Example:**
     ``download_image_with_feature_id(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512", img_format='png')``

##outputpath (str)
 
 The ``outputpath`` is the desired location for the image to be downloaded. ``outputpath`` defaults to root directory and defaults name of file to download . File extension is also needed in outputpath if declared (ex: ``r'C:\Users\<user>\image.jpeg'``)
	
   **Example:**
		``(C:\Users\<user>\download.jpeg)``


