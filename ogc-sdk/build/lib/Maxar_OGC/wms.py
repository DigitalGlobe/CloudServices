import requests
import Maxar_OGC.process as process



class WMS:
    def __init__(self, session):
        self.base_url = session['base_url'] + "mapservice/wmsaccess"
        self.headers = session['headers']
        self.connect_id = session['connectid']
        self.response = None
        self.version = session['version']
        self.querystring = self._init_querystring()



    def return_image(self, **kwargs):
        """
        Function finds the imagery matching a bbox or feature id
        Kwargs:
            bbox = String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            filter = CQL filter used to refine data of search.
            height = Integer value representing the vertical number of pixels to return
            width = Integer value representing the horizontal number of pixels to return
            layers = String representing the called upon layer. Defaults to 'DigitalGlobe:Imagery'
            format = String of the format of the response image either jpeg, png or geotiff
            featureprofile = String of the desired stacking profile. Defaults to account Default
        Returns:
            requests response object of desired image
        """
        if kwargs['width'] < 0 or kwargs['width'] > 8000:
            raise Exception("Invalid value for width parameter (max 8000)")
        if kwargs['height'] < 0 or kwargs['height'] > 8000:
            raise Exception("Invalid value for height parameter (max 8000)")
        self.querystring = self._init_querystring()
        keys = list(kwargs.keys())
        if 'bbox' in keys:
            process._validate_bbox(kwargs['bbox'])
            self.querystring.update({'bbox': kwargs['bbox']})
        else:
            raise Exception('Search function must have a BBOX.')
        if 'filter' in keys:
            self.querystring.update({'coverage_cql_filter': kwargs['filter']})
            del (kwargs['filter'])
        for key, value in kwargs.items():
            self.querystring[key] = value
        request = requests.get(self.base_url, headers=self.headers, params=self.querystring)
        self.response = request
        return process._response_handler(self.response)

    def _init_querystring(self):
        querystring = {'connectid': self.connect_id,
                       'service': 'WMS',
                       'request': 'GetMap',
                       'version': '1.3.0',
                       'crs': 'EPSG:4326',
                       'height': '512',
                       'width': '512',
                       'layers': 'DigitalGlobe:Imagery',
                       'format': 'image/jpeg',
                       'SDKversion': '{}'.format(self.version)
                       }
        return querystring
