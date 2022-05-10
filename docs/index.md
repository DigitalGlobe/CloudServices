## Getting started

**Maxar-OGC** is a Python library for accessing Maxar's imagery platforms
to search and download imagery. Connection is established using connect id 
and login credentials.


Installation:

1. pip install Maxar-OGC
2. Create a credentials file called ``.ogc-config`` in the following format

    `[ogc]
user_name=<your-user-name>
user_password=<your-password>
user_tenant=<your-base-url> i.e. https://securewatch.digitalglobe.com
user_connectid=<your-connectid>`
