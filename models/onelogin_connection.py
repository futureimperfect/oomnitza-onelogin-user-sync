import collections
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

    def get_max_id_in(self, onelogin_users):
        """
        @returns the highest ID in onelogin_users.
        """
        onelogin_user_ids = []

        # for user in onelogin_users['user']:
        for user in onelogin_users:
            onelogin_user_ids.append(int(user['id']))

        return max(onelogin_user_ids)

    def fetch_all_users(self, users=None, max_id=None):
        """
        Connects to OneLogin server using configuration and attempts to query
        and return all users.

        Reference: https://onelogin.zendesk.com/hc/en-us/articles/201175524-Users-API
        """
        auth_param = "Basic %s:" % base64.standard_b64encode(self.onelogin_api_token)
        headers = {'Authorization': auth_param}
        # The OneLogin API returns 100 results at a time. We'll start at 0 and
        # set the from_id parameter to the max_id for each subsequent request.
        uri = self.onelogin_api_url if not max_id else self.onelogin_api_url + '?from_id=%s' % max_id
        response = requests.get(uri, headers=headers)

        try:
            response.raise_for_status()
            try:
                _users = xmltodict.parse(response.text)['users']['user'] + \
                    users if users else xmltodict.parse(response.text)['users']['user']
            except TypeError:
                # If the OneLogin API returns one result users won't
                # be in a list, there will just be one OrderedDict
                l = []
                d = xmltodict.parse(response.text)['users']['user']
                if isinstance(d, collections.OrderedDict):
                    l.append(d)
                    _users = l + users if users else xmltodict.parse(response.text)['users']['user']
            except KeyError:
                # The 'users' key doesn't exist.
                # We've likely gotten all the users
                # we're going to get
                _users = users
            _max_id = self.get_max_id_in(_users) if _users else None
            if max_id and int(_max_id) == int(max_id) and users is not None:
                return users
            else:
                return self.fetch_all_users(users=_users, max_id=_max_id)

        except requests.exceptions.HTTPError as e:
            print "[x] Error: Error occurred during OneLogin /api/v2/users call: '%s'. Check the options in the config" \
                  " file in the '[onelogin]' section.\nExiting. " % e.message
            sys.exit(2)
