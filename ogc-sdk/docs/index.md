## Getting started

**Maxar-OGC** is a Python library for accessing Maxar's imagery platforms
to search and download imagery. Connection is established using connect id 
and login credentials.


Installation:

1. Installation via pip is recommened: ``pip install Maxar-OGC`` in your environment.
2. We recommend creating a credentials file to store your login information for future sessions in one of two ways. 
	* Use the command line interface command ``config`` from the command prompt and follow the prompts. See [Command Line Interface](cli_commands)
	* Create a credentials file called ``.ogc-config`` in your home directory with the following format

			[ogc] 
			user_name=<your-user-name>
			user_password=<your-password>
			user_tenant=<your-base-url> i.e. https://securewatch.digitalglobe.com
			user_connectid=<your-connectid> 

After creating your config file, you are now ready to start with the [Quickstart Guide](quickstart)