import ConfigParser
import sys
import requests
import xmltodict
import base64

class OneLoginConnection:

    # connection settings
    onelogin_api_token = None
    onelogin_api_url = "https://app.onelogin.com/api/v2/users"

    def __init__(self, config_file):
        """
        Initializes OneLogin REST API v2 communication wrapper with provided config file
        """
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        try:
            self.onelogin_api_token = config.get('onelogin', 'api_token')
        except ConfigParser.NoOptionError as e:
            print "[x] Error: Config file is not complete! Section '%s' must contain option '%s'. " \
                  "Check config examples at https://github.com/Oomnitza.\nExiting." % (e.section, e.option)
            sys.exit(2)

    def fetch_all_users(self):
        """
        Connects to OneLogin server using configuration and attempts to query
        and return all users.

        Reference: https://onelogin.zendesk.com/hc/en-us/articles/201175524-Users-API
        """
        auth_param = "Basic %s:" % base64.standard_b64encode(self.onelogin_api_token)
        headers = {'Authorization': auth_param}
        response = requests.get(self.onelogin_api_url, headers=headers)
        try:
            response.raise_for_status()
            return xmltodict.parse(response.text)['users']
        except requests.exceptions.HTTPError as e:
            print "[x] Error: Error occurred during OneLogin /api/v2/users call: '%s'. Check the options in the config" \
                  " file in the '[onelogin]' section.\nExiting. " % e.message
            sys.exit(2)