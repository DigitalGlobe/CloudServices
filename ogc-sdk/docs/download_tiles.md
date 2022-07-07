# Download Tiles


## Args:

#### bbox (str):

  A `bbox` (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate) for
  projection EPSG:4326

   **Example:**  

     interface.download_tiles(bbox="39.7530, -104.9962, 39.7580, -104.9912")


#### zoom_level (int):

  The `zoom_level` is the desired scale of the image

   **Example:**  

     interface.download_tiles(bbox="39.7530, -104.9962, 39.7580, -104.9912", zoom_level=15, img_format='png')

   
     

#### img_format (str):

  The `img_format` is the desired format of the returned object. Available options include **jpeg**, **png**, or **geotiff**

   **Example:**  

     interface.download_tiles(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512, img_format='png')

#### outputpath (str):
 
 The `outputpath` is the desired location for the image to be downloaded. `outputpath` defaults to root directory and defaults name of file to download . File extension is also needed in `outputpath` if declared (ex: `r'C:\Users\<user>\image.jpeg'`)
	
   **Example:**  

	 outputpath=r'C:\Users\<user>\download.jpeg'

#### display (bool):

  The `display` is a boolean to determine if a preview of the image is displayed in a Jupyter notebook. Default value is False

   **Example:**  

     interface.download_tiles(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512, img_format='png', download=True, outputpath=r'C:\Users\<user>\image.jpeg')
