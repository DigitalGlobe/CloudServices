import requests
import ogc.process as process
from pathlib import Path



class WCS:
    def __init__(self, session):
        self.base_url = session['base_url'] + "deliveryservice/wcsaccess"
        self.headers = session['headers']
        self.connect_id = session['connectid']
        self.response = None
        self.version = session['version']
        self.querystring = self._init_querystring()



    def return_image(self, bbox, identifier, gridoffsets, **kwargs):
        """
        Function finds the imagery matching a bbox or feature id
        Kwargs:
            bbox = String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            filter = CQL filter used to refine data of search.
            gridcrs = String of the Coordinate reference system used. Defaults to EPSG:4326.
            gridoffsets = Integer value representing the vertical number of pixels to return
            identifier = String of the feature id to be returned.
            format = String of the format of the response image either jpeg, png or geotiff
            featureprofile = String of the desired stacking profile. Defaults to account Default
        Returns:
            requests response object of desired image
        Notes: Currently only works with EPSG:4326
        """
        self.querystring = self._init_querystring()
        keys = list(kwargs.keys())
        process._validate_bbox(bbox)
        self._build_bbox(bbox)
        self._identifier(identifier)
        self._gridoffsets(gridoffsets)

        if 'filter' in keys:
            self._cql_filter(kwargs['filter'])
            del (kwargs['filter'])
        for key, value in kwargs.items():
            if key in self.querystring.keys():
                self.querystring[key] = value
            else:
                self.querystring.update({key: value})
        request = requests.get(self.base_url, headers=self.headers, params=self.querystring)
        self.response = request
        return process._response_handler(self.response)

    def _gridoffsets(self, gridoffsets):
        self.querystring.update({'gridoffsets': gridoffsets})

    def _identifier(self, identifier):
        self.querystring.update({'identifier': identifier})

    def _build_bbox(self, bbox):
        self.querystring.update({'boundingbox': bbox})

    def _cql_filter(self, filter):
        self.querystring.update({'coverage_cql_filter': filter})

    def _init_querystring(self):
        querystring = {'connectid': self.connect_id,
                       'service': 'WCS',
                       'request': 'GetCoverage',
                       'version': '1.3.0',
                       'gridcrs': 'urn:ogc:def:crs:EPSG::4326',
                       'format': 'image/jpeg',
                       'SDKversion': '{}'.format(self.version)
                       }
        return querystring
    def parse_coverage(self, coverage):
        writelist = []
        filename = Path(coverage)
        filename_replace_ext = filename.with_suffix('.txt')
        with open(coverage, 'rb') as open_file:
            for line in open_file:
                writelist.append(line)
        writelist1 = writelist[:21]
        writelist2 = writelist[21:]
        with open(filename_replace_ext, 'wb') as write_file:
            for item in writelist1:
                write_file.write(item)
        with open(coverage, 'wb') as write_file:
            for item in writelist2:
                write_file.write(item)
        return (str(filename_replace_ext) + " and " + str(coverage) + " have been downloaded")



