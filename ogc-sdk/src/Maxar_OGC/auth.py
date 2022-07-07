import os
import base64
import requests


class Auth:
    """
    This class handles authentication for the SDK when a config file is not present the user must pass the args below.
    Config file name convention: '.ogc-config'
    Please create .ogc-config in home dir.
    Args:
        host = desired environment
        connectid = the desired account connectid
        username = member manager username
        password = member manager password
    Returns:
        session_object = dictionary containing keys 'base_url', 'connectid', 'headers'
    """

    def __init__(self, base_url=None, connectid=None, username=None, password=None):
        self.base_url = base_url  # host name "https://securewatch.maxar.com/"
        self.connect_id = connectid
        self.username = username
        self.password = password
        self.version = '1.1.2'

        if not self.base_url:
            dir_path = os.path.expanduser('~')
            file = '.ogc-config'
            full_path = os.path.join(dir_path, file)
            if os.path.isfile(full_path):
                self.base_url, self.connect_id, self.username, self.password = self._get_environment(full_path)
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
        return tenant, connectid, user_name, password

    def _check_auth(self):
        connectid = self.session_object['connectid']
        host = self.session_object['base_url']
        headers = self.session_object['headers']
        if not connectid:
            raise Exception('Connect ID field is required. Please include a valid Connect ID.')

        if (not self.username and self.password) or (not self.password and self.username):
            raise Exception('Username and Password must both be provided.')

        url = "{}catalogservice/wfsaccess?" \
              "REQUEST=GetCapabilities&SERVICE=WFS&VERSION=2.0.0&CONNECTID={}".format(host, connectid)
        response = requests.request("GET", url, headers=headers, data={})
        if response.status_code != 200:
            raise Exception('Unable to connect. Status code equals {}'.format(response.status_code))

    def _get_session(self):
        header = {}
        session = {'base_url': self.base_url,
                   'connectid': self.connect_id,
                   'version': self.version}
        if self.username and self.password:
            header.update({'Authorization': 'Basic {}'.format(self._encode_creds())})
        session.update({'headers': header})
        return session

    def _encode_creds(self):
        auth = "{}:{}".format(self.username, self.password)
        encode = str(base64.b64encode(bytes(auth, 'utf-8')))
        encode = encode[2:-1]
        return str(encode)
