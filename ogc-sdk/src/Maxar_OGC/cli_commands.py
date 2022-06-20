import click
import sys
import os
from Maxar_OGC.interface import Interface


def check_for_config():
    home_dir = os.path.expanduser("~")
    if os.path.exists(os.path.join(home_dir, '.ogc-config')):
        cli_interface = Interface()
    else:
        raise Exception("OGC config file not found. Please ensure that your config file is located in your home "
                        "directory")
    return cli_interface


@click.command()
@click.option('--tenant', '-t', help='Desired tenant', type=str, prompt='Please enter tenant')
@click.option('--connectid', '-c', help='Your connect Id', type=str, prompt='Please enter connect Id')
@click.option('--username', '-u', help='Your username', type=str, prompt='Please enter your username if required',
              default=' ')
@click.option('--password', '-p', help='Your password', type=str, prompt='Please enter your password if required',
              default=' ')
def config_file(tenant, connectid, username=None, password=None):
    """
    Function creates a configuration file for authentication use for Maxar tenants
    """

    if tenant.lower() == "securewatch":
        domain = "https://securewatch.maxar.com/"
    elif tenant.lower() == "earthwatch":
        domain = "https://access.maxar.com/"
    elif tenant.lower() == "evwhs":
        domain = "https://evwhs.digitalglobe.com/"
    else:
        raise Exception('{} is not a valid tenant, please enter a valid tenant'.format(tenant))
    config = ['[ogc]', 'user_tenant = {}'.format(domain.lower()), 'user_connectid = {}'.format(connectid),
              'user_name = {}'.format(username), 'user_password = {}'.format(password)]
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".ogc-config"), "w") as f:
        for line in config:
            f.write(line)
            f.write('\n')


@click.command()
@click.option('--password', '-p', help="New password", type=str, prompt='Enter new password')
def reset_password(password):
    """
    Function updates the password in the configuration file
    """

    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".ogc-config"), 'r') as f:
        text = f.readlines()
        text[4] = 'user_password = {}\n'.format(password)
        with open(os.path.join(home_dir, ".ogc-config"), 'w') as f:
            f.writelines(text)


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)', type=str)
@click.option('--filter', '-f', help='CQL filter used to refine data of search', type=str)
@click.option('--shapefile', '-s', help='Binary of whether or not to return as shapefile format', type=bool)
@click.option('--featureprofile', '-fp', help='String of the desired stacking profile. Defaults to account Default',
              type=str)
@click.option('--typename', '-t',
              help='String of the typename. Defaults to FinishedFeature. Example input MaxarCatalogMosaicProducts',
              type=str)
def search(bbox=None, filter=None, shapefile=False, featureprofile=None, typename=None):
    """
    Function searches an AOI using the WFS method and returns a list of features and their metadata that intersect with
    the AOI
    """

    check = check_for_config()
    if not typename:
        wfs = check.search(bbox, filter, shapefile, featureprofile=featureprofile)
    else:
        wfs = check.search(bbox, filter, shapefile, featureprofile=featureprofile, typename=typename)
    click.echo(wfs)


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)', type=str)
@click.option('--height', '-h', help='Integer value representing the vertical number of pixels to return', type=int)
@click.option('--width', '-w', help='Integer value representing the horizontal number of pixels to return', type=int)
@click.option('--img_format', '-img', help='String of the format of the response image either jpeg, png or geotiff',
              type=str)
@click.option('--identifier', '-id', help='String of the feature id', type=str)
@click.option('--gridoffsets', '-g', help='Sting of the pixel size to be returned in X and Y dimensions', type=str)
@click.option('--zoom_level', '-z', help='Integer value of the zoom level. Used for WMTS', type=int)
@click.option('--download', '-d', help='Boolean of user option to download file locally', type=bool)
def download(bbox=None, height=None, width=None, img_format=None, identifier=None, gridoffsets=None, zoom_level=None,
             download=True):
    """
    Function downloads an image or a list of image calls and returns the file location of the download. NOTE: Structure
    of call should be structured with one of the following:
    1) bbox, zoom_level, img_format
    2) bbox, identifier, gridoffsets, img_format
    3) bbox, img_format, height, width
    """

    check = check_for_config()
    if zoom_level:
        if not bbox:
            raise Exception('zoom_level must have a bbox')
        else:
            wmts = cli_interface.download_image(zoom_level=zoom_level, bbox=bbox, img_format=img_format)
        click.echo(wmts)
    elif identifier:
        if not gridoffsets or not bbox:
            raise Exception('Identifiers must have gridoffset and bbox')
        else:
            wcs = cli_interface.download_image(bbox=bbox, identifier=identifier, gridoffsets=gridoffsets,
                                               img_format=img_format)
        click.echo(wcs)
    else:
        if not bbox or not img_format or not width or not height:
            raise Exception('height/width must have a bbox and an img_format')
        else:
            wms = cli_interface.download_image(bbox=bbox, img_format=img_format,
                                               height=height, width=width, display=False)
        click.echo(wms)


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)', type=str)
@click.option('--featureid', '-id', help='String of the feature id', type=str)
@click.option('--band_combination', '-band', help='String of the desired band combination of 1-4 items ex: "R, G, B"',
              type=str)
@click.option('--height', '-h', help='Integer value representing the vertical number of pixels to return', type=int)
@click.option('--width', '-w', help='Integer value representing the horizontal number of pixels to return', type=int)
@click.option('--img_format', '-img', help='String of the format of the response image either jpeg, png or geotiff',
              type=str)
def band_manipulation(bbox=None, featureid=None, band_combination=None, height=256, width=256, img_format='jpeg'):
    """
    Function manipulates the bands of a SWIR 8-band or MS1_MS2 image and returns the file location of the downloaded
    image
    """

    check = check_for_config()
    band_combination = sys.argv[6].split(',')
    band_combination = [i.strip(' ') for i in band_combination]
    bands = cli_interface.band_manipulation(bbox=bbox, featureid=featureid, band_combination=band_combination,
                                            height=height, width=width, img_format=img_format)
    click.echo(bands)


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)', type=str,
              prompt='Enter bbox in miny,minx,maxy,maxx format')
def calculate_bbox_sqkm(bbox=None):
    """
    Function calculates the area in square kilometers of the bbox
    """

    check = check_for_config()
    sqkm = cli_interface.calculate_sqkm(bbox=bbox)
    click.echo("Square kilometers of bbox is: {}".format(sqkm))
