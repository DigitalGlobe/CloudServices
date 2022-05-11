# Band Manipulation


Args that can be passed in:

## bbox (str) (required)

  A ``bbox`` (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate). Other projections are not supported at this time

   **Example:**
   
     bbox="39.7530, -104.9962, 39.7580, -104.9912"


## featureid (str) (required)

  The ``featureid`` is the online id of the desired image feature

   **Example:**
   
     featureid='d330c2f9486b4b5b0798b142fd1e6388'

## band_combination (list) (required)

  The ``band_combination`` is a list of strings containing the desired band combination of 1-4 items. Available options include:

   * R
   * G
   * B
   * C
   * Y
   * RE
   * N
   * N2
   * S1
   * S2
   * S3
   * S4
   * S5
   * S6
   * S7

  Further information about bands can be found here: [Bands](https://securewatchdocs.maxar.com/en-us/Miscellaneous/DevGuides/WMTS/WMTS_GetTile.htm#TheBandsParameter)

   **Example:**
   
     band_combination=['R', 'B', 'G', 'C']

##height(int)

  Desired image ``height`` in pixels. Maximum is 8000.

   **Example:**
     ``download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512)``
##width (int)

  Desired image ``width`` in pixels. Maximum is 8000.

   **Example:**
     ``download_image(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512)``

##img_format

  The ``img_format`` is the desired format of the returned object. Available options include **jpeg**, **png**, or **geotiff**

   **Example:**
   
     band_manipulation(bbox="39.7530, -104.9962, 39.7580, -104.9912", height=512, width=512, img_format='png')

## outputpath (str)

  The ``outputpath`` is the desired location for the image to be downloaded. ``outputpath`` defaults to root directory and defaults name of file 
  to download (ex: C:\Users\<user>\download.jpeg). File extension is also needed in ``outputpath`` if declared (ex: ``r'C:\Users\<user>\image.jpeg'``)

   **Example:**
   
     band_manipulation(bbox="39.7530, -104.9962, 39.7580, -104.9912", featureid='d330c2f9486b4b5b0798b142fd1e6388', band_combination=['R', 'B', 'G', 'C'], download=True, outputpath=r'C:\Users\<user>\image.jpeg')