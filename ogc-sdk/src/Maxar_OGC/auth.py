import os
import base64
import requests
import random


class Auth:
    """
    This class handles authentication for the SDK when a config file is not present the user must pass the args below.
    Config file name convention: '.ogc-config'
    Please create .ogc-config in home dir.
    Args:
        host = desired environment
        connectid = the desired account connectid
        username = username for your account
        password = password for your account
        sar_username = username for your sar data access
        sar_password = password for your sar data access

    Returns:
        session_object = dictionary containing keys 'base_url', 'connectid', 'headers'
    """

    def __init__(self, base_url=None, connectid=None, username=None, password=None, sar_username=None, sar_password=None):
        self.base_url = base_url  # host name "https://securewatch.maxar.com/"
        self.connect_id = connectid
        self.username = username
        self.password = password
        self.version = 'python_2.0_1.4.0'
        self.sar_username = sar_username
        self.sar_password = sar_password

        if not self.base_url:
            dir_path = os.path.expanduser('~')
            file = '.ogc-config'
            full_path = os.path.join(dir_path, file)
            if os.path.isfile(full_path):
                self.base_url, self.connect_id, self.username, self.password, self.sar_username, self.sar_password = self._get_environment(full_path)
            else:
                raise ValueError("Please create .ogc-config in home dir.")

        else:
            acceptable_urls = ["https://securewatch.maxar.com/", "https://securewatch.digitalglobe.com/",
                               "https://access.maxar.com/", "https://services.digitalglobe.com/",
                               "https://evwhs.digitalglobe.com/"]
            if self.base_url not in acceptable_urls:
                raise ValueError("Base_url must match acceptable Maxar url.")
        self.session_object = self._get_session()
        self._check_auth()

    @staticmethod
    def _get_environment(file):
        with open(file) as config_file:
            cred_dict = {}
            for line in config_file.readlines():
                if '=' in line:
                    key, value = line.split('=')
                    key = key.strip()
                    value = value.strip()
                    if '\n' in value:
                        value = value.replace('\n', '')
                    cred_dict.update({key: value})
        tenant = cred_dict['user_tenant']
        connectid = cred_dict['user_connectid']
        try:
            user_name = cred_dict['user_name']
        except:
            user_name = None
        try:
            password = cred_dict['user_password']
        except:
            password = None
        try:
            sar_username = cred_dict['saruser']
        except:
            sar_username = None
        try:
            sar_password = cred_dict['sarpass']
        except:
            sar_password = None

        return tenant, connectid, user_name, password, sar_username, sar_password

    def _check_auth(self):
        connectid = self.session_object['connectid']
        host = self.session_object['base_url']
        headers = self.session_object['headers']
        sdk_version = self.session_object['version']
        if not connectid:
            raise Exception('Connect ID field is required. Please include a valid Connect ID.')

        if (not self.username and self.password) or (not self.password and self.username):
            raise Exception('Username and Password must both be provided.')

        #create random string to prevent caching
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        randomLetters = ''.join(random.choices(letters, k=6))

        testBBOX = '33.204230,-92.672525,33.210711,-92.656228' #this is over the ocean to ensure no images get selected and speed
        url = "{}catalogservice/wfsaccess?REQUEST=GetFeature&TYPENAME=DigitalGlobe:FinishedFeature&SERVICE=WFS&VERSION=2.0.0&CONNECTID={}&BBOX={}&SRSNAME=EPSG:4326&SDKversion={}&random={}".format(host,connectid,testBBOX,sdk_version,randomLetters)
        response = requests.request("GET", url, headers=headers)

        if response.status_code != 200:
            raise Exception('Unable to connect. Status code equals {}'.format(response.status_code))

    def _get_session(self):
        session = {'base_url': self.base_url,
                   'connectid': self.connect_id,
                   'version': self.version}
        if self.username and self.password:
            header = {'Authorization': 'Basic {}'.format(self._encode_creds(self.username, self.password))}
        if self.sar_username and self.sar_password:
            sar_header = {'Authorization': 'Basic {}'.format(self._encode_creds(self.sar_username,self.sar_password))} 
            session.update({"sar_header": sar_header})
        session.update({'headers': header})
        return session

    def _encode_creds(self, username, password):
        auth = "{}:{}".format(username, password)
        encode = str(base64.b64encode(bytes(auth, 'utf-8')))
        encode = encode[2:-1]
        return str(encode)

