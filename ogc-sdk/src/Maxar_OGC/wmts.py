import requests
import xml.etree.ElementTree as ET
import Maxar_OGC.process as process
import math
from pyproj import transform, Proj

class WMTS:
    def __init__(self, session):
        self.base_url = session['base_url'] + "earthservice/wmtsaccess"
        self.headers = session['headers']
        self.connect_id = session['connectid']
        self.response = None
        self.version = session['version']
        self.querystring = self._init_querystring()

    def wmts_convert(self, zoom_level, laty, longx, crs="EPSG:4326"):
        """
        Function converts a lat long position to the tile column and row needed to return WMTS imagery over the area
        Args:
            zoom_level: Integer value of the desired zoom level
            laty: Integer value of the latitude
            longx: Integer value of the desired longitude
            crs (string) = Desired projection. Defaults to EPSG:4326
        Returns:
            String values of the Tile Row and the Tile Column
        """
        if crs == 'EPSG:4326':
            querystring = self.querystring
            querystring['request'] = 'GetCapabilities'
            matrixwidth = ''
            matrixheight = ''
            projection = 'EPSG:4326'
            response = requests.request("GET", self.base_url, headers=self.headers, params=querystring)
            response = process._response_handler(response)
            root = ET.fromstring(response.content)
            for TileMatrixSet in root.iter(r'{http://www.opengis.net/wmts/1.0}TileMatrixSet'):
                if len(TileMatrixSet) > 0:
                    for i in range(2, 23):
                        if TileMatrixSet[i][0].text == projection + ':' + str(zoom_level):
                            matrixwidth = TileMatrixSet[i][5].text
                            matrixheight = TileMatrixSet[i][6].text
            if not matrixwidth or not matrixheight:
                raise Exception('Unable to determine Matrix dimensions from input coordinates')

            return str(round((float(longx) + 180) * (int(matrixwidth)/360))), str(round((90 - float(laty)) * (int(matrixheight)/180)))
        else:
            inProj = Proj(init=crs)
            outProj = Proj(init='epsg:4326')
            x2, y2 = transform(inProj, outProj, longx, laty)

            def deg2num(lat_deg, lon_deg, zoom):
                lat_rad = math.radians(lat_deg)
                n = 2.0 ** zoom
                xtile = int((lon_deg + 180.0) / 360.0 * n)
                ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
                return (str(xtile), str(ytile))

            tiles = deg2num(y2, x2, zoom_level)
            return tiles

    def wmts_get_tile(self, tilerow, tilecol, zoom_level, crs="EPSG:4326", **kwargs):
        """
        Function executes the wmts call and returns a response object of the desired tile
        Args:
            tilerow: String value of the tile row.
            tilecol: String value of the tile column
            zoom_level: Integer value of the desired zoom level
            crs (string) = Desired projection. Defaults to EPSG:4326
        Returns:
            WMTS tiles for the input data
        """

        querystring = self.querystring
        if crs != "EPSG:4326":
            querystring['TileMatrixSet'] = crs
        querystring['TileMatrix'] = querystring['TileMatrixSet'] + ':' + str(zoom_level)
        querystring['tilerow'] = tilerow
        querystring['tilecol'] = tilecol
        querystring['request'] = 'GetTile'
        response = requests.request("GET", self.base_url, headers=self.headers, params=self.querystring)
        process_response = process._response_handler(response)
        return process_response

    def wmts_bbox_get_tile_list(self, zoom_level, bbox, crs="EPSG:4326", **kwargs):
        """
        Function takes in a bbox and zoom level to return a list of WMTS calls that can be used to aquire all the wmts
        tiles. Projection is EPSG:4326
        Args:
            zoom_level: Integer value of the desired zoom level
            bbox: String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            crs (string) = Desired projection. Defaults to EPSG:4326
        Returns:
            List of WMTS calls.
        """

        process._validate_bbox(bbox, srsname=crs)
        bbox_list = [i for i in bbox.split(',')]
        miny = float(bbox_list[0])
        minx = float(bbox_list[1])
        maxy = float(bbox_list[2])
        maxx = float(bbox_list[3])

        min_tilerow, min_tilecol = self.wmts_convert(zoom_level, miny, minx, crs)
        max_tilerow, max_tilecol = self.wmts_convert(zoom_level, maxy, maxx, crs)

        if max_tilerow < min_tilerow:
            swap = max_tilerow
            max_tilerow = min_tilerow
            min_tilerow = swap
        if max_tilecol < min_tilecol:
            swap = max_tilecol
            max_tilecol = min_tilecol
            min_tilecol = swap
        tiles = []
        row_col = []

        for i in range(int(min_tilecol), int(max_tilecol) + 1):
            for j in range(int(min_tilerow), int(max_tilerow) + 1):
                querystring = self.querystring
                querystring['request'] = 'GetTile'
                querystring['TileMatrixSet'] = crs
                querystring['TileMatrix'] = querystring['TileMatrixSet'] + ':' + str(zoom_level)
                querystring['TileRow'] = i
                querystring['TileCol'] = j
                tiles.append(self.base_url + '?' + "&".join("{}={}".format(key, value) for key,value in querystring.items()))
                row_col.append((querystring['TileRow'], querystring['TileCol'], zoom_level))
        combined = [tiles, row_col]
        return combined

    def _init_querystring(self):
        querystring = {'connectid': self.connect_id,
                       'service': 'WMTS',
                       'request': 'GetTile',
                       'version': '1.0.0',
                       'TileMatrixSet': 'EPSG:4326',
                       'Layer': 'DigitalGlobe:ImageryTileService',
                       'Format': 'image/jpeg',
                       'SDKversion': '{}'.format(self.version)
                       }
        return querystring

