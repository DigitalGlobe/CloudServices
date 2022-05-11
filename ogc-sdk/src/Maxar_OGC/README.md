# Installation Instructions
1. Install python 3.7
1. Ensure the following python modules are installed (requests, pyproj, shapely, functools, beautifulsoup4, IPython)
1. Download/Clone repo to local machine.
1. Extract repo zip file
1. Move contents of "marians-team/share-libraries" to assigned system path
   * Or, add "marians-team/share-libraries" directory to system paths
1. Create a credentials file called `.ogc-config` 
   * The file should look like:
   ```
   [ogc]
   user_name=<your-user-name>
   user_password=<your-password>
   user_tenant=https://securewatch.digitalglobe.com/
   user_connectid=<your-desired-connectid>
   ```
# Usage Instructions
```
from ogc import Interface
try:
  sw_ogc = Interface() # if .ogc-config was created
except:
  sw_ogc = Interface('https://securewatch.maxar.com/','<connect_id>') # if .ogc-config was not created
print(help(sw_ogc))
```
