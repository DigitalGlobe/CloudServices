# Download Full Resolution Image

## Args:


#### featureid (str) (required):

  The `featureid` is the online id of the desired image feature
  
   **Example:**
   
     interface.get_full_res_image(featureid='932f7992a4d86a9ca412c024c22792ce')
	 
#### thread_number (int):

  The number of threads used in the download process. More threads will generally go faster but use more system resources. Defaults to 100 threads.

   **Example:**
   
     interface.get_full_res_image(featureid='932f7992a4d86a9ca412c024c22792ce', thread_number=200)
	 
#### bbox (str):

  A `bbox` (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate) for
  projection EPSG:4326
  
   **Example:**
   
     interface.get_full_res_image(featureid='932f7992a4d86a9ca412c024c22792ce', bbox="39.7530, -104.9962, 39.7580, -104.9912")
	 
#### mosaic (bool):

  Flag to create mosaic image from downloaded files (defaults to False)
  
   **Example:**
   
     interface.get_full_res_image(featureid='932f7992a4d86a9ca412c024c22792ce', mosaic=True)
	 
#### img_size (int):

	Resolution of individual images in pixels (img_size x img_size). Defaults to 1024
	
	**Example:**
	
	 interface.get_full_res_image(featureid='932f7992a4d86a9ca412c024c22792ce', img_size=512)
	 
	 
## Kwargs:	 
	 

#### outputdirectory (str):

  The `outputdirectory` is the desired location for the image to be downloaded. `outputdirectory` defaults to root directory and defaults name of file to download (ex: `r'C:\Users\<user>\download.jpeg'`). File extension is also needed in `outputpath` if declared (ex: `r'C:\Users\<user>\image.jpeg'`)

   **Example:**
   
     interface.get_full_res_image(featureid='932f7992a4d86a9ca412c024c22792ce', outputdirectory=r'C:\Users\<user>\download.jpeg')

#### img_format (str):

  The `img_format` is the desired format of the returned object. Available options include **jpeg**, **png**, or **geotiff**

   **Example:**
   
     interface.get_full_res_image(featureid='932f7992a4d86a9ca412c024c22792ce', img_format='jpeg')