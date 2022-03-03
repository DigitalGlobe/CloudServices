**Metadata**
=============

Kwargs that can be passed in:

 *bbox (str)*

  A ``bbox`` (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate) for
  projection EPSG:4326 or minx,miny,maxx,maxy,EPSG:3857 for projection EPSG:3857. Other projections are not supported at this time

   **Example:**
     ``metadata(bbox="39.7530, -104.9962, 39.7580, -104.9912")``

     ``metadata(bbox="-11688123.519228712,4830113.564872338,-11687566.921774745,4830837.565406834,EPSG:3857")``

 *featureid (str)*

  The ``featureid`` is the online id of the desired image feature

   **Example:**
     ``metadata(featureid='d330c2f9486b4b5b0798b142fd1e6388')``