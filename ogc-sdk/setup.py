import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent.resolve()

README = (HERE / "README.md").read_text()

setup(
  name = 'Maxar_OGC',
  packages = ['Maxar_OGC'],
  version = '0.1.15',      
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
          'ipython'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',    
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.7',     
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)