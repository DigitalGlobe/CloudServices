# Download Image by Pixel Count

## Args:

#### bbox (str) (required):

  A `bbox` (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate) for
  projection EPSG:4326

   **Example:**
   
     interface.download_image_by_pixel_count(bbox="39.7530, -104.9962, 39.7580, -104.9912")
	 

#### height, width (int) (required):

  Desired image `height` and `width` in pixels. Maximum is 8000.

   **Example:**
   
     interface.download_image_by_pixel_count(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512)

#### img_format (str):

  The `img_format` is the desired format of the returned object. Available options include **jpeg**, **png**, or **geotiff**

   **Example:**
   
     interface.download_image_by_pixel_count(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512", img_format='png')

#### outputpath (str):
  
 The `outputpath` is the desired location for the image to be downloaded. `outputpath` defaults to root directory and defaults name of file to download. File extension is also needed in `outputpath` if declared (ex: `r'C:\Users\<user>\image.jpeg'`)
	
   **Example:**
   
	 outputpath=r'C:\Users\<user>\download.jpeg'

#### display (bool):

  The `display` is a boolean to determine if a preview of the image is displayed in a Jupyter notebook. Default value is False

   **Example:**
   
     interface.download_image_by_pixel_count(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512, img_format='png', outputpath=r'C:\Users\<user>\image.jpeg')
	 
## Kwargs:

#### filter (str):

  A `filter` is a CQL filter using Common Query Language to refine data of search. Further CQL parameters accepted by Maxar can be
  found here: [Filters](https://securewatchdocs.maxar.com/en-us/Miscellaneous/DevGuides/Common_Query_Language/Query.htm?Highlight=cql_)

   **Examples:**
   
     interface.download_image_by_pixel_count(filter="(acquisitionDate>='2022-01-01')")
     
	 interface.download_image_by_pixel_count(filter="(acquisitionDate>='2022-01-01')AND(cloudCover<0.20)")

     interface.download_image_by_pixel_count(bbox="39.7530, -104.9962, 39.7580, -104.9912", filter="(acquisitionDate>='2022-01-01')AND(cloudCover<0.20)")

   *  
      If a bbox is desired, the bbox string is an argument separate from the filter string. This bbox must be in EPSG:4326.
      Search parameters must be wrapped in parentheses within the filter string

#### featureprofile (str): 
  
  A `featureprofile`, or stacking profile, is defined based upon the attributes that are most important to the user. The stacking
  profile is used to assemble the features into a mosaic that best satisfies the desired preference. If a profile is not specified, it 
  will default to Default_Profile. A list of available stacking profiles can be found here: [Stacking Profiles](https://securewatchdocs.maxar.com/en-us/Miscellaneous/DevGuides/Stacking_Profiles/stack_profiles.htm)


   **Example:**
	
      interface.download_image_by_pixel_count(bbox="39.7530, -104.9962, 39.7580, -104.9912", featureprofile='Cloud_Cover_Profile')
	  
#### bands (list):

  The `bands` is a list of strings containing the desired band combination of 1-4 items. For more information visit our [Band Manipulation](band_manipulation.md) page.
