# Release Notes

## Version 1.4.0 (Oct 25, 2023)

- Added SAR download functionality for GEGD/EVWHS customers.
- Changed default thread number for `get_full_res_image` function from 100 to 25

## Version 1.3.1 (May 22, 2023)

- Bug fixes to get_full_res function
- CQL Checker was not allowing valid CQLs to pass, it has been removed for the time being

## Version 1.3.0 (January 6, 2023)
- New Features
	- Added checker to validate CQL filter. Exception will now be thrown if CQL filter format is incorrect.
	- Search function now includes two additional metadata fields. These are `coverage`, which provides the decimal ratio of the feature covered by the bbox and `bbox_coverage`, which provides the decimal ratio of the bbox covered by the feature.
	- Added `srsname` as an arg to several functions, defaulting to `EPSG:4326`. Previously this was available as a kwarg:
		- Search
		- Download Image
		- Download Full Resolution Image
		- Download Tiles
		- Download Image with Feature ID
		- Download Image by Pixel Count
		- Band Manipulation

## Version 1.2.0 (August 15, 2022)
- New Features
	- Added get_filter_parameters to return all parameters for a CQL filter
	- Updated search function with boolean for returning results as a csv

- Bug Fixes
	- Corrected issue with create mosaic not running when selected as part of the get_full_res function

## Version 1.1.2 (Jul 7, 2022)
- Update documentation
	- Added quickstart guide and formatting changes

## Version 1.1.1 (Jul 5, 2022)
- Bug Fixes
	- Fixed issue with No Auth connectid requiring a username and password

## Version 1.1.0 (Jun 20, 2022)
- New Features
	- CLI commands
	- Create Mosaic 
- Bug Fixes
	- Fixed issue with shapefile downloads not accepting user-defined directory path
