# Download Browse Image


# input id (str) (Required)

  An input id can be either the feature id or the catalog id of the desired browse image.

   **Example:**
   
     download_browse_image(input_id=desired_featureid, img_format='jpeg', outputpath=output_location, display=True)

# img_format (str)

  The ``img_format`` is the desired format of the returned object. Available options include **jpeg**, **png**, or **geotiff**

   **Example:**
   
     download_browse_image(input_id=`featureid/catalogid`, img_format='png')


# outputpath (str)

  The ``outputpath`` is the desired location for the image to be downloaded. ``outputpath`` defaults to root directory and defaults name of file to download (ex: C:\Users\<user>\download.jpeg). File extension is also needed in outputpath if declared (ex: ``r'C:\Users\<user>\image.jpeg'``)

   **Example:**
   
     download_browse_image(input_id=`desired_featureid`, outputpath=`output_location`)

# display (bool)

  The ``display`` is a boolean to determine if a preview of the image is displayed in a Jupyter notebook. Default value is ``False``
  
  **Example:**
  
    download_browse_image(input_id=`desired_featureid`, display=True)