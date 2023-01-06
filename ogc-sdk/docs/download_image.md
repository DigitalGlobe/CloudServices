# Download Image

## Args:

#### bbox (str):

  A `bbox` (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate) for
  projection EPSG:4326

   **Example:**
   
     interface.download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912")
	 
#### srsname (str):

  Desired projection. Defaults to "EPSG:4326".
  
  **Example:**
  
    interface.download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", srsname="EPSG:3857")
	 

#### height, width (int):

  Desired image `height` and `width` in pixels. Maximum is 8000.

   **Example:**
   
     interface.download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512)

#### img_format (str):

  The `img_format` is the desired format of the returned object. Available options include **jpeg**, **png**, or **geotiff**

   **Example:**
   
     interface.download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512, img_format='png')

#### identifier and gridoffsets (str):

  The `identifier` is the online id of the desired image feature. The `gridoffsets` are the desired output resolution in units of GridCRS

   **Example:**
   
     interface.download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", identifier='932f7992a4d86a9ca412c024c22792ce', gridoffsets='.0000045,.0000045', img_format='png')

   
     

#### zoom_level (int):

  The `zoom_level` is the desired scale of the image

   **Example:**
   
     interface.download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", zoom_level=15, img_format='png')

   
     

#### download (bool) and outputpath (str):

  The `download` is a boolean of whether or not the desired image should be downloaded. `download` defaults to true. The `outputpath` is the desired location for the image to be downloaded. `outputpath` defaults to root directory and defaults name of file to download (ex: `r'C:\Users\<user>\download.jpeg'`). File extension is also needed in `outputpath` if declared (ex: `r'C:\Users\<user>\image.jpeg'`)

   **Example:**
   
     interface.download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512, img_format='png', download=True, outputpath=r'C:\Users\<user>\image.jpeg')

## Kwargs:

#### legacyid (str):

  The `legacyid` is the archive identifier of the desired browse image

   **Example:**
   
     interface.download_image(legacyid='104001007396EC00')

