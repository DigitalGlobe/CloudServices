# Quick Start

## Quick Start Guide

After setting up the config file from the [Getting Started](/) section, run the following code to create an instance of the Interface Class. This instance will be used to access functionality of the OGC-SDK.

	from Maxar_OGC import Interface
	interface = Interface()
	
In the following example, we will search for an AOI within the feature id `932f7992a4d86a9ca412c024c22792ce`. Our AOI will be the bbox `39.906477,-105.010843,39.918031,-104.991939`. The results will be returned as a json object which we will then print.


	from Maxar_OGC import Interface
	interface = Interface()
	
	feature_id = '932f7992a4d86a9ca412c024c22792ce'
	aoi = '39.906477,-105.010843,39.918031,-104.991939'
	
	results = interface.search(filter="featureId='{}'".format(feature_id), bbox=aoi)
	
	print(results)
	
The results will be a list of dictionaries
	
	[
	 {'type': 'Feature', 
	  'id': '932f7992a4d86a9ca412c024c22792ce', 
	  'geometry': 
	    {'type': 'Polygon', 
		 'coordinates': [[[-105.1551495, 40.2601995], [-105.04295325, 40.27042125], [-104.930757, 40.280643], [-104.934771, 39.79818675], [-104.938785, 39.3157305], [-105.0430545, 39.3136875], [-105.147324, 39.3116445], [-105.15123675, 39.785922], [-105.1551495, 40.2601995]]]
		}, 
	  'geometry_name': 'geometry', 
	  'properties': 
	    {'featureId': '932f7992a4d86a9ca412c024c22792ce', 
		 'acquisitionDate': '2020-11-01 18:04:25', 
		 'acquisitionTime': 1804, 
		 'sensorType': '', 
		 'source': 'WV02', 
		 'sourceUnit': 'Strip', 
		 'productType': 'Pan Sharpened Natural Color', 
		 'CE90Accuracy': '8.4 meters', 
		 'RMSEAccuracy': '3.91 meters', 
		 'cloudCover': 0, 
		 'offNadirAngle': 20.23818, 
		 'sunElevation': 34.886154, 
		 'sunAzimuth': 168.41226, 
		 'groundSampleDistance': 0.5, 
		 'groundSampleDistanceUnit': 'Meter', 
		 'dataLayer': 'daily_take', 
		 'legacyDescription': 'AOI4_L3_WV2', 
		 'outputMosaic': False, 
		 'colorBandOrder': 'RGB', 
		 'assetName': 'FINISHED', 
		 'assetType': 'PRODUCT_GEOMETRY', 
		 'legacyId': '10300100AE766C00', 
		 'factoryOrderNumber': '013291395-10', 
		 'perPixelX': 4.5e-06, 
		 'perPixelY': -4.5e-06, 
		 'crsFromPixels': 'EPSG:4326', 
		 'url': '', 
		 'ageDays': 613, 
		 'formattedDate': '2020-11-01', 
		 'ingestDate': '2020-11-01 21:19:29', 
		 'spatialAccuracy': '1:12,000', 
		 'earliestAcquisitionDate': '2020-11-01 18:04:36', 
		 'latestAcquisitionDate': '2020-11-01 18:04:36', 
		 'pixelsIngested': True, 
		 'preciseGeometry': True, 
		 'vendorName': '', 
		 'vendorReference': '', 
		 'companyName': 'DigitalGlobe', 
		 'acquisitionType': '', 
		 'orbitDirection': '', 
		 'licenseType': '', 
		 'isBrowse': False, 
		 'isMirrored': False, 
		 'isMultipleWKB': False, 
		 'copyright': 'Image Copyright 2020 DigitalGlobe Inc', 
		 'beamMode': '', 
		 'polarisationMode': '', 
		 'polarisationChannel': '', 
		 'antennaLookDirection': '', 
		 'minimumIncidenceAngle': None, 
		 'maximumIncidenceAngle': None, 
		 'incidenceAngleVariation': None, 
		 'niirs': 4.9, 
		 'verticalAccuracy': None, 
		 'tagsAsString': ''
		 }, 
	  'coverage': 0.0010546500824560633}
	]
		
For more details, see [Search](/image_search)
	
To download the image to the default location ``C:\Users\<user>\download.jpeg`` or `~\download.jpeg`, we will use the following code. This will download the imagery from the feature ID within the aoi and return the location of the downloaded image.

	from Maxar_OGC import Interface
	interface = Interface()

	feature_id = '932f7992a4d86a9ca412c024c22792ce'
	aoi = '39.906477,-105.010843,39.918031,-104.991939'
	cql_filter = "featureId='{}'".format(feature_id)

	download = interface.download_image_by_pixel_count(bbox=aoi, height=512, width=512, img_format='jpeg', filter=cql_filter)
	print(download)
	
The result should be a jpeg as shown below.

![satellite_image](/images/sample_image.jpeg)

For more details, see [Download Image by Pixel Count](/download_image_pixel_count)
	