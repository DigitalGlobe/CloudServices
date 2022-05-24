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

# How to Install Jupyter Notebooks
## Link to Jupyter labs install instructions Here
```
https://jupyter.org/install
```
## Recommended Steps

In your python 3.7 environment run the following installation commands
```
pip install notebook
```
After Installation is completed launch the Jupyter Notebook in your python environment with 
```
jupyter notebook
```

## (Optional) Creating a Shortcut for your Specific Python Environment Jupyter Notebook.
Create a new Short cut on your desktop. 
After Naming your shortcut right click and select Properties
Under the Shortcut tab
In the target box input the following command. Substituting in the Path to your Anaconda3 and the name of your python environment. 

```
%windir%\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy ByPass -NoExit -Command "& '<Path to Anaconda3>\condabin\conda-hook.ps1' ; "conda activate <PythonEnvironmentName>"; "jupyter notebook"
```
in the Start In box input 
```
%cd%
```
This will allow you to store this shortcut anywhere on your computer.