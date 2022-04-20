# Metadata

## bbox (str):
  
  A ``bbox`` (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate) in ESPG 4326. Other projections are not supported at this time

   **Example:**
   
     metadata(bbox="39.7530, -104.9962, 39.7580, -104.9912")

## featureid (str): 
  
  The ``featureid`` is the online id of the desired image feature

   **Example:**
   
     metadata(featureid='d330c2f9486b4b5b0798b142fd1e6388')