# Get Full Resolution Image

Args that can be passed in:


## featureid (str)

  The featureid is the online id of the desired image feature
   **Example:**
     get_full_res_image(featureid='57d0e26239dde11463d31ff0893ce9ca', outputdirectory=self.pwd) )
	 
## thread_percentage (int)

  The thread_percentage percentage of total tiles returned per thread. Add more about threading. Possibly hardcoding this. 

   **Example:**
   
     download_browse_image(input_id=`featureid/catalogid`, img_format='png')
	 
## bbox (str) (required)

  A bbox (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate) for
  projection EPSG:4326
  
   **Example:**
   
     get_full_res_image(bbox="39.7530, -104.9962, 39.7580, -104.9912")
	 

## outputdirectory (str)

  The outputdirectory is the desired location for the image to be downloaded. outputdirectory defaults to root directory and defaults name of file to download (ex: C:\Users\<user>\download.jpeg). File extension is also needed in outputpath if declared (ex: r'C:\Users\<user>\image.jpeg')

   **Example:**
   
     get_full_res_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", outputdirectory=`output_location`)

## img_format (str)

  The img_format is the desired format of the returned object. Available options include **jpeg**, **png**, or **geotiff**

   **Example:**
     download_image_by_pixel_count(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512", img_format='png')