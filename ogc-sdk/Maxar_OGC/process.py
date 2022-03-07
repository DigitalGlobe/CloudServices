import os
import pyproj
import shapely.ops as ops
from shapely.geometry.polygon import Polygon
from functools import partial
import random
import string


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
            miny = float(bbox_list[0])
            minx = float(bbox_list[1])
            maxy = float(bbox_list[2])
            maxx = float(bbox_list[3])
        except:
            raise Exception('Bbox coordiantes must be numeric.')
        bbox_data = {'min_y': miny, 'min_x': minx, 'max_y': maxy, 'max_x': maxx}
        if bbox_data['min_y'] >= bbox_data['max_y']:
            raise Exception("Improper order of bbox: min_y is greater than max_y.")
        if bbox_data['min_x'] >= bbox_data['max_x']:
            raise Exception("Improper order of bbox: min_x is greater than max_x.")
        for key in bbox_data.keys():
            if 'y' in key:
                if bbox_data[key] > 90 or bbox_data[key] < -90:
                    raise Exception("Improper bbox parameter: {} coordinate outside of range -90:90.".format(key))
            elif 'x' in key:
                if bbox_data[key] > 180 or bbox_data[key] < -180:
                    raise Exception("Improper bbox parameter: {} coordinate outside of range -180:180.".format(key))
    elif len(bbox_list) == 5:
        try:
            minx = float(bbox_list[0])
            miny = float(bbox_list[1])
            maxx = float(bbox_list[2])
            maxy = float(bbox_list[3])
            if bbox_list[4][0] == ' ':
                crs = bbox_list[4][1:]
            else:
                crs = bbox_list[4]
        except:
            raise Exception('Bbox coordinates must be numeric')
        bbox_data = {'min_y': miny, 'min_x': minx, 'max_y': maxy, 'max_x': maxx}
        if bbox_data['min_y'] >= bbox_data['max_y']:
            raise Exception("Improper order of bbox: min_y is greater than max_y.")
        if bbox_data['min_x'] >= bbox_data['max_x']:
            raise Exception("Improper order of bbox: min_x is greater than max_x.")
        for key in bbox_data.keys():
            if 'y' in key:
                if bbox_data[key] > 88985946 or bbox_data[key] < -88985946:
                    raise Exception(
                        "Improper bbox parameter: {} coordinate outside of range -88985946:88985946.".format(key))
            elif 'x' in key:
                if bbox_data[key] > 20037497 or bbox_data[key] < -20037497:
                    raise Exception(
                        "Improper bbox parameter: {} coordinate outside of range -20037497:20037497.".format(key))
        if crs != 'EPSG:3857':
            raise Exception("Projection must be EPSG:4326 (exactly 4 coordinates) or EPSG:3857 (4 coordinates plus 'EPSG:3857')")
    else:
        raise Exception("Projection must be EPSG:4326 (exactly 4 coordinates) or EPSG:3857 (4 coordinates plus 'EPSG:3857')")


def download_file(response, format_response=None, download_path=None):
    if download_path:
        filename = download_path
    else:
        filename = 'Download.' + format_response
    if os.path.isfile(filename):
        while os.path.isfile(filename):
            filename = filename.split('.')[0] + '_dup' + '.' + filename.split('.')[1]
    with open(filename, 'wb') as output_file:
        output_file.write(response.content)

    return filename


def _remove_cache(querystring):
    pool_list = string.digits + string.ascii_letters
    random_characters1 = ''.join(i for i in random.choices(pool_list, k=25))
    random_characters2 = ''.join(i for i in random.choices(pool_list, k=25))
    querystring.update({random_characters1:random_characters2})
    return querystring
