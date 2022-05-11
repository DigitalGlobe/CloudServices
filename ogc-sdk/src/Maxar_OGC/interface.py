import os

from Maxar_OGC.auth import Auth
from Maxar_OGC.wms import WMS
from Maxar_OGC.wfs import WFS
from Maxar_OGC.wmts import WMTS
from Maxar_OGC.wcs import WCS
import Maxar_OGC.process as process
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

    def search(self, bbox=None, filter=None, shapefile=False, **kwargs):
        """
        Function searches using the wfs method.
        Args:
            bbox = String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            filter = CQL filter used to refine data of search.
            shapefile = Binary of whether or not to return as shapefile format
        Kwargs:
            featureprofile = String of the desired stacking profile. Defaults to account Default
        Returns:
            Response is either a list of features or a shapefile of all features and associated metdata.
        """

        if shapefile:
            result = self.wfs.search(bbox=bbox, filter=filter, outputformat='shape-zip', **kwargs)
        else:
            result = self.wfs.search(bbox=bbox, filter=filter, **kwargs)
        if bbox:
            if shapefile:
                return process.download_file(result, format_response='zip')
            else:
                result = process.aoi_coverage(bbox, result)
                return result['features']
        else:
            if shapefile:
                return process.download_file(result, format_response='zip')
            else:
                return result.json()['features']

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

    def download_browse_image(self, input_id, img_format='jpeg', outputpath=None, display=False):
        """
        Function downloads the browse image for the desired legacy id
        Args:
            input_id: String of the desired input id (Can be feature id or catalog id)
            img_format: String of the format of the response image either jpeg, png or geotiff
            outputpath: String of output path must include output format. Downloaded path default is user home path.
            display: Boolean to display image in IDE (Jupyter Notebooks only)
        Returns:
            Downloaded image location of desired legacy id in desired format
        """

        legacyid = self._convert_feature_to_legacy(input_id)
        process._check_image_format(img_format)
        url = "https://api.discover.digitalglobe.com/show?id={}".format(legacyid)
        result = requests.request("GET", url, headers={}, data={})
        if display:
            process._display_image(result)
        if outputpath:
            file_name = process.download_file(result, download_path=outputpath)
        else:
            file_name = process.download_file(result, format_response=img_format)
        return f"Downloaded file {file_name}"

    def get_tile_list_with_zoom(self, bbox, zoom_level):
        """
        Function acquires a list of tile calls dependent on the desired bbox and zoom level
        Args:
            bbox: String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            zoom_level: Integer value of the zoom level
        Returns:
            List of individual tile calls for desired bbox and zoom level
        """

        process._validate_bbox(bbox)
        wmts_list = self.wmts.wmts_bbox_get_tile_list(zoom_level, bbox)
        return wmts_list

    def download_tiles(self, bbox, zoom_level, img_format='jpeg', outputpath=None, display=False):
        """
        Function downloads all tiles within a bbox dependent on zoom level
        Args:
            bbox: String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            zoom_level: Integer value of the zoom level
            img_format: String of the format of the response image either jpeg, png or geotiff
            outputpath: String of output path must include output format. Downloaded path default is user home path.
            display: Boolean to display image in IDE (Jupyter Notebooks only)
        Returns:
            Message displaying success and location of downloaded tiles
        """

        wmts = self.get_tile_list_with_zoom(bbox, zoom_level)[1]
        if outputpath:
            extension = outputpath.split(".")[-1]
            base_file = outputpath.replace("." + extension, "")
        else:
            extension = img_format
            base_file = os.getcwd() + "\\Download"
        for tile in wmts:
            response = self.wmts.wmts_get_tile(tile[0], tile[1], tile[2])
            if display:
                process._display_image(response)
            filename = "{}_{}_{}_{}.{}".format(base_file, tile[0], tile[1], tile[2], extension)
            with open(filename, 'wb+') as f:
                f.write(response.content)
        return "Download complete, files are located in {}".format(base_file)

    def download_image_with_feature_id(self, bbox, identifier, gridoffsets, img_format='jpeg', outputpath=None):
        """
        Function downloads the image and metadata of desired feature id
        Args:
            bbox: String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            identifier: String of desired feature id
            gridoffsets: Sting of the pixel size to be returned in X and Y dimensions
            img_format: String of the format of the response image either jpeg, png or geotiff
            outputpath: String of output path must include output format. Downloaded path default is user home path.
        Returns:
            Downloaded image location of desired feature id in desired format and associated metadata
        """

        process._check_image_format(img_format)
        result = self.wcs.return_image(bbox, identifier, gridoffsets)

        if outputpath:
            file_name = process.download_file(result, download_path=outputpath)
        else:
            file_name = process.download_file(result, format_response=img_format)
        return self.wcs.parse_coverage(file_name)

    def download_image_by_pixel_count(self, bbox, height, width, img_format='jpeg', outputpath=None, display=False,
                                      **kwargs):
        """
        Function downloads the image of desired bbox dependent on pixel height and width
        Args:
            bbox: String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            height: Integer value representing the vertical number of pixels to return
            width: Integer value representing the horizontal number of pixels to return
            img_format: String of the format of the response image either jpeg, png or geotiff
            outputpath: String of output path must include output format. Downloaded path default is user home path.
            display: Boolean to display image in IDE (Jupyter Notebooks only)
        Kwargs:
            filter = CQL filter used to refine data of search.
            featureprofile = String of the desired stacking profile. Defaults to account Default
            bands = List of strings containing the desired band combination of 1-4 items. Requires SWIR 8 Band or
            MS1_MS2
        Returns:
            Downloaded image location of desired bbox dependent on pixel height and width
        """

        img_formatted = process._check_image_format(img_format)
        process._validate_bbox(bbox)
        if width < 0 or width > 8000:
            raise Exception("Invalid value for width parameter (max 8000)")
        if height < 0 or height > 8000:
            raise Exception("Invalid value for height parameter (max 8000)")
        result = self.wms.return_image(bbox=bbox, format=img_formatted, height=height, width=width, **kwargs)
        if display:
            process._display_image(result)

        if outputpath:
            file_name = process.download_file(result, download_path=outputpath)
        else:
            file_name = process.download_file(result, format_response=img_format)
        return f"Downloaded file {file_name}"

    def band_manipulation(self, bbox, featureid, band_combination, height=256, width=256, img_format='jpeg',
                          download=True, outputpath=None):
        """
        Function changes the bands of the feature id passed in.
        Args:
            bbox = String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            featureid = String of the id of the image
            band_combination = List of strings containing the desired band combination of 1-4 items.
            download = boolean of user option to download band manipulation file locally.
            outputpath = String of output path must include output format. Downloaded path default is user home path.
        Returns:
            requests response object of the altered image
        """

        band_string = self._band_check(featureid, band_combination)
        feature_id_filter = "featureId='{}'".format(featureid)
        message = self.download_image_by_pixel_count(bbox, height, width, img_format, outputpath=outputpath, display=False,
                                                     filter=feature_id_filter, bands=band_string)
        return message

    @staticmethod
    def calculate_sqkm(bbox):
        area = process.area_sqkm(bbox)
        return area

    def get_full_res_image(self, featureid, thread_percentage=6, thread_number=100, bbox=None, **kwargs):
        """
        Function takes in a feature id and breaks the image up into 1024x1024 tiles, then places a number of calls
        based on multithreading percentages to return a full image strip in multiple tiles
        Args:
            featureid = String of the id of the image
            thread_percentage = int: whole percent of threads given to multithread functionality
            thread_number = int: number of threads given to multithread functionality
            bbox = String of the aoi coordinates in crs EPSG:4326
        kwargs:
            outputdirectory = string: desired output location for tiles
            image_format = string: desired image format (png or jpeg)
        Returns:
            Finished message with location of tiles
        """

        if bbox:
            process._validate_bbox(bbox)
        wfs_request = self.search(filter="featureId='{}'".format(featureid))
        image_bbox = wfs_request[0]['geometry']['coordinates'][0]
        x_coords = [x[0] for x in image_bbox]
        y_coords = [y[1] for y in image_bbox]

        miny = min(y_coords)
        maxy = max(y_coords)
        minx = min(x_coords)
        maxx = max(x_coords)

        if bbox:
            bbox_order = bbox.split(',')
            miny = max(miny, float(bbox_order[0]))
            maxy = min(maxy, float(bbox_order[2]))
            minx = max(minx, float(bbox_order[1]))
            maxx = min(maxx, float(bbox_order[3]))

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
            Returns:
                Message displaying success and location of downloaded tiles
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
        if 'outputdirectory' not in kwargs.keys():
            outputdirectory = os.path.expanduser('~')
        else:
            outputdirectory = kwargs['outputdirectory']
        with open(os.path.join(outputdirectory, 'Grid_cell_coordinates.txt'), 'w') as grid_coords:
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
            output = os.path.join(outputdirectory, key + ".{}".format(format))
            process.download_file(value, download_path=output)
        return "Finished full image download process, output directory is: {}".format(os.path.split(output)[0])

    def _band_check(self, featureid, band_combination):
        """
        Function checks bands given against a list of valid bands
        Args:
            featureid: String of the id of the image
            band_combination: List of strings containing the desired band combination of 1-4 items.
        Returns:
            String of band combination
        """
        band_check = self.search(filter="featureId='{}'".format(featureid))
        band_check_list = ['MS1_MS2', 'SWIR 8-Band']
        if band_check[0]['properties']['productType'] not in band_check_list:
            raise Exception('Product Type for the image must be either SWIR 8-band or MS1_MS2.')
        band_options = ['R', 'G', 'B', 'C', 'Y', 'RE', 'N', 'N2', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7']
        if len(band_combination) <= 0 or len(band_combination) > 4:
            raise Exception('The number of bands must be greater than 0 and less than or equal to 4.')

        band_string = ','.join([i if i in band_options else 'z' for i in band_combination])

        if 'z' in band_string:
            raise Exception(band_combination + ' is not a valid option.')
        return band_string

    def _convert_feature_to_legacy(self, input_id):
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
            json_return = self.search(filter="featureId='{}'".format(input_id))
            legacy_id = json_return[0]['properties']['legacyId']
        return legacy_id
