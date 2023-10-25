# Sar Data Download (GEGD/EVWHS ONLY)

#### *Note:* Additional credentials are required to utilize this functionality. These may either be passed in during intialization or added to the `.ogc-config` file.

During instantation:
		
	from Maxar_OGC import Interface
	interface = Interface(base_url=<base_url>, connectid=<connectid>, 
						  username=<username>, password=<password>, 
						  sar_username=<sarusername>, sar_password=<sarpassword>)
	
Updating `.ogc-config`
	
	[ogc]
	user_tenant = <base_url>
	user_connectid = <connectid>
	user_name = <username>
	user_password = <password>
	saruser = <sarusername>
	sarpass = <sarpassword>
	
Using CLI

	config --saruser(-S) <sarusername> --sarpass(-P) <sarpassword>

## Args:

#### sar_url (str):

  A `sar_url` (Sar URL) is the URL from the "legacyID" field in the metadata of the image.

   **Example:**
   interface.sar_download("https://sar-download.3pa.maxar.com/capella/archive/2023/01/13/51271088-29c2-4014-bc57-2280d15915f3/index.html")	 


## Kwargs:

#### outputpath (str):

  The `outputpath` is the desired directory for the data to be downloaded. If not provided defaults to the users home directory

   **Example:**
   
     interface.sar_download("https://sar-download.3pa.maxar.com/capella/archive/2023/01/13/51271088-29c2-4014-bc57-2280d15915f3/index.html", outputpath=r'C:\Users\<user>')

