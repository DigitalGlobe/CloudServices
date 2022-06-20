# Search

## Args:

#### bbox (str):
  A bbox (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate). Must be in projection EPSG:4326

   **Example:**
   
     search(bbox="39.7530, -104.9962, 39.7580, -104.9912")

#### filter (str):

  A filter is a CQL filter using Common Query Language to refine data of search. Further CQL parameters accepted by Maxar can be
  found here: [Filters](https://securewatchdocs.maxar.com/en-us/Miscellaneous/DevGuides/Common_Query_Language/Query.htm?Highlight=cql_)

   **Examples:**
   
     search(filter="(acquisitionDate>='2022-01-01')")
     
	 search(filter="(acquisitionDate>='2022-01-01')AND(cloudCover<0.20)")

     search(bbox="39.7530, -104.9962, 39.7580, -104.9912", filter="(acquisitionDate>='2022-01-01')AND(cloudCover<0.20)")

   *  
      If a bbox is desired, the bbox string is an argument separate from the filter string. This bbox must be in EPSG:4326.
      Search parameters must be wrapped in parentheses within the filter string
	  
#### shapefile (bool):

  Binary of whether or not to return as shapefile format
  
   **Example:**
   
     search(bbox="39.7530, -104.9962, 39.7580, -104.9912", shapefile=True)


## Kwargs:
  

#### featureprofile (str): 
  
  A featureprofile, or stacking profile, is defined based upon the attributes that are most important to the user. The stacking
  profile is used to assemble the features into a mosaic that best satisfies the desired preference. If a profile is not specified, it 
  will default to Default_Profile. A list of available stacking profiles can be found here: [Stacking Profiles](https://securewatchdocs.maxar.com/en-us/Miscellaneous/DevGuides/Stacking_Profiles/stack_profiles.htm)

   **Example:**
	
      search(bbox="39.7530, -104.9962, 39.7580, -104.9912", featureprofile='Cloud_Cover_Profile')
	  
#### typename (str):

  The typename of the desired feature type. Available feature types can be found here: [Feature Types](https://securewatchdocs.maxar.com/en-us/Miscellaneous/DevGuides/WFS/WFS_Feature.htm#WFSServiceDetails)
  
   **Example:**
   
     search(bbox="39.7530, -104.9962, 39.7580, -104.9912", typename="MaxarCatalogMosaicProducts")