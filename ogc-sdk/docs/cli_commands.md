# Command Line Interface
After downloading the Maxar_OGC library, open a terminal session and activate the python environment the library exists in

### Create a config file
- In the terminal, enter `config` to begin the setup of a configuration file
- The terminal will prompt you for a desired tenant, connectid, username, and password
- Enter in desired information **NOTE: If authorization is not required for your connectid, hit enter when username and password are prompted to enter in a blank value**

### Reset password in config file
- In the terminal, enter `password` to reset a password in the configuration file
- The terminal will prompt you for a new password
- Enter in desired password

### Search available imagery
- In the terminal, enter `search` followed by the desired flags to refine your search. Available flags can be found by running `search --help`
- Available flags are:
  - `--box`, `-b`: Bounding box. A string of the bounding box of the desired AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
  - `--filter`, `-f`: Filter. A string of a CQL filter used to refine data of search
  - `--shapefile`, `-s`: Shapefile. A boolean operator of whether or not to return found data as a shapefile format
  - `--featureprofile`, `-fp`: Feature profile. A string of the desired stacking profile. Defaults to account Default
  - `--typename`, `-t`: Typename. A string of the typename. Defaults to FinishedFeature. Example input: MaxarCatalogMosaicProducts

For further information on search functionality, see [Search](image_search.md)

### Download available imagery
- In the terminal, enter `download` followed by the desired flags to refine your download. Available flags can be found by running `download --help`
- Available flags are:
  - `--bbox`, `-b`: Bounding box. A string of the bounding box of the desired AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
  - `--height`, `-h`: Height. An integer value representing the vertical number of pixels to return
  - `--width`, `-w`: Width. An integer value representing the horizontal number of pixels to return
  - `--img_format`, `-img`: Image format. A string of the format of the response image in jpeg, png, or geotiff
  - `--identifier`, `-id`: Identifier. A string of the feature id
  - `--gridoffsets`, `-g`: Grid offsets. A string of the pixel size to be returned in X and Y dimensions
  - `--zoom`, `-z`: Zoom level. An integer value of the zoom level. Used for WMTS
  - `--download`, `-d`: Download. A boolean operator for user option to download file locally
  
**NOTE: Structure of calls should be structured with one of the following examples:**
  
	- bbox, zoom_level, img_format
	- bbox, identifier, gridoffsets, img_format
	- bbox, img_format, height, width

For further information on download functionality, see one of the following:

- [Download](download_image.md)
- [Download Browse](download_browse_image.md)
- [Download with Feature Id](download_image_featureid.md)
- [Download by Pixel Count](download_image_pixel_count.md)
- [Download Tiles](download_tiles.md)

### Band manipulation
- In the terminal, enter `bands` followed by the desired flags to refine your band manipulation. Available flags can be found by running `bands --help`
- Available flags are:
  - `--bbox`, `-b`: Bounding box. A string of the bounding box of the desired AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
  - `--featureid`, `-id`: Feature id. A string of the feature id
  - `--band_combination`, `-band`: Band combination. A string of the desired band combination of 1-4 items. Example: "R, G, B"
  - `--height`, `-h`: Height. An integer value representing the vertical number of pixels to return
  - `--width`, `-w`: Width. An integer value representing the horizontal number of pixels to return
  - `--img_format`, `-img`: Image format. A string of the format of the response image in jpeg, png, or geotiff

For further information on band manipulation functionality, see [Band Manipulation](band_manipulation.md)

### Calculate bbox area in SQKM
- In the terminal, enter `area` to determine the size of the desired AOI in SQKM
- The terminal will prompt you for a bounding box
- Enter in desired bounding box
- Alternatively, enter `area` followed by the desired flag to determine the size of the desired AOI in SQKM. Available flag can be found by running `area --help`
- Available flag is:
  - `--bbox`, `-b`: Bounding box. A string of the bounding box of the desired AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
