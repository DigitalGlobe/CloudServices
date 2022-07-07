# Download Browse Image

## Args:


#### input_id (str) (required):

  An `input_id` can be either the feature id or the catalog id of the desired browse image.

   **Example:**
   
     interface.download_browse_image(input_id='932f7992a4d86a9ca412c024c22792ce', img_format='jpeg', outputpath=output_location, display=True)

#### img_format (str):

  The `img_format` is the desired format of the returned object. Available options include **jpeg**, **png**, or **geotiff**

   **Example:**
   
     interface.download_browse_image(input_id='932f7992a4d86a9ca412c024c22792ce', img_format='png')


#### outputpath (str):

  The `outputpath` is the desired location for the image to be downloaded. `outputpath` defaults to root directory and defaults name of file to download (ex: `r'C:\Users\<user>\download.jpeg'`). File extension is also needed in `outputpath` if declared (ex: `r'C:\Users\<user>\image.jpeg'`)

   **Example:**
   
     interface.download_browse_image(input_id='932f7992a4d86a9ca412c024c22792ce', outputpath=output_location)

#### display (bool):

  The `display` is a boolean to determine if a preview of the image is displayed in a Jupyter notebook. Default value is False
  
  **Example:**
  
    interface.download_browse_image(input_id='932f7992a4d86a9ca412c024c22792ce', display=True)