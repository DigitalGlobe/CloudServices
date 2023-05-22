import requests
import Maxar_OGC.process as process


class WFS:
    def __init__(self, session):
        self.base_url = session['base_url'] + "catalogservice/wfsaccess"
        self.headers = session['headers']
        self.connect_id = session['connectid']
        self.response = None
        self.version = session['version']
        self.querystring = self._init_querystring()

    def search(self, typename='FinishedFeature', srsname='EPSG:4326', **kwargs):
        """
        Function searches using the wfs method.
        Args:
            typename = String of the typename. Defaults to 'FinishedFeature'. Example input 'MaxarCatalogMosaicProducts'
            srsname (string) = Desired projection. Defaults to EPSG:4326
        Kwargs:
            bbox = String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            filter = CQL filter used to refine data of search.
            outputformat = String of the format of the response object. Defaults to json.
            featureprofile = String of the desired stacking profile. Defaults to account Default
            typename = String of the typename. Defaults to FinishedFeature. Example input MaxarCatalogMosaicProducts
        Returns:
            Response object of the search
        """

        self.querystring = self._init_querystring()
        process._check_typeName(typename)
        self.querystring.update({'typename': 'DigitalGlobe:{}'.format(typename)})
        keys = list(kwargs.keys())
        if 'filter' in keys and kwargs['filter']:
            # process.cql_checker(kwargs.get('filter'))
            if 'bbox' in keys and kwargs['bbox']:
                if srsname == "EPSG:4326":
                    process._validate_bbox(kwargs['bbox'], srsname=srsname)
                    self._combine_bbox_and_filter(kwargs['filter'], kwargs['bbox'], typename)
                    del (kwargs['filter'])
                    del (kwargs['bbox'])
                else:
                    process._validate_bbox(kwargs['bbox'], srsname=srsname)
                    bbox_list = [i for i in kwargs['bbox'].split(',')]
                    self.querystring['srsname'] = srsname
                    srsname = "'" + srsname + "'"
                    kwargs['bbox'] = ",".join([bbox_list[1], bbox_list[0], bbox_list[3], bbox_list[2], srsname])
                    self._combine_bbox_and_filter(kwargs['filter'], kwargs['bbox'], typename)
                    del (kwargs['filter'])
                    del (kwargs['bbox'])
            else:
                if not srsname:
                    self.querystring['srsname'] = "EPSG:4326"
                else:
                    self.querystring['srsname'] = srsname
                self.querystring.update({'cql_filter': kwargs['filter']})
                del (kwargs['filter'])
        elif kwargs['bbox']:
            process._validate_bbox(kwargs['bbox'], srsname=srsname)
            if srsname == "EPSG:4326":
                bbox_list = [i for i in kwargs['bbox'].split(',')]
                kwargs['bbox'] = ",".join([bbox_list[0], bbox_list[1], bbox_list[2], bbox_list[3]])
            else:
                bbox_list = [i for i in kwargs['bbox'].split(',')]
                kwargs['bbox'] = ",".join([bbox_list[1], bbox_list[0], bbox_list[3], bbox_list[2], srsname])
                self.querystring['srsname'] = srsname
        elif 'request' in keys:
            if kwargs['request'] == 'DescribeFeatureType':
                self.querystring.update({'request': kwargs['request']})
                del(kwargs['filter'])
                del(kwargs['bbox'])
                del(self.querystring['outputformat'])
        else:
            raise Exception('Search function must have a BBOX or a Filter.')
        for key, value in kwargs.items():
            self.querystring[key] = value
        query_string = process._remove_cache(self.querystring)
        request = requests.get(self.base_url, headers=self.headers, params=query_string)
        self.response = request
        return process._response_handler(self.response)

    def _combine_bbox_and_filter(self, filter, bbox, typename):
        if 'MaxarCatalogMosaic' in typename:
            bbox_geometry = 'BBOX(shape,{})'.format(bbox)
            combined_filter = bbox_geometry + 'AND' + '(' + filter + ')'
        elif 'PCMChangePolygons' in typename:
            bbox_geometry = 'BBOX(Shape,{})'.format(bbox)
            combined_filter = bbox_geometry + 'AND' + '(' + filter + ')'
        else:
            bbox_geometry = 'BBOX(geometry,{})'.format(bbox)
            combined_filter = bbox_geometry + 'AND' + '(' + filter + ')'
        self.querystring.update({'cql_filter': filter})
        self.querystring.update({'cql_filter': combined_filter})

    def _init_querystring(self):
        querystring = {'connectid': self.connect_id,
                       'service': 'WFS',
                       'request': 'GetFeature',
                       'typename': 'DigitalGlobe:FinishedFeature',
                       'version': '1.1.0',
                       'srsname': 'EPSG:4326',
                       'height': '3000',
                       'width': '3000',
                       'outputformat': 'json',
                       'SDKversion': '{}'.format(self.version)
                       }
        return querystring

