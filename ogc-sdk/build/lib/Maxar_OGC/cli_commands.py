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
@click.option('--domain', '-d', help='Desired domain', type=str)
@click.option('--connectid', '-c', help='Your connect Id', type=str)
@click.option('--username', '-u', help='Your username (if required)', type=str)
@click.option('--password', '-p', help='Your password (if required)', type=str)
def config_file(domain=None, connectid=None, username=None, password=None):
    """
    Function creates a configuration file for authentication use for Maxar tenants
    """

    home_dir = os.path.expanduser("~")
    if os.path.exists(os.path.join(home_dir, '.ogc-config')):
        check = input("An ogc-config file already exists. Overwrite?[y/n]: ")
        if check.lower() == 'n':
            return click.echo("Config file setup aborted")
        elif check.lower() == 'y':
            pass
        else:
            return click.echo("Invalid input. Please run command again and enter either y or n")

    if domain:
        domain = domain
    else:
        domain = click.prompt('Desired tenant')

    domain_list = ["https://securewatch.maxar.com/", "https://access.maxar.com/", "https://evwhs.digitalglobe.com/",
                   "https://services.digitalglobe.com/", "https://securewatch.digitalglobe.com/"]
    if domain.lower() == "securewatch":
        domain = "https://securewatch.maxar.com/"
    elif domain.lower() == "earthwatch":
        domain = "https://access.maxar.com/"
    elif domain.lower() == "evwhs":
        domain = "https://evwhs.digitalglobe.com/"
    else:
        domain = domain
    if domain.lower() not in domain_list:
        return click.echo('{} is not a valid tenant. Please enter a valid tenant'.format(domain))

    if connectid:
        connectid = connectid
    else:
        connectid = click.prompt('Your connect Id')
    if domain and connectid and username and password:
        auth = 'y'
    else:
        auth = click.prompt('Auth required?[y/n]')

    if auth.lower() == 'n':
        if username or password:
            return click.echo("Username and password not required, please try again")
        config = ['[ogc]', 'user_tenant = {}'.format(domain.lower()), 'user_connectid = {}'.format(connectid)]
        with open(os.path.join(home_dir, ".ogc-config"), "w") as f:
            for line in config:
                f.write(line)
                f.write('\n')

    elif auth.lower() == 'y':
        if username:
            username = username
        else:
            username = click.prompt('Your username')
        if password:
            password = password
        else:
            password = click.prompt('Your password', hide_input=True, confirmation_prompt=True)
        config = ['[ogc]', 'user_tenant = {}'.format(domain.lower()), 'user_connectid = {}'.format(connectid),
                  'user_name = {}'.format(username), 'user_password = {}'.format(password)]
        with open(os.path.join(home_dir, ".ogc-config"), "w") as f:
            for line in config:
                f.write(line)
                f.write('\n')
    else:
        return click.echo("Invalid input. Please run command again and enter either y or n")
    return click.echo("OGC config file created. File is located in {}".format(home_dir))


@click.command()
@click.option('--password', '-p', help="New password", type=str)
def reset_password(password):
    """
    Function updates the password in the configuration file
    """

    home_dir = os.path.expanduser("~")
    if os.path.exists(os.path.join(home_dir, '.ogc-config')):
        pass
    else:
        return click.echo("No .ogc-config file found. Please create file")
    with open(os.path.join(home_dir, '.ogc-config'), 'r') as f:
        lines = len(f.readlines())
        if lines > 3:
            pass
        else:
            return click.echo("No existing password found. Please run config to update connection parameters")
    password = click.prompt('Enter new password', hide_input=True, confirmation_prompt=True)
    with open(os.path.join(home_dir, ".ogc-config"), 'r') as f:
        text = f.readlines()
        text[4] = 'user_password = {}\n'.format(password)
        with open(os.path.join(home_dir, ".ogc-config"), 'w') as f:
            f.writelines(text)
    return click.echo("Password updated")


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
