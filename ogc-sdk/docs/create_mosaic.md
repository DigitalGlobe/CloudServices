# Create Mosaic

## Args:

#### base_dir (str) (required):

  The base_dir is the root directory containing the image files to be mosaiced.

   **Example:**
   
     base_dir=r"C:\Users\<user>\<directory>"


#### img_size (int):

  The size of the image in pixels (defaults to 1024).

   **Example:**
   
     img_size=1024

#### img_format (str):

  The format of the images downloaded from the get_full_res function (defaults to 'png')
  
   **Example:**
   
     img_format='png'


## Kwargs:

#### outputdirectory (str):

  The outputdirectory is the desired location for the image to be downloaded. outputdirectory defaults to root directory and defaults name of file to download (ex: C:\Users\<user>\merged_image.png).

   **Example:**
   
     create_mosaic(base_dir=`base_dir`, img_size=1024, img_format='png', outputdirectory=`outputdirectory`)