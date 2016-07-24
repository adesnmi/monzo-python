import requests
import datetime

class MondoClient(object):
    API_URL = 'https://api.getmondo.co.uk/'
    def __init__(self, access_token):
        self.access_token = access_token

    def whoami(self):
        """Gives information about an access token."""
        url = "{0}/ping/whoami".format(self.API_URL)
        headers = {'Authorization': 'Bearer {0}'.format(self.access_token) }
        r = requests.get(url, headers=headers)
        return r.json()

    
