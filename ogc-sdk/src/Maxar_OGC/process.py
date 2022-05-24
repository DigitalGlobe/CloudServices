import os
import pyproj
import shapely.ops as ops
from shapely.geometry.polygon import Polygon
import shapely.geometry
import shapely.wkt
from functools import partial
import random
import string
import queue
from concurrent.futures import ThreadPoolExecutor



def _response_handler(response):
    """
    Function takes in the server response code and responds accordingly.
    Returns:
        requests response object of server status
    """
    if response.status_code != 200:
        raise Exception("Non-200 response received for {}.".format(response.url))
    elif 'Exception' in response.text:
        raise Exception(response.url, response.text)
    else:
        return response


def area_sqkm(bbox):
    """
    Function takes in the bbox and calculates the area in SQKM.
    Args:
        bbox =  String of Coordinates separated by comma
            ex: "39.84387,-105.05608,39.95133,-104.94827"
    Returns:
        float value of area in SQKM
    """

    _validate_bbox(bbox)
    bboxlst = bbox.split(',')
    ymin = float(bboxlst[0])
    ymax = float(bboxlst[2])
    xmin = float(bboxlst[1])
    xmax = float(bboxlst[3])

    geom = Polygon([(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin), (xmin, ymin)])

    geom_area = ops.transform(
    partial(
        pyproj.transform,
        pyproj.Proj(init='EPSG:4326'),
        pyproj.Proj(
            proj='aea',
            lat_1=geom.bounds[1],
            lat_2=geom.bounds[3]
        )
    ),
    geom)

    # Print the area in sqkm^2

    geomareasqkm = geom_area.area/(10**6)
    return geomareasqkm


def _display_image(image):
    """
    Function takes in the response object and displays it.
    Args:
        image = response object from wms method
    """

    try:
        import IPython.display as disp
        from IPython.display import Image, display
    except:
        raise Exception('Must have IPython installed to display.')
    display(disp.Image(image.content))


def _validate_bbox(bbox):
    """
    Function takes in the bbox and validates that it is proper format
    Args:
        bbox =  String of Coordinates separated by comma
        example = "-105.05608, 39.84387, -104.94827, 39.95133"
    """

    bbox_list = [i for i in bbox.split(',')]
    if len(bbox_list) == 4:
        try:
            bbox_data = {'min_y': float(bbox_list[0]), 'min_x': float(bbox_list[1]), 'max_y': float(bbox_list[2]),
                         'max_x': float(bbox_list[3])}
        except:
            raise Exception('Bbox coordiantes must be numeric.')
        if bbox_data['min_y'] >= bbox_data['max_y']:
            raise Exception("Improper order of bbox: min_y is greater than max_y.")
        if bbox_data['min_x'] >= bbox_data['max_x']:
            raise Exception("Improper order of bbox: min_x is greater than max_x.")

        if [bbox_data[i] for i in bbox_data.keys() if '_y' in i if bbox_data[i] > 90 or bbox_data[i] < -90]:
            if [bbox_data[i] for i in bbox_data.keys() if '_x' in i if bbox_data[i] > 180 or bbox_data[i] < -180]:
                raise Exception(
                    "Improper bbox parameter: {} coordinate outside of range -90:90 and {} outside of range -180:180".format(
                        (bbox_list[0], bbox_list[2]), (bbox_list[1], bbox_list[3])))
            else:
                raise Exception("Improper bbox parameter: {} coordinate outside of range -90:90.".format(
                    (bbox_list[0], bbox_list[2])))
        elif [bbox_data[i] for i in bbox_data.keys() if '_x' in i if bbox_data[i] > 180 or bbox_data[i] < -180]:
            raise Exception("Improper bbox parameter: {} coordinate outside of range -180:180.".format(
                (bbox_list[1], bbox_list[3])))

    else:
        raise Exception("Projection must be EPSG:4326 (exactly 4 coordinates)")


def download_file(response, format_response=None, download_path=None):
    """
    Function downloads response to local machine
    Args:
        response: Dictionary of response object
        format_response: String of file type
        download_path: String of desired download path location on local machine
    Returns:
        String of download path location on local machine
    """

    if download_path:
        filename = download_path
    else:
        filename = 'Download.' + format_response
        filename = os.path.join(os.getcwd(), filename)
    if os.path.isfile(filename):
        while os.path.isfile(filename):
            filename = os.path.join(os.path.split(filename)[0], os.path.split(filename)[1].split('.')[0] + '_dup.' +
                                    os.path.split(filename)[1].split('.')[1])
    with open(filename, 'wb') as output_file:
        output_file.write(response.content)

    return filename


def _remove_cache(querystring):
    """
    Function assigns random characters to bypass caching
    Args:
        querystring: Dictionary of the desired query
    Returns:
        Dictionary of updated query string with random characters
    """

    pool_list = string.digits + string.ascii_letters
    random_characters1 = ''.join(i for i in random.choices(pool_list, k=25))
    random_characters2 = ''.join(i for i in random.choices(pool_list, k=25))
    querystring.update({random_characters1:random_characters2})
    return querystring

def aoi_coverage(bbox, response):
    """
    Function adds the percentage of the desired feature that is covered by the AOI
    Args:
        bbox: String of Coordinates separated by comma
        response: Response object from a WFS request call
    Returns:
        Updated dictionary of the json object
    """

    coverage = response.json()
    box_order = bbox.split(',')
    aoi_polygon = shapely.geometry.box(
        *(float(box_order[1]), float(box_order[0]), float(box_order[3]), float(box_order[2])), ccw=True)
    for feature in coverage['features']:
        if feature['geometry']['type'] == 'Polygon':
            feature_wkt = shapely.wkt.loads("POLYGON (({}))".format(
                ", ".join([" ".join([str(k) for k in i]) for i in feature['geometry']['coordinates'][0]])))
            feature['coverage'] = aoi_polygon.intersection(feature_wkt).area / feature_wkt.area
        else:
            feature_wkt = shapely.wkt.loads("MULTIPOLYGON ({})".format(", ".join(
                ["(({}))".format(", ".join([" ".join([str(k) for k in i]) for i in l[0]])) for l in
                 feature['geometry']['coordinates']])))
            feature['coverage'] = aoi_polygon.intersection(feature_wkt).area / feature_wkt.area

    return coverage

def _check_image_format(img_format):
    """
    Function checks image format given for each call
    Args:
        img_format: String of desired image format
    Returns:
        String of image format with 'image/' preceding to comply with Maxar API calls
    """

    acceptable_format = ['jpeg', 'png', 'geotiff']
    if img_format in acceptable_format:
        return 'image/' + img_format
    else:
        raise Exception('Format not recognized, please use acceptable format for downloading image.')

def _check_typeName(typename):
    acceptable_types = ['FinishedFeature', 'TileMatrixFeature', 'ImageInMosaicFeature', 'MaxarCatalogMosaicProducts',
                        'MaxarCatalogMosaicSeamlines', 'MaxarCatalogMosaicTiles']
    if typename not in acceptable_types:
        raise Exception('{} is not an acceptable TypeName. Please use one of the following {}'.format(typename, acceptable_types))

class BoundedThreadPoolExecutor(ThreadPoolExecutor):

    def __init__(self, *args, **kwargs):
        super(BoundedThreadPoolExecutor, self).__init__(*args, **kwargs)
        self._work_queue = queue.Queue()