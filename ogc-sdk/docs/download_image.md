# Download Image

## Args:

#### bbox (str):

  A bbox (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate) for
  projection EPSG:4326

   **Example:**
   
     download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912")
	 

#### height (int):

  Desired image height in pixels. Maximum is 8000.

   **Example:**
   
     download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512)
	 
#### width (int):

  Desired image width in pixels. Maximum is 8000.

   **Example:**
   
     download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512)

#### img_format (str):

  The img_format is the desired format of the returned object. Available options include **jpeg**, **png**, or **geotiff**

   **Example:**
   
     download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512, img_format='png')

#### identifier and gridoffsets (str):

  The identifier is the online id of the desired image feature. The gridoffsets are the desired output resolution in units of GridCRS

   **Example:**
   
     download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", identifier='d330c2f9486b4b5b0798b142fd1e6388', gridoffsets='.0000045,.0000045', img_format='png')

   
     

#### zoom_level (int):

  The zoom_level is the desired scale of the image

   **Example:**
   
     download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", zoom_level=15, img_format='png')

   
     

#### download (bool) and outputpath (str):

  The download is a boolean of whether or not the desired image should be downloaded. download defaults to true. The outputpath is the desired location for the image to be downloaded. outputpath defaults to root directory and defaults name of file to download (ex: C:\Users\<user>\download.jpeg). File extension is also needed in outputpath if declared (ex: r'C:\Users\<user>\image.jpeg')

   **Example:**
   
     download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512, img_format='png', download=True, outputpath=r'C:\Users\<user>\image.jpeg')

## Kwargs:

#### legacyid (str):

  The legacyid is the archive identifier of the desired browse image

   **Example:**
   
     download_image(legacyid='104001007396EC00')

