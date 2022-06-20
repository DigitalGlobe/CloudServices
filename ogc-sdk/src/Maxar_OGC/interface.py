import os

from Maxar_OGC.auth import Auth
from Maxar_OGC.wms import WMS
from Maxar_OGC.wfs import WFS
from Maxar_OGC.wmts import WMTS
from Maxar_OGC.wcs import WCS
import Maxar_OGC.process as process
import requests
import warnings
import queue
import concurrent.futures
from concurrent.futures import as_completed
import sys
from PIL import Image


warnings.filterwarnings("ignore")


class Interface:
    """
    The primary interface for interacting with the WMS and WFS OGC classes.
    Args:
        base_url (string) = The url that you are using ex. 'https://securewatch.digitalglobe.com/'
        connect_id (string) = The connectId tied to your account
        username (string) = The username if your connectId requires Auth
        password (string) = The password associated with your username
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
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            filter (string) = CQL filter used to refine data of search.
            shapefile (bool) = Binary of whether or not to return as shapefile format
        Kwargs:
            featureprofile (string) = The desired stacking profile. Defaults to account Default
            typename (string) = The typename of the desired feature type. Defaults to FinishedFeature. Example input
            MaxarCatalogMosaicProducts
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
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            height (int) = The vertical number of pixels to return
            width (int) = The horizontal number of pixels to return
            img_format (string) = The format of the response image either jpeg, png or geotiff
            identifier (string) = The feature id
            gridoffsets (string) = The pixel size to be returned in X and Y dimensions
            zoom_level (int) = The zoom level. Used for WMTS
            download (bool) = User option to download band manipulation file locally.
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
        Kwargs:
            legacyid (string) = The duc id to download the browse image
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
            input_id (string) = The desired input id (Can be feature id or catalog id)
            img_format (string) = The format of the response image either jpeg, png or geotiff
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
            display (bool) = Display image in IDE (Jupyter Notebooks only)
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
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            zoom_level (int) = The zoom level
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
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            zoom_level (int) = The zoom level
            img_format (string) = The format of the response image either jpeg, png or geotiff
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
            display (bool) = Display image in IDE (Jupyter Notebooks only)
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

    def download_image_with_feature_id(self, bbox, identifier, gridoffsets, img_format='jpeg', display=True,
                                       outputpath=None):
        """
        Function downloads the image and metadata of desired feature id
        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            identifier (string) = Desired feature id
            gridoffsets (string) = The pixel size to be returned in X and Y dimensions
            img_format (string) = The format of the response image either jpeg, png or geotiff
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
        Returns:
            Downloaded image location of desired feature id in desired format and associated metadata
        """

        process._check_image_format(img_format)
        result = self.wcs.return_image(bbox, identifier, gridoffsets)

        if display:
            process._display_image(result)

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
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            height (int) = The vertical number of pixels to return
            width (int) = The horizontal number of pixels to return
            img_format (string) = The format of the response image either jpeg, png or geotiff
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
            display (bool) = Display image in IDE (Jupyter Notebooks only)
        Kwargs:
            filter (string) = CQL filter used to refine data of search.
            featureprofile (string) = The desired stacking profile. Defaults to account Default
            bands (list[string]) = The desired band combination of 1-4 items. Requires SWIR 8 Band or MS1_MS2
        Returns:
            Downloaded image location of desired bbox dependent on pixel height and width
        """

        img_formatted = process._check_image_format(img_format)
        process._validate_bbox(bbox)
        if width <= 0 or width > 8000:
            raise Exception("Invalid value for width parameter (max 8000)")
        if height <= 0 or height > 8000:
            raise Exception("Invalid value for height parameter (max 8000)")
        result = self.wms.return_image(bbox=bbox, format=img_formatted, height=height, width=width, **kwargs)
        if display:
            process._display_image(result)

        if outputpath:
            file_name = process.download_file(result, download_path=outputpath)
        else:
            file_name = process.download_file(result, format_response=img_format)
        return "Downloaded file {}".format(file_name)

    def band_manipulation(self, bbox, featureid, band_combination, height=256, width=256, img_format='jpeg',
                          display=True,
                          outputpath=None):
        """
        Function changes the bands of the feature id passed in.
        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            featureid (string) = The id of the image
            band_combination (list[string]) = The desired band combination of 1-4 items.
            height (int) = The vertical number of pixels to return
            width (int) = The horizontal number of pixels to return
            image_format (string) = The file type that you want downloaded.
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
        Returns:
            download location for file
        """

        band_string = self._band_check(featureid, band_combination)
        feature_id_filter = "featureId='{}'".format(featureid)
        message = self.download_image_by_pixel_count(bbox, height, width, img_format, outputpath=outputpath,
                                                     display=display,
                                                     filter=feature_id_filter, bands=band_string)
        return message

    def get_full_res_image(self, featureid, thread_number=100, bbox=None, mosaic=False, **kwargs):
        """
        Function takes in a feature id and breaks the image up into 1024x1024 tiles, then places a number of calls
        based on multithreading percentages to return a full image strip in multiple tiles
        Args:
            featureid (string) = Feature id of the image
            thread_number (int) = Number of threads given to multithread functionality
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            mosaic (bool) = Flag if image files are mosaiced
        kwargs:
            outputdirectory (string) = Desired output location for tiles
            image_format (string) = Desired image format (png or jpeg)
        Returns:
            None
        """

        if bbox:
            process._validate_bbox(bbox)
        wfs_request = self.search(filter="featureId='{}'".format(featureid))
        image_bbox = wfs_request[0]['geometry']['coordinates'][0]
        x_coords = [x[0] for x in image_bbox]
        y_coords = [y[1] for y in image_bbox]

        miny = min(y_coords)
        maxy = max(y_coords) + 0.0042176
        minx = min(x_coords)
        maxx = max(x_coords) + 0.0054932

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

        if len(y_list) == 1:
            if len(x_list) == 1:
                tiles['c{}_r{}'.format(0, 0)] = '{}, {}, {}, {}'.format(y_list[0], x_list[0],
                                                                        y_list[0] + 0.0042176, x_list[0] + 0.0054932)
            else:
                for x in range(len(x_list) - 1):
                    tiles['c{}_r{}'.format(x, 0)] = '{}, {}, {}, {}'.format(y_list[0], x_list[x], y_list[0] + 0.0042176,
                                                                            x_list[x + 1])
        elif len(x_list) == 1:
            for y in reversed(range(len(y_list) - 1)):
                tiles['c{}_r{}'.format(0, len(y_list) - y - 2)] = '{}, {}, {}, {}'.format(y_list[y], x_list[0],
                                                                                          y_list[y + 1],
                                                                                          x_list[0] + 0.0054932)
        else:
            for y in reversed(range(len(y_list) - 1)):
                for x in range(len(x_list) - 1):
                    tiles['c{}_r{}'.format(x, len(y_list) - y - 2)] = '{}, {}, {}, {}'.format(y_list[y], x_list[x],
                                                                                              y_list[y + 1],
                                                                                              x_list[x + 1])

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

        def response_thread(coord_list):
            """
            Function multithreads requests to speed up image return process
            Args:
                coord_list (list) = Coordinates for individual tiles
            Returns:
                List of cell locations and corresponding response objects
            """
            sub_bbox, sub_grid_cell_location = coord_list.split("|")
            sub_query = querstring.copy()
            sub_query['bbox'] = sub_bbox
            sub_response = requests.request("GET", url, params=sub_query, headers=headers)
            return [sub_grid_cell_location, sub_response]


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

        chunk_size = thread_number * 5
        chunk_count = int(len(multithreading_array) / chunk_size)
        for i in range(chunk_count + 1):
            if i == chunk_count:
                sub_array = multithreading_array[i * chunk_size:]
            else:
                sub_array = multithreading_array[i * chunk_size:(i + 1) * chunk_size]
            with process.BoundedThreadPoolExecutor(max_workers=thread_number) as executor:
                futures = [executor.submit(response_thread, coords) for coords in sub_array]
                for future in as_completed(futures):
                    coord, response = future.result()
                    sub_output = os.path.join(outputdirectory, coord + ".{}".format(format))
                    process.download_file(response, download_path=sub_output)
            sys.stdout.write('Finished section {} out of {}'.format(i+1, chunk_count+1))
            sys.stdout.write('\r')
        sys.stdout.write('\r')
        print('\n')

        if mosaic:
            return "Finished full image download process, output directory is: {}. Beginning mosaic process".\
                format(os.path.split(outputdirectory)[0])
            create_mosaic(base_dir=kwargs['outputdirectory'], img_size=1024, img_format=image_format, **kwargs)
        else:
            return "Finished full image download process, output directory is: {}".\
                format(os.path.split(outputdirectory)[0])


    def create_mosaic(self, base_dir, img_size=1024, img_format='png', **kwargs):
        '''
        Function creates a mosaic of downloaded image tiles from full_res_dowload function
        Args:
            base_dir (string) = Root directory containing image files to be mosaiced
            img_size (int) = Size of individual image files, defaults to 1024
            img_format (string) = Image format of files
        Kwargs:
            outputdirectory (string) = Directory destination of finished mosaic file
        Returns:
            None
        '''
        Image.MAX_IMAGE_PIXELS = None
        coord_list = []
        for k in [i for i in os.listdir(base_dir) if ".txt" not in i and os.path.isfile(os.path.join(base_dir, i))]:
            filename = k
            coords = k.replace('c', '').replace('_r', ',').replace('.{}'.format(img_format), '').split(',')
            coord_list.append([filename, int(coords[0]), int(coords[1])])

        max_row = max([i[2] for i in coord_list]) + 1
        max_col = max([i[1] for i in coord_list]) + 1
        maximum = max(max_col, max_row)
        size = img_size * maximum
        mosaic = Image.new('RGB', (max_col * img_size, max_row * img_size), (size, size, size))

        count = 0
        for i in coord_list:
            column = img_size * i[1]
            row = img_size * i[2]
            mosaic.paste(Image.open(os.path.join(base_dir, i[0])), (column, row))
            count += 1
            if count % 100 == 0:
                sys.stdout.write("Processing {} of {} total".format(count, len(coord_list)))
                sys.stdout.write("\r")

        if 'outputdirectory' in kwargs.keys():
            mosaic.save(r"{}\merged_image.{}".format(kwargs['outputdirectory'], img_format))
            sys.stdout.write("Finished image mosaic process, output directory is: {}".format(kwargs['outputdirectory']))
        else:
            mosaic.save(r"{}\merged_image.{}".format(base_dir, img_format))
            sys.stdout.write("Finished image mosaic process, output directory is: {}".format(base_dir))

    def _band_check(self, featureid, band_combination):
        """
        Function checks bands given against a list of valid bands
        Args:
            featureid (string) = The id of the image
            band_combination (list[string]) = The desired band combination of 1-4 items.
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
            input_id (string) = The id that you are searching for
        Returns:
            Legacy id of desired feature
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

    @staticmethod
    def calculate_sqkm(bbox):
        """
        Function calculates the area in square kilometers of the desired bounding box
        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
        Returns:
            Float of bounding box area in square kilometers
        """
        
        area = process.area_sqkm(bbox)
        return area
