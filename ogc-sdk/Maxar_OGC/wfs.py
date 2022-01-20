import requests
import Maxar_OGC.process as process


class WFS:
    def __init__(self, session):
        self.base_url = session['base_url'] + "catalogservice/wfsaccess"
        self.headers = session['headers']
        self.connect_id = session['connectid']
        self.response = None
        self.querystring = self._init_querystring()

    def search(self, **kwargs):
        """
        Function searches using the wfs method.
        Kwargs:
            bbox = String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            filter = CQL filter used to refine data of search.
            crs = String of the Coordinate reference system used. Defaults to EPSG:4326.
            outputformat = String of the format of the response object. Defaults to json.
            featureprofile = String of the desired stacking profile. Defaults to account Default
        Returns:
            Response object of the search
        """
        self.querystring = self._init_querystring()
        keys = list(kwargs.keys())
        if 'filter' in keys:
            if 'bbox' in keys:
                process._validate_bbox(kwargs['bbox'])
                self._combine_bbox_and_filter(kwargs['filter'], kwargs['bbox'])
                del(kwargs['filter'])
            else:
                self._parse_filter(kwargs['filter'])
                del (kwargs['filter'])
        elif 'bbox' in keys:
            process._validate_bbox(kwargs['bbox'])
            self._build_bbox(kwargs['bbox'])
        else:
            raise Exception('Search function must have a BBOX or a Filter.')
        for key, value in kwargs.items():
            if key in self.querystring.keys():
                self.querystring[key] = value
            else:
                self.querystring.update({key: value})

        query_string = process._remove_cache(self.querystring)
        request = requests.get(self.base_url, headers=self.headers, params=query_string)
        self.response = request
        return process._response_handler(self.response)

    def _parse_filter(self, filter):
        self.querystring.update({'cql_filter': filter})

    def _combine_bbox_and_filter(self, filter, bbox):
        bbox_geometry = 'BBOX(geometry,{}'.format(bbox)
        combined_filter = bbox_geometry + 'AND' + filter
        self._parse_filter(combined_filter)

    def _build_bbox(self, bbox):
        self.querystring.update({'bbox': bbox})

    def _init_querystring(self):
        querystring = {'connectid': self.connect_id,
                       'service': 'WFS',
                       'request': 'GetFeature',
                       'typename': 'DigitalGlobe:FinishedFeature',
                       'version': '1.1.0',
                       'srsname': 'EPSG:4326',
                       'height': '3000',
                       'width': '3000',
                       'outputformat': 'json'
                       }
        return querystring
