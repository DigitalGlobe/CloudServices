# Discover Browse


Args that can be passed in:

## input_id (str) - Required
 
  An ``input_id`` is Feature Id or a Legacy Identifier. A Legacy Identifier will start with one of the following prefixes 102, 103, 104, 105, or 106.
  
   **Examples:**
   
     ``input_id="104001007396EC00"`` (Legacy Identifier)

     ``input_id="d330c2f9486b4b5b0798b142fd1e6388"`` (Feature Id)
	 
## download (bool) and outputpath (str)

  The ``download`` is a boolean of whether or not the desired image should be downloaded. ``download`` defaults to true. The ``outputpath`` is the desired location for the image to be downloaded. ``outputpath`` defaults to root directory and defaults name of file to download (ex: C:\Users\<user>\download.jpeg). File extension is also needed in outputpath if declared (ex: ``r'C:\Users\<user>\image.jpeg'``)

   **Example:**
     ``discover_browse(input_id="104001007396EC00", download=True, outputpath=r'C:\Users\<user>\image.jpeg')``