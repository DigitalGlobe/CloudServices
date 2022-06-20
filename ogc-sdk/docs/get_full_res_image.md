# Download Full Resolution Image

## Args:


#### featureid (str) (required):

  The featureid is the online id of the desired image feature
  
   **Example:**
   
     get_full_res_image(featureid=`featureid/catalogid`)
	 
#### thread_number (int):

  The number of threads used in the download process. More threads will generally go faster but use more system resources. Defaults to 100 threads.

   **Example:**
   
     get_full_res_image(featureid=`featureid/catalogid`, thread_number=200)
	 
#### bbox (str):

  A bbox (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate) for
  projection EPSG:4326
  
   **Example:**
   
     get_full_res_image(featureid=`featureid/catalogid`, bbox="39.7530, -104.9962, 39.7580, -104.9912")
	 
#### mosaic (bool):

  Flag to create mosaic image from downloaded files (defaults to False)
  
   **Example:**
   
     get_full_res_image(featureid=`featureid/catalogid`, mosaic=True)
	 
	 
## Kwargs:	 
	 

#### outputdirectory (str):

  The outputdirectory is the desired location for the image to be downloaded. outputdirectory defaults to root directory and defaults name of file to download (ex: C:\Users\<user>\download.jpeg). File extension is also needed in outputpath if declared (ex: r'C:\Users\<user>\image.jpeg')

   **Example:**
   
     get_full_res_image(featureid=`featureid/catalogid`, outputdirectory=`output_location`)

#### img_format (str):

  The img_format is the desired format of the returned object. Available options include **jpeg**, **png**, or **geotiff**

   **Example:**
     get_full_res_image(featureid=`featureid/catalogid`, img_format='jpeg')