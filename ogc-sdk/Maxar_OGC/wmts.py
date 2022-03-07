
import requests
import xml.etree.ElementTree as ET
import ogc.process as process


class WMTS:
    def __init__(self, session):
        self.base_url = session['base_url'] + "earthservice/wmtsaccess"
        self.headers = session['headers']
        self.connect_id = session['connectid']
        self.response = None
        self.querystring = self._init_querystring()

    def wmts_convert(self, zoom_level, projection, laty, longx):
        """
        This function converts a lat long position to the tile column and row needed to return WMTS imagery over the
        area
        :param zoom_level: Integer value of the desired zoom level
        :param projection: String value of the Projection Either EPSG:4326, EPSG:3857, or EPSG:3395
        :param laty: Integer value of the latitude
        :param longx:Integer value of the desired longitude
        :return: String values of the Tile Row and the Tile Column
        """
        querystring = self.querystring
        querystring['request'] = 'GetCapabilities'
        matrixwidth = ''
        matrixheight = ''
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
        tiles_per_long = int(matrixwidth)/360
        tiles_per_lat = int(matrixheight)/180
        dX = float(longx) + 180
        dY = 90 - float(laty)
        tilecol = dX * tiles_per_long
        tilerow = dY * tiles_per_lat
        return str(round(tilecol)), str(round(tilerow))

    def wmts_get_tile(self, tilerow, tilecol, zoom_level, **kwargs):
        """
        This function executes the wmts call and returns a response object of the desired tile
        :param tilerow: String value of the tile row.
        :param tilecol: String value of the tile column
        :param zoom_level: Integer value of the desired zoom level
        :return: Returns the WMTS tiles for the input data
        """
        querystring = self.querystring
        if 'projection' in kwargs.keys():
            querystring['TileMatrixSet'] = kwargs['projection']
        querystring['TileMatrix'] = querystring['TileMatrixSet'] + ':' + str(zoom_level)
        querystring['tilerow'] = tilerow
        querystring['tilecol'] = tilecol
        querystring['request'] = 'GetTile'
        response = requests.request("GET", self.base_url, headers=self.headers, params=self.querystring)
        process_response = process._response_handler(response)
        return process_response

    def wmts_bbox_get_tile_list(self, zoom_level, bbox, **kwargs):
        """
        This function takes in a bbox and zoom level to return a list of WMTS calls that can be used to aquire all the
        wmts tiles. If no projection is given default value is EPSG:4326
        :param zoom_level: Integer value of the desired zoom level
        :param bbox:
        :return: List of WMTS calls.
        """

        process._validate_bbox(bbox)
        bbox_list = [i for i in bbox.split(',')]
        if len(bbox_list) == 4:
            miny = float(bbox_list[0])
            minx = float(bbox_list[1])
            maxy = float(bbox_list[2])
            maxx = float(bbox_list[3])
            projection = 'EPSG:4326'
        else:
            raise Exception('Must provide four coordinates in EPSG:4326')
        # elif len(bbox_list) == 5:
        #     minx = float(bbox_list[0])
        #     miny = float(bbox_list[1])
        #     maxx = float(bbox_list[2])
        #     maxy = float(bbox_list[3])
        #     projection = 'EPSG:3857'

        min_tilerow, min_tilecol = self.wmts_convert(zoom_level, projection, miny, minx)
        max_tilerow, max_tilecol = self.wmts_convert(zoom_level, projection, maxy, maxx)
        if max_tilerow < min_tilerow:
            swap = max_tilerow
            max_tilerow = min_tilerow
            min_tilerow = swap
        if max_tilecol < min_tilecol:
            swap = max_tilecol
            max_tilecol = min_tilecol
            min_tilecol = swap
        tiles = []

        for i in range(int(min_tilecol), int(max_tilecol) + 1):
            for j in range(int(min_tilerow), int(max_tilerow) + 1):
                querystring = self.querystring
                querystring['request'] = 'GetTile'
                querystring['TileMatrix'] = querystring['TileMatrixSet'] + ':' + str(zoom_level)
                querystring['TileRow'] = i
                querystring['TileCol'] = j
                tiles.append(self.base_url + '?' + "&".join("{}={}".format(key, value) for key,value in querystring.items()))
        return tiles

    def _init_querystring(self):

        querystring = {'connectid': self.connect_id,
                       'service': 'WMTS',
                       'request': 'GetTile',
                       'version': '1.0.0',
                       'TileMatrixSet': 'EPSG:4326',
                       'Layer': 'DigitalGlobe:ImageryTileService',
                       'Format': 'image/jpeg'
                       }
        return querystring

