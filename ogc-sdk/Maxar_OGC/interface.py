import os

import ogc.process
from ogc.auth import Auth
from ogc.wms import WMS
from ogc.wfs import WFS
from ogc.wmts import WMTS
from ogc.wcs import WCS
import ogc.process as process
import requests
import warnings
from multiprocessing.dummy import Pool as ThreadPool
import sys
warnings.filterwarnings("ignore")


class Interface:
    """
    The primary interface for interacting with the WMS and WFS OGC classes.
    Args:
        base_url = String of the url that you are using ex. 'https://securewatch.digitalglobe.com/'
        connect_id = String of the connectId tied to your account
        username = String of the username if your connectId requires Auth
        Password = String of the password associated with your username
    """
    def __init__(self, *args):
        if len(args) > 0:
            try:
                base_url = args[0]
                connect_id = args[1]
            except:
                raise Exception("Must pass connectId with base_url")
            if len(args) == 4:
                username = args[2]
                password = args[3]
                self._session = Auth(base_url, connect_id, username, password).session_object
            else:
                self._session = Auth(base_url, connect_id).session_object
        else:
            self._session = Auth().session_object

        self.wms = WMS(self._session)
        self.wfs = WFS(self._session)
        self.wmts = WMTS(self._session)
        self.wcs = WCS(self._session)

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
        result = self.wfs.search(**kwargs)
        if "outputformat" not in kwargs.keys():
            return result.json()
        else:
            return result.text

    def download_image(self, bbox=None, height=None, width=None, img_format=None, identifier=None,
                       gridoffsets=None, zoom_level=None, download=True, outputpath=None, display=True,
                       **kwargs):
        """
        Function downloads the image using the wms method.
        Args:
            bbox = String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            height = Integer value representing the vertical number of pixels to return
            width = Integer value representing the horizontal number of pixels to return
            img_format = String of the format of the response image either jpeg, png or geotiff
            identifier = String of the feature id
            gridoffsets = Sting of the pixel size to be returned in X and Y dimensions
            zoom_level = integer value of the zoom level. Used for WMTS
            download = boolean of user option to download band manipulation file locally.
            outputpath = String of output path must include output format. Downloaded path default is user home path.
        Kwargs:
            legacyid = String of the duc id to download the browse image
            crs = String of the Coordinate reference system used. Defaults to EPSG:4326
        Returns:
            requests response object or downloaded file path
        """
        acceptable_format = ['jpeg', 'png', 'geotiff']
        if img_format in acceptable_format:
            img_formatted = 'image/' + img_format
        else:
            raise Exception('Format not recognized, please use acceptable format for downloading image.')
        if 'legacyid' in kwargs.keys():
            legacy_id = kwargs['legacyid']
            url = "https://api.discover.digitalglobe.com/show?id={}".format(legacy_id)
            result = requests.request("GET", url, headers={}, data={})
        elif zoom_level:
            if not bbox:
                raise Exception('zoom_level must have a bbox')
            else:
                process._validate_bbox(bbox)
                wmts_list = self.wmts.wmts_bbox_get_tile_list(zoom_level, bbox)
                return wmts_list
        elif identifier:
            if not gridoffsets or not bbox:
                raise Exception('Identifiers must have gridoffset and bbox')
            else:
                result = self.wcs.return_image(bbox, identifier, gridoffsets)
                if outputpath:
                    file_name = process.download_file(result, download_path=outputpath)
                else:
                    file_name = process.download_file(result, format_response=img_format)
                return self.wcs.parse_coverage(file_name)
        else:
            if not bbox or not img_format or not width or not height:
                raise Exception('height/width must have a bbox and an img_format')
            else:
                process._validate_bbox(bbox)
                if width < 0 or width > 8000:
                    raise Exception("Invalid value for width parameter (max 8000)")
                if height < 0 or height > 8000:
                    raise Exception("Invalid value for height parameter (max 8000)")
                result = self.wms.return_image(bbox=bbox, format=img_formatted, height=height, width=width, **kwargs)
        if display:
            process._display_image(result)
        if download:
            if outputpath:
                file_name = process.download_file(result, download_path=outputpath)
            else:
                file_name = process.download_file(result, format_response=img_format)
            return f"Downloaded file {file_name}"
        else:
            return result

    def metadata(self, bbox=None, featureid=None):
        """
        Function searches using the wfs method for meta data of a desired feature id or bbox.
        Kwargs:
            bbox = String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            featureid = String of the id of the image
        Returns:
            Returns json of metadata of desired bbox or featureid
        """
        if bbox and featureid:
            raise Exception('Can only have a bbox or featureid, not both.')
        if bbox:
            search = self.wfs.search(bbox=bbox, showtherasterreturned='True')
            return search.json()
        if featureid:
            search_value = self.wfs.search(filter="featureId='{}'".format(featureid))
            return search_value.json()

    def band_manipulation(self, bbox, featureid, band_combination, download=True, **kwargs):
        """
        Function changes the bands of the feature id passed in.
        Args:
            bbox = String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            featureid = String of the id of the image
            band_combination = List of strings containing the desired band combination of 1-4 items.
            download = boolean of user option to download band manipulation file locally.
        Kwargs:
            outputpath = String of output path must include output format. Downloaded path default is user home path.
            crs = String of the Coordinate reference system used. Defaults to EPSG:4326
        Returns:
            requests response object of the altered image
        """
        band_check = self.metadata(featureid=featureid)
        band_check_list = ['MS1_MS2', 'SWIR 8-Band']
        if band_check['features'][0]['properties']['productType'] not in band_check_list:
            raise Exception('Product Type for the image must be either SWIR 8-band or MS1_MS2.')
        band_options = ['R', 'G', 'B', 'C', 'Y', 'RE', 'N', 'N2', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7']
        if len(band_combination) <= 0 or len(band_combination) > 4:
            raise Exception('The number of bands must be greater than 0 and less than or equal to 4.')
        band_string = ''
        for band in band_combination:
            if band in band_options:
                band_string = band_string + band + ','
            else:
                raise Exception(band + ' is not a valid option.')
        band_string = band_string[:-1]
        feature_id_filter = "featureId='{}'".format(featureid)
        if 'format' in kwargs.keys():
            variable_format = kwargs['format']
            del kwargs['format']
        else:
            variable_format = 'jpeg'
        if 'height' in kwargs.keys():
            variable_height = kwargs['height']
            del kwargs['height']
        else:
            variable_height = 256
        if 'width' in kwargs.keys():
            variable_width = kwargs['width']
            del kwargs['width']
        else:
            variable_width = 256
        message = self.download_image(bbox=bbox, filter=feature_id_filter, bands=band_string, transparent=True,
                            img_format=variable_format, height=variable_height, width=variable_width, download=download,
                            **kwargs)
        return message

    def discover_browse(self, input_id, download=True, outputpath=None):
        """
        Function takes in a feature id or legacy id and finds the browse image associated with it.
        Args:
            input_id = String of the id that you are searching for
            download = boolean of user option to download band manipulation file locally.
            outputpath = String of output path must include output format. Downloaded path default is user home path.
        Returns:
            requests response object of the browse image
        """
        catalog_identifiers = ['101', '102', '103', '104', '105', '106']

        # if the id passed in is a cat id or WVO4 Inv id. Return the browse for that id from discover api
        if input_id[0:3] in catalog_identifiers or '-inv' == input_id[-4:]:
            legacy_id = input_id
        # If the id passed in is a feature id. Use our wfs method to return a json and parse out the legacy id from
        # the metadata
        else:
            json_return = self.metadata(featureid=input_id)
            legacy_id = json_return['features'][0]['properties']['legacyId']

        response = self.download_image(img_format='jpeg', download=download, outputpath=outputpath,
                                       legacyid=legacy_id)

        return response

    @staticmethod
    def calculate_sqkm(bbox):
        area = process.area_sqkm(bbox)
        return area

    def get_full_res_image(self, featureid, thread_percentage=6, thread_number=100, **kwargs):
        """
        Function takes in a feature id and breaks the image up into 1024x1024 tiles, then places a number of calls
        based on multithreading percentages to return a full image strip in multiple tiles
        Args:
            featureid = string: feature id of desired image
            thread_percentage = int: whole percent of threads given to multithread functionality
            thread_number = int: number of threads given to multithread functionality
        kwargs:
            output_location = string: desired output location for tiles
            image_format = string: desired image format (png or jpeg)
        Returns:
            Finished message with location of tiles
        """
        wfs_request = self.search(filter="featureId='{}'".format(featureid))
        image_bbox = wfs_request['features'][0]['geometry']['coordinates'][0]
        x_coords = [x[0] for x in image_bbox]
        y_coords = [y[1] for y in image_bbox]
        bbox = '{},{},{},{}'.format(min(y_coords), min(x_coords), max(y_coords), max(x_coords))
        miny = min(y_coords)
        maxy = max(y_coords)
        minx = min(x_coords)
        maxx = max(x_coords)
        y_list = []
        x_list = []
        while miny < maxy:
            y_list.append(miny)
            miny += 0.0042176
        while minx < maxx:
            x_list.append(minx)
            minx += 0.0054932
        tiles = {}
        for y in reversed(range(len(y_list) - 1)):
            for x in range(len(x_list) - 1):
                tiles['c{}_r{}'.format(x,len(y_list)-y-2)] = '{}, {}, {}, {}'.format(y_list[y], x_list[x],
                                                                       y_list[y + 1], x_list[x + 1])

        print("Started full image download process...")

        url = self.wms.base_url
        headers = self.wms.headers
        querstring = self.wms.querystring
        querstring['width'] = 1024
        querstring['height'] = 1024
        querstring['coverage_cql_filter'] = "featureId='{}'".format(featureid)
        if 'image_format' in kwargs.keys():
            format = kwargs['image_format']
            querstring['format'] = 'image/{}'.format(format)
        else:
            format = querstring['format'][6:]
        response_times = {}

        def task_to_run(coord_list):
            """
            Function multithreads requests to speed up image return process
            Args:
                coord_list = List of coordinates for individual tiles
            """
            bbox, grid_cell_location = coord_list.split("|")
            querstring['bbox'] = bbox
            response = requests.request("GET", url, params=querstring, headers=headers)
            response_times[grid_cell_location] = response

            i = len(list(response_times.keys()))
            l = len(multithreading_array)
            total_image = (i * 10) // l
            total_space = 10 - total_image
            percent = (i * 100) // l
            if percent % 10 == 0:
                sys.stdout.write('{}'.format('.' * total_image))
                sys.stdout.write('\r')

        div = len(tiles) * (0.01 * thread_percentage)
        num = int(div) + 1
        if num > thread_number:
            num = thread_number
        multithreading_array = ["{}|{}".format(k, j) for j, k in list(tiles.items())]
        if 'output_location' not in kwargs.keys():
            output_location = os.path.expanduser('~')
        else:
            output_location = kwargs['output_location']
        with open(os.path.join(output_location, 'Grid_cell_coordinates.txt'), 'w') as grid_coords:
            grid_coords.write('grid_cell_name | grid_cell_bbox\n')
            for line in multithreading_array:
                value, key = line.split('|')
                grid_coords.write('{} | {}\n'.format(key, value))
        pool = ThreadPool(num)
        results = pool.map(task_to_run, multithreading_array)
        pool.close()
        pool.join()
        sys.stdout.write('\r')
        print('\n')
        sys.stdout.write('Finished raw download')

        for key, value in response_times.items():
            output = os.path.join(output_location, key + ".{}".format(format))
            ogc.process.download_file(value, download_path=output)
        return "Finished full image download process, output directory is: {}".format(os.path.split(output)[0])
