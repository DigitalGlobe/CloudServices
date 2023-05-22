import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent.resolve()

README = (HERE / "README.md").read_text()

setup(
  name = 'Maxar_OGC',
  version = '1.3.1',
  license='MIT',
  description = 'SDK for interacting with Maxar imagery platforms',
  long_description=README,
  long_description_content_type="text/markdown",
  author = 'GCS Marianas Team',
  author_email = 'DL-GCS-Marianas@digitalglobe.com',
  project_urls = {
        'Documentation': 'https://cloudservices.readthedocs.io/en/latest/index.html',
        'Source': 'https://github.com/DigitalGlobe/CloudServices'
        },
  keywords = ['OGC', 'WMS', 'WFS', 'WMTS', 'WCS', 'MAXAR', 'IMAGERY', 'GIS'],
  python_requires= '>=3.6',
  install_requires=[
          'pyproj',
          'shapely',
          'requests',
          'ipython',
          'pillow',
          'click',
          #'rasterio',
          'beautifulsoup4',
          'lxml'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
  entry_points='''
    [console_scripts]
    search=Maxar_OGC.cli_commands:search
    config=Maxar_OGC.cli_commands:config_file
    password=Maxar_OGC.cli_commands:reset_password
    download=Maxar_OGC.cli_commands:download
    bands=Maxar_OGC.cli_commands:band_manipulation
    area=Maxar_OGC.cli_commands:calculate_bbox_sqkm
    '''
)
