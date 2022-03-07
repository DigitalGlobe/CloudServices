**Code examples**
=================

The following code examples walk through how to get started using the basic features of this SDK. It assumes that the ``.ogc-config`` file has been set up.
All of the examples assume that the Interface object has been instantiated in the following manner::

 from Maxar_OGC import Interface
 sw_ogc = Interface()


*Search*

Used to locate features and metadata within a bounding box. A CQL filter can also be passed as an argument::

 sw_ogc.search(bbox='39.7663253,-104.9414063,39.7747695,-104.9304199')

Returns a dictionary of features within the bbox.

*Download Image*

Downloads image specified to root directory with the default name of 'Download'. A specific path and name can be entered with the ``outputpath`` argument::

 sw_ogc.download_image(height=256, width=256, bbox='39.7663253,-104.9414063,39.7747695,-104.9304199',img_format='jpeg')

*Metadata*

Returns a dictionary of metadata of features within the bbox::

 sw_ogc.metadata(bbox='39.7663253,-104.9414063,39.7747695,-104.9304199')

*Band Manipulation*

Used to manipulate the band combination of an image. Optionals ``download`` argument and ``outputpath`` kwarg can be used to download the image::

 sw_ogc.band_manipulation(bbox='39.7663253,-104.9414063,39.7747695,-104.9304199', featureid='f4053158236d148d333c9df075ef4124', band_combination=['R','G','B'])

*Discover Browse*

Returns the browse image associated with a feature id or legacy id::

 sw_ogc.discover_browse(input_id='f4053158236d148d333c9df075ef4124')
